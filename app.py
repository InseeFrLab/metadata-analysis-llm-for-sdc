#!/usr/bin/env python3
"""Flask server — serves the DSFR pipeline UI and drives the src/ LLM pipeline.

Run:
    python app.py
    # open http://127.0.0.1:5000/

Offline stub (no LLM key needed — replaces the src chat() with a saved reply):
    SDC_STUB_REPLY=path/to/saved_reply.txt python app.py
"""

import csv
import io
import os
import re
import sys
from pathlib import Path
from flask import Flask, jsonify, redirect, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from src import LLM_API_call
from src.data import read_file
from src.clean import _dataframe_to_rows, clean_sheet
from src.transform_input import wrap, to_markdown
from src.LLM_API_call import is_auto_continued, FORCE_JSON_INSTRUCTION
from src.extract_JSON_array import extract_array
from src.validate_json_output import validate
from src.transform_output import HEADER_BASE, _spanning_pairs, max_spanning

# Ensure the project root is importable (so `src` resolves) regardless of cwd.
_ROOT = Path(__file__).parent
sys.path.insert(0, str(_ROOT))

# ---------------------------------------------------------------------------
# Flask app — the frontend/ folder is the static root, so index.html's
# "../../styles.css" / "../../_ds_bundle.js" / "../../assets/…" resolve to the
# real files under frontend/.
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder=str(_ROOT / "frontend"), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
app.config["UPLOAD_FOLDER"] = _ROOT / "uploads" / "temp"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# System prompt driving the two-phase pipeline (read once at startup).
PROMPT = (_ROOT / "src" / "prompts" / "prompt_questions.md").read_text(encoding="utf-8")

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
#   "history":   list,       message history — required for Phase 2
#   "questions": list,       parsed question dicts ([] if auto_continued)
#   "records":   list|None,  validated records; None = Phase 2 not yet run
# }


# ---------------------------------------------------------------------------
# Pipeline glue (mirrors main.py, reusing the src/ primitives)
# ---------------------------------------------------------------------------

def serialize(filepath) -> str:
    """Workbook → cleaned Markdown (main.py steps I–III)."""
    data = read_file(str(filepath))
    cleaned_sheets = []
    for name, df in data.items():
        rows = clean_sheet(_dataframe_to_rows(df))
        if any(any(c for c in r) for r in rows):
            cleaned_sheets.append((name, rows))
    return to_markdown(cleaned_sheets, title=Path(filepath).name)


def _csv_cols_rows(records: list):
    """Flatten records to the verified 2n+5 column layout (main.py steps V–VI)."""
    n_span = max_spanning(records)
    cols = list(HEADER_BASE)
    for i in range(1, n_span + 1):
        cols += [f"spanning_{i}", f"hrc_spanning_{i}"]

    rows = []
    for rec in records:
        row = [rec["table_name"], rec["field"], rec["hrc_field"],
               rec["indicator"], rec["hrc_indicator"]]
        pairs = _spanning_pairs(rec)
        for i in range(n_span):
            code, hrc = pairs[i] if i < len(pairs) else ("NA", "NA")
            row += [code, hrc]
        rows.append(row)
    return cols, rows


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

    try:
        md = serialize(filepath)
    except Exception as exc:
        return jsonify({"error": f"Échec de la sérialisation : {exc}"}), 422

    history = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": wrap(md)},
    ]
    try:
        reply = LLM_API_call.chat(history)
        print("=== RAW REPLY ===\n", reply, "\n =============")
    except Exception as exc:
        return jsonify({"error": _llm_error_message(exc)}), 502
    history.append({"role": "assistant", "content": reply})

    # Phase 1 auto-continued: the model answered directly in JSON, no questions.
    if is_auto_continued(reply):
        records = extract_array(reply)
        if records is None:
            return jsonify({"error": "Réponse du modèle illisible (aucun tableau JSON)."}), 422
        errors = validate(records)
        if errors:
            return jsonify({"error": "Validation du schéma échouée :\n" + "\n".join(errors)}), 422
        sessions[session_id] = {
            "file_name": filename,
            "filepath": str(filepath),
            "markdown": md,
            "history": history,
            "questions": [],
            "records": records,
        }
        return jsonify({
            "session_id": session_id,
            "file_name": file.filename,
            "extracted_markdown": md,
            "questions": [],
            "records": _records_to_ui(records),
        })

    parsed = _parse_questions(reply)
    sessions[session_id] = {
        "file_name": filename,
        "filepath": str(filepath),
        "markdown": md,
        "history": history,
        "questions": parsed,
        "records": None,
    }
    return jsonify({
        "session_id": session_id,
        "file_name": file.filename,
        "extracted_markdown": md,
        "questions": parsed,
    })


@app.route("/api/answer", methods=["POST"])
def submit_answers():
    """Step 2: receive producer answers, run Phase 2, return validated table."""
    data = request.get_json(force=True) or {}
    session_id = data.get("session_id", "")
    sess = sessions.get(session_id)
    if not sess:
        return jsonify({"error": "Session introuvable"}), 404

    if sess["records"] is not None:
        return jsonify({"status": "ok", "normalized_table": _records_to_ui(sess["records"])})

    answers = data.get("answers", {})
    answers_text = _format_answers(sess["questions"], answers)

    # Phase 2 (main.py lines 57–70): apply answers, then force JSON if the model re-asks.
    history = sess["history"]
    history.append({"role": "user", "content": answers_text})
    try:
        reply = LLM_API_call.chat(history)
        history.append({"role": "assistant", "content": reply})
        if extract_array(reply) is None:
            history.append({"role": "user", "content": FORCE_JSON_INSTRUCTION})
            reply = LLM_API_call.chat(history)
            history.append({"role": "assistant", "content": reply})
    except Exception as exc:
        return jsonify({"error": _llm_error_message(exc)}), 502

    records = extract_array(reply)
    if records is None:
        return jsonify({"error": "Le modèle n'a pas produit de tableau JSON exploitable."}), 422
    errors = validate(records)
    if errors:
        return jsonify({"error": "Validation du schéma échouée :\n" + "\n".join(errors)}), 422

    sess["records"] = records
    return jsonify({"status": "ok", "normalized_table": _records_to_ui(records)})


@app.route("/api/export", methods=["POST"])
def export_table():
    """Step 4: download the validated table as CSV."""
    data = request.get_json(force=True) or {}
    session_id = data.get("session_id", "")
    sess = sessions.get(session_id)
    if not sess:
        return jsonify({"error": "Session introuvable"}), 404
    if sess["records"] is None:
        return jsonify({"error": "Tableau non encore produit — relancez le pipeline"}), 409

    fmt = data.get("format", "csv")
    records = sess["records"]
    stem = Path(sess["file_name"]).stem

    if fmt == "csv":
        cols, rows = _csv_cols_rows(records)
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


def _llm_error_message(exc: Exception) -> str:
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


def _parse_questions(text: str) -> list:
    """Parse the LLM's Phase 1 JSON question array into structured dicts the UI expects."""
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


def _format_answers(questions: list, answers: dict) -> str:
    """Reconstruct the numbered answer text Phase 2 expects."""
    lines = []
    for q in questions:
        ans = answers.get(str(q["id"]), "").strip()
        if ans:
            lines.append(f"{q['id']}. {ans}")
    return "\n".join(lines)


def _records_to_ui(records: list) -> list:
    """Flatten nested spanning_variables into a display string for the Table component."""
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
    app.run(debug=True, host="0.0.0.0", port=5000)
