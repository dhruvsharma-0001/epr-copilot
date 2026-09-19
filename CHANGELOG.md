# Changelog

All notable changes to the **EPR Compliance Copilot** will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-19 (Official v1 Release)

### Added
- **Official v1 Release**: Production-ready baseline with citation-grounded RAG, deterministic calculator, and multi-model routing.
- **Knowledge Base Expansion**: Added chunks `kb017` to `kb022` covering Single-Use Plastics (SUP) 19-item ban, 120-micron carry bag rule, Plastic Waste Processors (PWP) registration & digital credit generation, MSME brand owner turnover exemptions, CPCB vs SPCB jurisdictional criteria, end-of-life disposal channels (AFR/IRC SP:98), and Battery/E-Waste cross-compliance.
- **Static Asset Separation**: Extracted inline CSS into `static/css/app.css` and JavaScript into `static/js/app.js`.
- **Print / PDF Report Export**: Added dedicated print stylesheet (`@media print`) and UI button to print or save statutory compliance calculation audit reports directly to PDF.
- **Docker Support**: Added production multi-stage `Dockerfile` and `docker-compose.yml` with non-root execution and healthcheck probes.
- **Automated Test Suite**: Added 18 unit and integration tests across `tests/` (`test_calculator.py`, `test_knowledge_base.py`, `test_retriever.py`, `test_chain.py`, `test_api.py`).
- **CI/CD**: Added GitHub Actions workflow (`.github/workflows/ci.yml`) matrix-tested across Python 3.11 and 3.12.
- **Pre-commit Hooks**: Configured `.pre-commit-config.yaml` with `detect-secrets` and file integrity checks.
- **Health Endpoint**: Added `GET /health` probe for orchestration liveness monitoring.

### Changed
- **Groq Model Update**: Updated default Groq model from decommissioned `deepseek-r1-distill-llama-70b` to active `qwen/qwen3.8-27b`.
- **LangGraph Singleton**: Cached compiled graph and LLM instance to eliminate re-compilation per request.
- **Security Hardening**: Disabled debug mode in production, enforced 64 KB payload limits, and added question length bounds.
- **Calculator Sanitization**: Guarded against `NaN`, `Infinity`, negative numbers, and non-numeric inputs.

## [0.2.0] - 2026-09-18

### Added
- Multi-provider dynamic LLM routing (Groq, OpenRouter, Gemini, Anthropic, OpenAI).
- Interactive EPR liability and Environmental Compensation calculator.
- Tabbed interface with CPCB filing checklist and knowledge base viewer.

## [0.1.0] - 2026-09-15

### Added
- Initial prototype baseline with TF-IDF retrieval and mock mode generation.
