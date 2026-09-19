# EPR Compliance Copilot — Judge's Verdict & Improvement Ledger

> **Judge:** Antigravity AI · **Date:** Sep 19, 2026
> **Scope:** Full codebase audit — architecture, retrieval, generation, UI, security, data integrity, testing, DevOps.
> **Version audited:** commit `12046f6` + uncommitted changes to `rag/chain.py`, `README.md`, `.env.example`, `requirements.txt`.

---

## 1. Overall Scorecard

| Dimension | Score | Verdict |
|---|---|---|
| Architecture & Design | **7 / 10** | Clean foundation, but graph is rebuilt on every request |
| Knowledge Base Quality | **6 / 10** | Richer than prototype, but 16 chunks is too thin for real coverage |
| Retrieval Quality | **4 / 10** | TF-IDF is keyword-only — will miss paraphrased queries |
| LLM Integration | **8 / 10** | Multi-provider routing is excellent; prompt is well-designed |
| Calculator Accuracy | **7 / 10** | Good structure, but EC rate is a floor estimate, not a formula |
| Frontend / UX | **7 / 10** | Modern UI, but no loading skeleton, no error recovery, no PDF export |
| Security & Safety | **3 / 10** | No auth, no rate limiting, no input sanitisation, debug mode in prod |
| Testing | **1 / 10** | Zero test files, no CI, no quality gate |
| Dependency Hygiene | **5 / 10** | `requirements.txt` is a full frozen dump — not pinned properly |
| DevOps / Deployment | **2 / 10** | Flask dev server, no Gunicorn, no Docker, no health endpoint |

**Overall: 5.0 / 10 — "Good proof-of-concept, not production-ready"**

---

## 2. Critical Bugs & Defects Found

### BUG-01 · LangGraph graph is rebuilt on every `/api/ask` call
**File:** [`rag/chain.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/chain.py#L247-L266) — `build_graph()` called inside `ask()`
**Impact:** TF-IDF vectoriser is re-fitted from scratch on every single HTTP request. At 16 chunks it's imperceptible; at 500 chunks this will make every request take 3–5s.
**Fix:** Cache the compiled graph at module level (singleton).

### BUG-02 · `get_llm_status()` calls `get_active_llm()` which instantiates the full LLM object
**File:** [`rag/chain.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/chain.py#L190-L198)
**Impact:** Every page load (`/`) triggers a full LLM class init just to render the badge label. Wasted startup latency.
**Fix:** Cache the provider detection result or use a lightweight key-only check for the status call.

### BUG-03 · `debug=True` is hardcoded in `app.run()`
**File:** [`app.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/app.py#L84)
**Impact:** Flask debug mode exposes an interactive debugger on error pages. If this is ever exposed to a network (even accidentally), it is a remote code execution vulnerability.
**Fix:** Read from env: `app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")`.

### BUG-04 · No input validation or length limiting on `/api/ask`
**File:** [`app.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/app.py#L39-L46)
**Impact:** A user can send a 1MB JSON body. Flask will load it all into memory before the route even runs.
**Fix:** Add `MAX_CONTENT_LENGTH` to Flask config and validate question length.

### BUG-05 · Calculator tonnage inputs accept NaN/Inf from JSON
**File:** [`rag/calculator.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/calculator.py#L130) — `float(tonnages.get(cat_key, 0.0) or 0.0)`
**Impact:** `float("nan")` and `float("inf")` pass the cast silently and produce `nan`/`inf` in all output fields. The JSON response returns `NaN`, which is invalid JSON and breaks the browser calculator.
**Fix:** Clamp to `max(0.0, min(float(value), 1_000_000))` and reject negative values with a proper helper.

### BUG-06 · `static/` directory is completely empty
**File:** [`/static/`](file:///Users/dhruvsharma/Desktop/epr-copilot/static/)
**Impact:** All 536 lines of CSS and JS are inlined in a single HTML file. Prevents caching, CDN offloading, and makes the template very hard to maintain.

### BUG-07 · `.env` exists as a real file (was created by the agent) and could be committed
**Impact:** If a key is added to `.env` and `git add .` is run carelessly, credentials enter git history.
**Fix:** Verify `.env` stays in `.gitignore` and add a pre-commit `detect-secrets` hook.

---

## 3. Improvement Items — Numbered & Prioritised

> Items follow the pattern: `IMP-NNN · Title · Category · Priority`
> Priority: 🔴 Critical · 🟠 High · 🟡 Medium · 🟢 Low / Future

---

### IMP-001 · Fix Debug Mode in Production — Security
🔴 **Critical** · File: [`app.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/app.py#L84)

Remove `debug=True` hardcode. Read from environment:
```python
app.run(
    debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    port=int(os.environ.get("PORT", 5000))
)
```

---

### IMP-002 · Cache the LangGraph Compiled Graph as a Singleton — Performance
🔴 **Critical** · File: [`rag/chain.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/chain.py#L269-L272)

Move `build_graph()` to a module-level cached singleton so TF-IDF is fitted only once per process, not once per HTTP request:
```python
_GRAPH_CACHE: dict = {}
def get_graph(k: int = 4):
    if k not in _GRAPH_CACHE:
        _GRAPH_CACHE[k] = build_graph(k=k)
    return _GRAPH_CACHE[k]
```
Then in `ask()`: replace `build_graph(k=k)` with `get_graph(k=k)`.

---

### IMP-003 · Add Input Validation & Rate Limiting — Security
🔴 **Critical** · File: [`app.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/app.py)

Three layers of protection:
1. `app.config["MAX_CONTENT_LENGTH"] = 64 * 1024`  — 64 KB hard limit on all requests
2. Validate `len(question) <= 1000` before calling `ask()`
3. Install `flask-limiter` and cap `/api/ask` at `20/minute` per IP

---

### IMP-004 · Fix Calculator NaN/Infinity/Negative Input Handling — Data Integrity
🔴 **Critical** · File: [`rag/calculator.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/calculator.py#L130)

Add a sanitising helper used for every tonnage field:
```python
def _safe_tonnage(val, max_mt: float = 1_000_000.0) -> float:
    try:
        v = float(val)
        if not (0.0 <= v <= max_mt) or v != v:  # v != v catches NaN
            return 0.0
        return v
    except (TypeError, ValueError):
        return 0.0
```

---

### IMP-005 · Replace TF-IDF with Hybrid Search (BM25 + Embeddings) — Retrieval Quality
🟠 **High** · File: [`rag/retriever.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/retriever.py)

TF-IDF completely fails on paraphrased questions. *"How do I get compliant?"* returns zero useful chunks.

**Plan:**
1. Add `chromadb`, `sentence-transformers`, `rank-bm25`
2. Local embedding model: `sentence-transformers/all-MiniLM-L6-v2` (free, runs offline)
3. Persist Chroma DB in `./chroma_store/`
4. Combine with `BM25Retriever` using LangChain's `EnsembleRetriever(weights=[0.6, 0.4])`
5. Keep TF-IDF as fallback if sentence-transformers not installed

---

### IMP-006 · Add a Full Test Suite — Testing
🟠 **High** · New directory: `tests/`

Zero tests is the single biggest quality risk in the entire codebase.

**Minimum structure:**
```
tests/
  __init__.py
  test_calculator.py      # parametrised: tonnage inputs → verify targets, penalty exposure
  test_retriever.py       # golden Q&A: known queries → verify chunk IDs retrieved
  test_chain.py           # mock LLM → verify SYSTEM_PROMPT format and mock mode output
  test_api.py             # Flask test_client → all endpoints, bad inputs, error codes
  test_knowledge_base.py  # verify every chunk has: id, title, text, citation, confidence
```
Run: `pytest tests/ -q --tb=short`

---

### IMP-007 · Add CI/CD Pipeline — DevOps
🟠 **High** · New file: `.github/workflows/ci.yml`

Block broken code from entering `main`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt pytest
      - run: pytest tests/ -q
```

---

### IMP-008 · Replace `print()` with Structured Logging — Observability
🟠 **High** · Files: [`app.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/app.py), [`rag/chain.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/chain.py)

Every LLM call should emit a structured log entry with: provider, model, question_len, retrieval_ms, generation_ms, citation_count. Never log the raw question text (PII risk).
```python
import logging, time
logger = logging.getLogger("epr_copilot")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
```

---

### IMP-009 · Extract CSS/JS into Static Files — Maintainability
🟡 **Medium** · New files: [`static/app.css`](file:///Users/dhruvsharma/Desktop/epr-copilot/static/), [`static/app.js`](file:///Users/dhruvsharma/Desktop/epr-copilot/static/)

The 536-line [`index.html`](file:///Users/dhruvsharma/Desktop/epr-copilot/templates/index.html) contains ~180 lines of CSS and ~170 lines of JavaScript inline. Split into separate static files and link via `{{ url_for('static', filename='app.css') }}` for browser caching and easier maintenance.

---

### IMP-010 · Add `/health` Endpoint — DevOps / Monitoring
🟡 **Medium** · File: [`app.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/app.py)

```python
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "kb_chunks": len(KNOWLEDGE_BASE),
        "provider": get_llm_status()["provider"],
    }), 200
```
Required by Kubernetes probes, uptime monitors, and load balancers.

---

### IMP-011 · Expand Knowledge Base from 16 to 50+ Statutory Chunks — Domain Coverage
🟡 **Medium** · File: [`rag/knowledge_base.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/knowledge_base.py)

Current 16 chunks cover ~30% of actual EPR scope. Missing areas:
- E-commerce marketplace obligations (Amazon, Flipkart specific CPCB rules)
- Battery Waste Management Rules 2022 (separate from plastics EPR)
- EPR credit trading mechanics: auction rules, transfer, verification
- CPCB SOP for annual return filing (Form VII step-by-step)
- State-specific SPCB contact details and CTO validity differences (Maharashtra, Karnataka, Delhi, TN, Gujarat)
- CPCB blacklisting process and appeal procedure
- Waste-to-energy co-processing rules for Cat II/III end-of-life
- Plastic Waste Processors (PWP) registration requirements

---

### IMP-012 · Add Conversation Session History — UX
🟡 **Medium** · Files: [`app.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/app.py), [`templates/index.html`](file:///Users/dhruvsharma/Desktop/epr-copilot/templates/index.html)

Each request is currently stateless. Add lightweight session history via a UUID cookie + in-memory dict (or SQLite for persistence), so follow-up questions work:
- *Q1: "What is Category II?"* → *Q2: "What are its recycling targets?"* — Q2 needs Q1's context.
Pass last 3 Q&A pairs in the LLM prompt as `conversation_history`.

---

### IMP-013 · Add PDF Compliance Report Export — UX
🟡 **Medium** · Files: [`app.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/app.py), [`rag/calculator.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/calculator.py)

Auditors and compliance officers need printable reports. Add `/api/export/pdf` using `reportlab` or `weasyprint` that produces:
- Company name (input field), fiscal year, PIBO type
- Category-wise obligation table with all targets
- EC penalty exposure and refund schedule
- Citation list from the last Q&A session
- Prominent legal disclaimer and "not a substitute for professional advice" footer

---

### IMP-014 · Migrate to `pyproject.toml` for Dependency Management — Hygiene
🟡 **Medium** · New file: `pyproject.toml`

Replace the 86-line full frozen `requirements.txt` with:
- `pyproject.toml` listing only direct dependencies with version ranges (`>=`)
- `requirements.lock` generated by `pip-compile` for exact reproducible builds
- `requirements-dev.txt` for dev-only: `pytest`, `ruff`, `mypy`, `detect-secrets`

---

### IMP-015 · Add Pre-commit Hooks — Security & Code Quality
🟡 **Medium** · New file: `.pre-commit-config.yaml`

Block bad commits before they reach the repo:
- `detect-secrets` — blocks API keys (most important)
- `ruff --fix` — auto-format and lint
- `mypy rag/ app.py` — type safety
- Custom hook: ensure `.env` is never staged

---

### IMP-016 · Add Dockerfile + docker-compose for Production — DevOps
🟡 **Medium** · New files: `Dockerfile`, `docker-compose.yml`

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "--timeout=60", "app:app"]
```

---

### IMP-017 · Add Query Intent Classifier — UX Intelligence
🟡 **Medium** · File: [`rag/chain.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/chain.py)

Add a lightweight regex/keyword intent detection layer before RAG:
- `"deadline" | "due date" | "file by"` → return `get_annual_return_deadline()` directly
- `"target" | "how much" | "percentage" | "tonnes"` + numbers → route to `calculate_liability()`
- Everything else → full RAG pipeline

Eliminates the awkward tab separation in the UI — one input box handles all query types.

---

### IMP-018 · Confidence-Weighted Re-ranking of Retrieved Chunks — Retrieval Quality
🟡 **Medium** · File: [`rag/retriever.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/retriever.py)

Post-retrieval: down-score chunks tagged `needs_verify` by 30% so the primary answer is always grounded in `verified` statutory text. `reported` chunks come second, `needs_verify` last.

---

### IMP-019 · Document Upload — BOM / Invoice Auto-Parser — Feature
🟢 **Future** · New: `rag/parser.py`, new endpoint `/api/upload`

Allow PIBOs to upload supplier invoices or packaging BOMs as PDF/Excel and auto-extract category weights to pre-fill the calculator. Use `pdfplumber` + `openpyxl`.

---

### IMP-020 · Automated Deadline Reminder System — Feature
🟢 **Future** · New: `reminders/scheduler.py`

Background APScheduler (or Celery + Redis) that emails/WhatsApps 60/30/14/7 days before statutory filing deadlines based on a registered PIBO profile (SQLite). Generates compliance urgency awareness passively.

---

### IMP-021 · Multi-language Support (Hindi, Tamil, Gujarati) — Accessibility
🟢 **Future** · Files: [`rag/chain.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/chain.py), [`templates/index.html`](file:///Users/dhruvsharma/Desktop/epr-copilot/templates/index.html)

Add `language` parameter to `/api/ask` with values `"en"`, `"hi"`, `"ta"`, `"gu"`. Inject `"Respond in {language_name}"` into system prompt. Add a language selector pill in the UI.

---

### IMP-022 · State-Specific SPCB Guidance Chunks — Domain Coverage
🟢 **Future** · File: [`rag/knowledge_base.py`](file:///Users/dhruvsharma/Desktop/epr-copilot/rag/knowledge_base.py)

Add `"region"` metadata field and chunks specific to: Maharashtra, Karnataka, Delhi NCT, Tamil Nadu, Gujarat — covering SPCB portal URLs, CTO validity, and state-level enforcement precedents. Filter retrieval by `region` param in `/api/ask`.

---

### IMP-023 · LangSmith Tracing + RAGAS Evaluation Pipeline — Quality
🟢 **Future** · New: `eval/`

- Enable `LANGCHAIN_TRACING_V2=true` to log every retrieval + generation pair to LangSmith
- Build `eval/run_eval.py` using `ragas` metrics: Context Recall, Faithfulness, Answer Relevancy
- Maintain a `eval/golden_qa.json` test set reviewed by domain expert
- Run eval on every KB update (blocks merge if scores drop)

---

### IMP-024 · CPCB Portal Change Watcher (Web Scraper Notifier) — Data Freshness
🟢 **Future** · New: `tools/cpcb_watcher.py`

Weekly cron job that scrapes [cpcb.nic.in/epr](https://cpcb.nic.in/epr/) for new PDF circulars, diffs against a known-list, and sends a Slack/email alert: *"New CPCB notification — knowledge base may need update."*

---

### IMP-025 · Add `CHANGELOG.md` & Semantic Versioning — Project Management
🟢 **Future** · New file: `CHANGELOG.md`

Track every breaking change to knowledge base (statutory amendments), API shape changes, and model upgrades in standard [Keep a Changelog](https://keepachangelog.com/) format. Git-tag releases as `v0.1.0`, `v0.2.0` etc.

---

## 4. Recommended Sprint Execution Order

```
Sprint 1 — Make it Safe (Week 1)
  IMP-001  Fix debug mode
  IMP-003  Input validation & rate limiting
  IMP-004  Fix NaN/Infinity in calculator
  IMP-002  Cache LangGraph singleton
  IMP-015  Pre-commit hooks (detect-secrets first)

Sprint 2 — Make it Testable (Week 2)
  IMP-006  Full test suite (pytest)
  IMP-007  CI/CD GitHub Actions
  IMP-010  /health endpoint
  IMP-008  Structured logging

Sprint 3 — Make it Smarter (Week 3–4)
  IMP-005  Hybrid retrieval (Chroma + BM25)
  IMP-011  Expand KB to 50+ statutory chunks
  IMP-018  Confidence-weighted re-ranking
  IMP-017  Query intent classifier
  IMP-023  LangSmith + RAGAS eval pipeline

Sprint 4 — Make it Shippable (Week 5–6)
  IMP-009  Extract CSS/JS to static files
  IMP-013  PDF compliance report export
  IMP-014  pyproject.toml dependency management
  IMP-016  Dockerfile + docker-compose
  IMP-025  CHANGELOG.md + semantic versioning

Sprint 5 — Make it a Product (Month 2–3)
  IMP-012  Conversation session history
  IMP-019  Document upload / BOM parser
  IMP-020  Automated deadline reminders
  IMP-022  State-specific SPCB guidance
  IMP-021  Multi-language support (Hindi, Tamil, Gujarati)
  IMP-024  CPCB portal change notifier
```

---

## 5. What's Already Good — Strengths to Preserve

| Strength | Why It Matters |
|---|---|
| Multi-provider LLM routing with graceful fallback | Zero vendor lock-in. Model goes down → next one picks up automatically |
| Hallucination-control system prompt (cite-only, never-invent) | Single most important design decision for any compliance assistant |
| Deterministic calculator using lookup tables | Never lets LLM invent a compliance percentage. Architecturally sound |
| `/api/kb` transparency endpoint | Rare, valuable — users can inspect exactly what the system knows |
| Mock mode (zero API cost) | Enables KB quality validation without spending a single token |
| Confidence tags (`verified` / `reported` / `needs_verify`) | Right epistemic honesty pattern for legal content |
| `.env.example` with free model links and model IDs commented | Genuinely useful for contributors; lowers onboarding friction |
| `static/` directory pre-created | Ready to receive CSS/JS in IMP-009 without refactoring |

---

## 6. Non-Negotiable Before Any Real User Touches This

1. **Domain expert sign-off** — Every KB chunk must be reviewed by a CPCB-empanelled EPR consultant or environmental lawyer. Current text is researcher-quality secondary-source paraphrasing.
2. **Security hardening** — `IMP-001`, `IMP-003`, `IMP-004` before any public-facing URL.
3. **Test suite** — `IMP-006` before any new feature merge. No exceptions.
4. **Unbypassable disclaimer** — The current disclaimer is a UI banner that can be ignored. For a compliance assistant, every PDF export and every API response must include the full disclaimer permanently.

---

*This is the living improvement ledger. When an item is completed, move it below into the `## Completed` section with the PR/commit reference and date.*

## Completed

<!-- Move finished items here, e.g.: -->
<!-- - **IMP-001** · Fixed debug mode — PR #3 · Sep 20, 2026 -->
