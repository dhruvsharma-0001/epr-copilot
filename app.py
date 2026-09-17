"""
EPR Compliance Copilot -- prototype

Run with:
    python3 app.py

Then open http://localhost:5000

Set ANTHROPIC_API_KEY in your environment (or a .env file) to switch the
assistant from mock mode (raw retrieved chunks) to live mode (Claude-
generated, cited answers). See README.md.
"""

import os
from flask import Flask, request, jsonify, render_template

from dotenv import load_dotenv
load_dotenv()

from rag.chain import ask
from rag.calculator import get_target, get_annual_return_deadline
from rag.knowledge_base import KNOWLEDGE_BASE

app = Flask(__name__)


@app.route("/")
def index():
    live_mode = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return render_template("index.html", live_mode=live_mode, kb_size=len(KNOWLEDGE_BASE))


@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.get_json(force=True)
    question = (data or {}).get("question", "").strip()
    if not question:
        return jsonify({"error": "question is required"}), 400
    result = ask(question)
    return jsonify(result)


@app.route("/api/target/<fiscal_year>")
def api_target(fiscal_year):
    return jsonify(get_target(fiscal_year))


@app.route("/api/deadline")
def api_deadline():
    return jsonify(get_annual_return_deadline())


@app.route("/api/kb")
def api_kb():
    """Expose the knowledge base itself so you can see exactly what the
    assistant can and can't answer from -- transparency over the retrieval
    layer is the whole point at prototype stage."""
    return jsonify([
        {k: v for k, v in chunk.items() if k != "text"} | {"text_preview": chunk["text"][:120] + "..."}
        for chunk in KNOWLEDGE_BASE
    ])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
