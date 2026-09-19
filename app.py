"""
EPR Compliance Copilot - Server & API

Run with:
    .venv/bin/python app.py

Then open http://localhost:5000
"""

import os
import time
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

# Structured logging configuration (IMP-008)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("epr_copilot")

from rag.chain import ask, get_llm_status
from rag.calculator import get_target, get_annual_return_deadline, calculate_liability
from rag.knowledge_base import KNOWLEDGE_BASE

app = Flask(__name__)
# 64 KB request ceiling to prevent unbounded payload DOS attacks (IMP-003)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024


@app.route("/health")
def health():
    """Liveness & readiness probe endpoint (IMP-010)."""
    status = get_llm_status()
    return jsonify({
        "status": "ok",
        "kb_chunks": len(KNOWLEDGE_BASE),
        "is_live": status["is_live"],
        "provider": status["provider"],
    }), 200


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
    if len(question) < 3:
        return jsonify({"error": "question must be at least 3 characters"}), 400
    if len(question) > 1000:
        return jsonify({"error": "question must not exceed 1000 characters"}), 400

    start_t = time.time()
    result = ask(question)
    elapsed_ms = round((time.time() - start_t) * 1000, 1)

    logger.info(
        "POST /api/ask - question_len=%d citations=%d mode=%s latency=%.1fms",
        len(question),
        len(result.get("citations", [])),
        result.get("mode", "unknown"),
        elapsed_ms,
    )
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
    logger.info(
        "POST /api/calculate - pibo_type=%s fy=%s total_mt=%.1f",
        pibo_type,
        fiscal_year,
        result.get("total_introduced_packaging_mt", 0.0),
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
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug, port=port)
