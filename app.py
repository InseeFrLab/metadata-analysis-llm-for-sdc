#!/usr/bin/env python3
"""Flask server — serves the DSFR pipeline UI and coordinates with the LLM pipeline.

Run:
    python app.py
    # open http://127.0.0.1:5000/

Offline stub (no LLM key needed — replaces llm_client.chat with a saved reply):
    SDC_STUB_REPLY=path/to/saved_reply.txt python app.py
"""

import csv
import io
import os
import re
import sys
import tempfile
from pathlib import Path

from flask import Flask, jsonify, redirect, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from core import pipeline, transform_output

sys.path.insert(0, str(Path(__file__).parent))


# ---------------------------------------------------------------------------
# Flask app — project root is the static folder so index.html's
# "../../styles.css" resolves to /styles.css (the project-root file).
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).parent
app = Flask(__name__, static_folder=str(_ROOT), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
app.config["UPLOAD_FOLDER"] = _ROOT / "uploads" / "temp"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ---------------------------------------------------------------------------
# Offline stub — set SDC_STUB_REPLY to a saved LLM reply path to bypass the
# network call (useful for local testing without an API key).
# ---------------------------------------------------------------------------
_stub = os.environ.get("SDC_STUB_REPLY")
if _stub:
    from unittest.mock import patch
    from core import llm_client as _lc
    _reply_text = Path(_stub).read_text(encoding="utf-8")
    patch.object(_lc, "chat", return_value=_reply_text).start()

# ---------------------------------------------------------------------------
# In-memory session store
# ---------------------------------------------------------------------------
sessions: dict = {}
# sessions[session_id] = {
#   "file_name": str,        secure filename
#   "filepath":  str,        absolute temp path
#   "markdown":  str,        serialized Markdown
#   "history":   list,       Phase1Result.history — required for pipeline.answer()
#   "questions": list,       parsed question dicts ([] if auto_continued)
#   "records":   list|None,  validated records; None = Phase 2 not yet run
# }


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
    """Step 1: accept workbook, serialize it, call LLM Phase 1."""
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
        md = pipeline.serialize(filepath)
    except Exception as exc:
        return jsonify({"error": f"Échec de la sérialisation : {exc}"}), 422

    try:
        r = pipeline.start(md)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 502

    if r.auto_continued:
        sessions[session_id] = {
            "file_name": filename,
            "filepath": str(filepath),
            "markdown": md,
            "history": r.history,
            "questions": [],
            "records": r.records,
        }
        return jsonify({
            "session_id": session_id,
            "file_name": file.filename,
            "extracted_markdown": md,
            "questions": [],
            "records": _records_to_ui(r.records),
        })

    parsed = _parse_questions(r.questions)
    sessions[session_id] = {
        "file_name": filename,
        "filepath": str(filepath),
        "markdown": md,
        "history": r.history,
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

    try:
        records = pipeline.answer(sess["history"], answers_text)
    except (ValueError, RuntimeError) as exc:
        return jsonify({"error": str(exc)}), 422

    sess["records"] = records
    return jsonify({"status": "ok", "normalized_table": _records_to_ui(records)})


@app.route("/api/export", methods=["POST"])
def export_table():
    """Step 4: download the validated table as CSV or RDS."""
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
        cols = transform_output.header(records)
        rows = transform_output.csv_rows(records)
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
        try:
            tmp = Path(tempfile.mktemp(suffix=".rds"))
            transform_output.write_rds(records, tmp)
            return send_file(
                str(tmp),
                mimetype="application/octet-stream",
                as_attachment=True,
                download_name=f"{stem}_normalise.rds",
            )
        except ImportError:
            return jsonify({
                "error": (
                    "pyreadr et pandas ne sont pas installés. "
                    "Installez-les avec : pip install pyreadr pandas"
                )
            }), 501

    return jsonify({"error": f"Format non supporté : {fmt}"}), 400


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_CAT_RE = re.compile(r"^#+\s*\d+\.\s+(.+)$")
_Q_RE = re.compile(r"^\s*(\d+)\.\s+(.+)$")


def _parse_questions(text: str) -> list:
    """Parse the LLM's free-text question block into structured dicts the UI expects."""
    questions, category = [], "Général"
    for line in text.splitlines():
        line = line.strip()
        if m := _CAT_RE.match(line):
            category = m.group(1).strip()
            continue
        if m := _Q_RE.match(line):
            t = m.group(2).strip()
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
    """Reconstruct the numbered answer text pipeline.answer() expects."""
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
