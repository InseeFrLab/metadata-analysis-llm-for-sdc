import csv
import hashlib
import io
import os
import re
import threading
import time
from pathlib import Path

from flask import (
    Flask,
    jsonify,
    redirect,
    request,
    send_file,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from src import LLM_API_call
from src.clean import clean_sheet, dataframe_to_rows
from src.data import read_file
from src.extract_JSON_array import extract_array
from src.LLM_API_call import FORCE_JSON_INSTRUCTION, is_auto_continued
from src.transform_input import to_markdown, wrap
from src.transform_output import HEADER_BASE, max_spanning, spanning_pairs
from src.validate_json_output import validate

# `python backend/app.py` puts backend/ at sys.path[0] automatically, so `src`
# resolves with no manual sys.path handling — this is just for building paths.
_BACKEND = Path(__file__).parent
_PROJECT_ROOT = _BACKEND.parent

# ---------------------------------------------------------------------------
# Flask app — frontend/ is a sibling of backend/ at the project root, and is the
# static root, so index.html's "../../styles.css" / "../../_ds_bundle.js" /
# "../../assets/…" resolve to the real files under frontend/.
# ---------------------------------------------------------------------------
app = Flask(
    __name__, static_folder=str(_PROJECT_ROOT / "frontend"), static_url_path=""
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
app.config["UPLOAD_FOLDER"] = _PROJECT_ROOT / "uploads" / "temp"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# System prompt driving the two-phase pipeline (read once at startup).
_PROMPT_PATH = _BACKEND / "src" / "prompts" / "prompt_questions.md"
PROMPT = _PROMPT_PATH.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Offline stub — set SDC_STUB_REPLY to a saved LLM reply path to bypass the
# network call (useful for local testing without an API key). The endpoints
# call LLM_API_call.chat via the module object, so patching it here takes effect.
# ---------------------------------------------------------------------------
_stub = os.environ.get("SDC_STUB_REPLY")
if _stub:
    from unittest.mock import patch
    _reply_text = Path(_stub).read_text(encoding="utf-8")
    patch.object(LLM_API_call, "chat", return_value=_reply_text).start()

# ---------------------------------------------------------------------------
# In-memory session store
# ---------------------------------------------------------------------------
sessions: dict = {}
# sessions[session_id] = {
#   "file_name": str,        secure filename
#   "filepath":  str,        absolute temp path
#   "markdown":  str,        serialized Markdown
#   "baseline":  list,       frozen Phase 1 history (system, workbook, questions).
#                            Never mutated after upload — every Phase 2 run is
#                            rebuilt from it, which is what makes re-answering
#                            idempotent and free of self-anchoring.
#   "questions": list,       parsed question dicts ([] if auto_continued)
#   "results":   dict,       answers fingerprint -> validated records (per-session
#                            cache: an unchanged submission costs no model call)
#   "records":   list|None,  records currently shown/exported; None = no table yet
# }


# ---------------------------------------------------------------------------
# Pipeline glue (mirrors main.py, reusing the src/ primitives)
# ---------------------------------------------------------------------------

def serialize(filepath) -> str:
    """Workbook → cleaned Markdown (main.py steps I–III)."""
    data = read_file(str(filepath))
    cleaned_sheets = []
    for name, df in data.items():
        rows = clean_sheet(dataframe_to_rows(df))
        if any(any(c for c in r) for r in rows):
            cleaned_sheets.append((name, rows))
    return to_markdown(cleaned_sheets, title=Path(filepath).name)


def csv_cols_rows(records: list):
    """Flatten records to the verified 2n+5 column layout (main.py steps V–VI)."""
    n_span = max_spanning(records)
    cols = list(HEADER_BASE)
    for i in range(1, n_span + 1):
        cols += [f"spanning_{i}", f"hrc_spanning_{i}"]

    rows = []
    for rec in records:
        row = [rec["table_name"], rec["field"], rec["hrc_field"],
               rec["indicator"], rec["hrc_indicator"]]
        pairs = spanning_pairs(rec)
        for i in range(n_span):
            code, hrc = pairs[i] if i < len(pairs) else ("NA", "NA")
            row += [code, hrc]
        rows.append(row)
    return cols, rows


# ---------------------------------------------------------------------------
# Background jobs
#
# An LLM call can run for well over ten minutes, with no predictable ceiling.
# Holding an HTTP request open for that long is fragile whatever the proxy
# timeout is: Onyxia's reverse proxy cuts at ~60s, and even with that raised,
# a sleeping laptop / wifi blip / VPN reconnect would throw away a call with
# minutes of work invested in it.
#
# So the long endpoints don't answer synchronously. They start the work in a
# background thread, hand back a job id immediately, and the frontend polls
# /api/jobs/<id>. Nothing depends on a long-lived connection, so a dropped
# connection costs a poll, not a re-run.
# ---------------------------------------------------------------------------
jobs: dict = {}
# jobs[job_id] = {
#   "state":   "pending" | "done" | "error",
#   "body":    dict|None,  work_fn's return value once it has finished
#   "updated": float,      epoch seconds, for pruning finished jobs
# }

_JOB_TTL = 3600  # seconds a finished job stays readable


def prune_jobs():
    """Drop finished jobs past their TTL. Running jobs are never pruned —
    they have no upper bound on duration, which is the whole point."""
    cutoff = time.time() - _JOB_TTL
    stale = [jid for jid, j in list(jobs.items())
             if j["state"] != "pending" and j["updated"] < cutoff]
    for jid in stale:
        jobs.pop(jid, None)


def start_job(work_fn):
    """Run work_fn() in a background thread; reply 202 with its job id.
    work_fn must return a plain dict — its own success/failure shape — never
    raise (any internal try/except should convert failures to {"error": ...})."""
    prune_jobs()
    job_id = os.urandom(16).hex()
    jobs[job_id] = {"state": "pending", "body": None, "updated": time.time()}

    def run():
        try:
            body = work_fn()
        # Last-resort guard: work_fn already handles its own known errors.
        except Exception as exc:  # noqa: BLE001
            body = {"error": f"Erreur inattendue : {exc}"}
        # Publish the body before flipping the state — a poller that sees
        # "done" must never find a body that isn't there yet.
        jobs[job_id]["body"] = body
        jobs[job_id]["updated"] = time.time()
        jobs[job_id]["state"] = "error" if body.get("error") else "done"

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"job_id": job_id}), 202


# ---------------------------------------------------------------------------
# Routes — UI
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return redirect("/ui_kits/sdc-pipeline/")


@app.route("/ui_kits/sdc-pipeline/")
def pipeline_ui():
    return app.send_static_file("ui_kits/sdc-pipeline/index.html")


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(_e):
    return jsonify({"error": "Fichier trop volumineux (maximum 16 Mo)"}), 413


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@app.route("/api/jobs/<job_id>", methods=["GET"])
def job_status(job_id):
    """Poll a background job. Cheap and stateless-ish on purpose: the frontend
    may call this hundreds of times over a long run, and may resume calling it
    after a network interruption."""
    job = jobs.get(job_id)
    if not job:
        body = {"error": "Tâche introuvable ou expirée", "code": "job_not_found"}
        return jsonify(body), 404
    if job["state"] == "pending":
        return jsonify({"status": "pending"})
    if job["state"] == "error":
        body = job["body"]
        return jsonify({
            "status": "error",
            "error": body.get("error", "Erreur inconnue"),
            "code": body.get("code"),
        })
    return jsonify({"status": "done", "result": job["body"]})


@app.route("/api/upload", methods=["POST"])
def upload_metadata():
    """Step 1: accept workbook, serialize it, run LLM Phase 1."""
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Nom de fichier vide"}), 400

    session_id = os.urandom(16).hex()
    filename = secure_filename(f"{session_id[:8]}_{file.filename}")
    filepath = app.config["UPLOAD_FOLDER"] / filename
    file.save(str(filepath))

    def do_work():
        try:
            md = serialize(filepath)
        # Untrusted workbook: pandas/openpyxl/odfpy each raise their own error types.
        except Exception as exc:  # noqa: BLE001
            return {"error": f"Échec de la sérialisation : {exc}"}

        history = [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": wrap(md)},
        ]
        try:
            reply = chat_with_retry(history)
            print("=== RAW REPLY ===\n", reply, "\n =============")
        # External LLM call: openai client raises assorted network/auth error types.
        except Exception as exc:  # noqa: BLE001
            return {"error": llm_error_message(exc)}
        history.append({"role": "assistant", "content": reply})

        # Phase 1 auto-continued: the model answered directly in JSON, no questions.
        if is_auto_continued(reply):
            records = extract_array(reply)
            if records is None:
                return {"error": "Réponse du modèle illisible (aucun tableau JSON)."}
            errors = validate(records)
            if errors:
                msg = "Validation du schéma échouée :\n" + "\n".join(errors)
                return {"error": msg}
            sessions[session_id] = {
                "file_name": filename,
                "filepath": str(filepath),
                "markdown": md,
                "baseline": history,
                "questions": [],
                # There was nothing to ask, so this table already *is* the result
                # for the empty submission — seeding the cache with it means
                # continuing without adding anything costs no model call.
                "results": {answers_fingerprint(""): records},
                "records": records,
            }
            return {
                "session_id": session_id,
                "file_name": file.filename,
                "extracted_markdown": md,
                "questions": [],
                "records": records_to_ui(records),
            }

        parsed = parse_questions(reply)
        sessions[session_id] = {
            "file_name": filename,
            "filepath": str(filepath),
            "markdown": md,
            "baseline": history,
            "questions": parsed,
            "results": {},
            "records": None,
        }
        return {
            "session_id": session_id,
            "file_name": file.filename,
            "extracted_markdown": md,
            "questions": parsed,
        }

    return start_job(do_work)


@app.route("/api/answer", methods=["POST"])
def submit_answers():
    data = request.get_json(force=True) or {}
    session_id = data.get("session_id", "")
    sess = sessions.get(session_id)
    if not sess:
        body = {"error": "Session expirée côté serveur", "code": "session_expired"}
        return jsonify(body), 410

    extra_info = str(data.get("extra_info") or "").strip()
    answers = data.get("answers", {})

    # The text handed to the model *is* the identity of a submission: same text,
    # same model input, same table. So its fingerprint — not "does a table
    # already exist" — decides whether the producer actually changed anything.
    # That's what lets someone come back from Vérification, edit an answer and
    # get a genuinely new table, while an accidental round-trip through
    # « Retour aux questions » still costs nothing.
    answers_text = format_answers(sess["questions"], answers, extra_info)
    key = answers_fingerprint(answers_text)

    cached = sess["results"].get(key)
    if cached is not None:
        # Re-point the session at it: /api/export must hand back the table the
        # producer is looking at, including after reverting to earlier answers.
        sess["records"] = cached
        return jsonify({"status": "ok", "normalized_table": records_to_ui(cached)})

    def do_work():
        # Phase 2 (main.py 57-70): apply answers, force JSON if the model re-asks.
        # Always rebuilt from the frozen Phase 1 baseline, never from a previous
        # Phase 2 exchange. Two reasons: the model must not see its own earlier
        # table (at temperature 0 it anchors on it and re-emits it verbatim,
        # which reads as "my new answers were ignored"), and a run that fails
        # can't leave a dangling, unanswered turn for the next attempt to build
        # on. Every run therefore starts from the same clean state.
        history = sess["baseline"] + [{"role": "user", "content": answers_text}]
        try:
            reply = LLM_API_call.chat(history)
            history.append({"role": "assistant", "content": reply})
            records, errors = extract_and_validate(reply)
            # Retry once, forcing JSON, whenever the reply isn't a usable
            # records table — either unparseable, or (the common case) the
            # model re-asked its Phase 1 questions instead of answering, which
            # is syntactically valid JSON (so extract_array alone can't catch
            # it) but fails the records schema with e.g. "'table_name' is a
            # required property ... Additional properties ... 'category'".
            if records is None or errors:
                history.append({"role": "user", "content": FORCE_JSON_INSTRUCTION})
                reply = LLM_API_call.chat(history)
                records, errors = extract_and_validate(reply)
        # External LLM call: openai client raises assorted network/auth error types.
        except Exception as exc:  # noqa: BLE001
            return {"error": llm_error_message(exc)}

        if records is None:
            return {"error": "Le modèle n'a pas produit de tableau JSON exploitable."}
        if errors:
            msg = "Validation du schéma échouée :\n" + "\n".join(errors)
            return {"error": msg}

        # Cached on success only, so a failed run is retried for real.
        sess["results"][key] = records
        sess["records"] = records
        table = records_to_ui(records)
        return {"status": "ok", "normalized_table": table}

    return start_job(do_work)


@app.route("/api/export", methods=["POST"])
def export_table():
    """Step 4: download the validated table as CSV."""
    data = request.get_json(force=True) or {}
    session_id = data.get("session_id", "")
    sess = sessions.get(session_id)
    if not sess:
        return jsonify({"error": "Session introuvable"}), 404
    if sess["records"] is None:
        msg = "Tableau non encore produit — relancez le pipeline"
        return jsonify({"error": msg}), 409

    fmt = data.get("format", "csv")
    records = sess["records"]
    stem = Path(sess["file_name"]).stem

    if fmt == "csv":
        cols, rows = csv_cols_rows(records)
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(cols)
        w.writerows(rows)
        payload = io.BytesIO(("﻿" + buf.getvalue()).encode("utf-8"))
        return send_file(
            payload,
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"{stem}_normalise.csv",
        )

    if fmt == "rds":
        return jsonify({"error": "Export RDS pas encore disponible."}), 501

    return jsonify({"error": f"Format non supporté : {fmt}"}), 400


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_Q_RE = re.compile(r"^\s*(\d+)\.\s+(.+)$")
_KNOWN_CATEGORIES = {
    "champ et population",
    "indicateurs et hiérarchies",
    "variables de croisement et nomenclatures",
    "structure des tableaux",
}


def llm_error_message(exc: Exception) -> str:
    """Turn a chat() failure (missing key, unreachable endpoint, ...) into an
    actionable message instead of letting Flask 500 with an HTML page (which
    breaks the frontend's res.json() and shows as a generic connection error)."""
    name = type(exc).__name__
    if isinstance(exc, RuntimeError):
        return str(exc)
    if "Connection" in name or "Timeout" in name:
        return (
            f"Impossible de joindre le serveur LLM ({exc}). "
            "Cet endpoint (llm.lab.sspcloud.fr) n'est accessible que depuis le "
            "réseau SSP Cloud — vérifiez votre connexion/VPN, ou définissez "
            "LLM_BASE_URL vers un endpoint accessible."
        )
    if "Authentication" in name or "PermissionDenied" in name:
        return f"Authentification refusée par le serveur LLM : {exc}"
    return f"Erreur lors de l'appel au modèle ({name}) : {exc}"


def chat_with_retry(history, attempts=2):
    """Retry only on transient network/timeout errors — never on a bad
    (but successfully returned) reply; that's a 422 problem, not a retry one."""
    last_exc = None
    for i in range(attempts):
        try:
            return LLM_API_call.chat(history)
        # Inspects type(exc).__name__ below to decide retry vs re-raise.
        except Exception as exc:
            name = type(exc).__name__
            if "Connection" in name or "Timeout" in name:
                last_exc = exc
                continue
            raise
    raise last_exc


def extract_and_validate(reply: str):
    """(records, errors) for a Phase 2 reply — records is None if reply isn't
    even parseable JSON; errors is the schema-validation error list (empty on
    success). Centralised so both the first attempt and the forced retry use
    the exact same "is this a usable table" check."""
    records = extract_array(reply)
    if records is None:
        return None, []
    return records, validate(records)


def parse_questions(text: str) -> list:
    """Parse the LLM's Phase 1 JSON question array into dicts the UI expects."""
    raw = extract_array(text)
    if raw is None:
        return []

    questions = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        t = str(item.get("text", "")).strip()
        if not t:
            continue
        category = str(item.get("category", "")).strip()
        if category.lower() not in _KNOWN_CATEGORIES:
            category = "Général"
        ref_m = re.search(r"[Ff]euille\s+\S+|T\d+", t)
        questions.append({
            "id": str(len(questions) + 1),
            "text": t,
            "category": category,
            "ref": ref_m.group(0) if ref_m else category,
            "options": [],
        })
    return questions


def answers_fingerprint(answers_text: str) -> str:
    """Stable identity of one Phase 2 submission. Hashed rather than stored raw
    so the per-session cache stays small whatever the producer pastes into
    « informations complémentaires »."""
    return hashlib.sha256(answers_text.encode("utf-8")).hexdigest()


def format_answers(questions: list, answers: dict, extra_info: str = "") -> str:
    """Reconstruct the numbered answer text Phase 2 expects, plus any free-text
    context the producer added beyond the model's specific questions."""
    lines = []
    for q in questions:
        # `or ""` — clearing a textarea sends null for that question, and a bare
        # .strip() on it would 500 as an HTML page (which the frontend surfaces
        # as a misleading "impossible de joindre le serveur").
        ans = str(answers.get(str(q["id"])) or "").strip()
        if ans:
            lines.append(f"{q['id']}. {ans}")
    extra = (extra_info or "").strip()
    if extra:
        if lines:
            lines.append("")
        lines.append("Informations complémentaires du producteur :")
        lines.append(extra)
    return "\n".join(lines)


def records_to_ui(records: list) -> list:
    """Flatten nested spanning_variables into a display string for the Table."""
    result = []
    for r in records:
        parts = []
        for sv in (r.get("spanning_variables") or []):
            code = sv.get("code", "NA")
            hrc = sv.get("hrc", "NA")
            parts.append(code if hrc == "NA" else f"{code} ({hrc})")
        result.append({
            "table_name": r.get("table_name", "NA"),
            "field": r.get("field", "NA"),
            "hrc_field": r.get("hrc_field", "NA"),
            "indicator": r.get("indicator", "NA"),
            "hrc_indicator": r.get("hrc_indicator", "NA"),
            "spanning": " · ".join(parts) if parts else "NA",
        })
    return result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
