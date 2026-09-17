"""
EPR Compliance Copilot - Server & API

Run with:
    .venv/bin/python app.py

Then open http://localhost:5000
"""

import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

from rag.chain import ask, get_llm_status
from rag.calculator import get_target, get_annual_return_deadline, calculate_liability
from rag.knowledge_base import KNOWLEDGE_BASE

app = Flask(__name__)


@app.route("/")
def index():
    status = get_llm_status()
    return render_template(
        "index.html",
        live_mode=status["is_live"],
        provider_label=status["label"],
        kb_size=len(KNOWLEDGE_BASE),
    )


@app.route("/api/status")
def api_status():
    return jsonify(get_llm_status())


@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.get_json(force=True) or {}
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "question is required"}), 400
    result = ask(question)
    return jsonify(result)


@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json(force=True) or {}
    pibo_type = data.get("pibo_type", "Brand Owner")
    fiscal_year = data.get("fiscal_year", "2026-27")
    tonnages = data.get("tonnages", {})

    result = calculate_liability(
        pibo_type=pibo_type,
        fiscal_year=fiscal_year,
        tonnages=tonnages,
    )
    return jsonify(result)


@app.route("/api/target/<fiscal_year>")
def api_target(fiscal_year):
    return jsonify(get_target(fiscal_year))


@app.route("/api/deadline")
def api_deadline():
    return jsonify(get_annual_return_deadline())


@app.route("/api/kb")
def api_kb():
    """Expose the knowledge base so users can inspect exact citations and confidence."""
    return jsonify([
        {k: v for k, v in chunk.items() if k != "text"} | {"text_preview": chunk["text"][:140] + "..."}
        for chunk in KNOWLEDGE_BASE
    ])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
