# EPR Compliance Copilot

A citation-grounded compliance copilot and obligation calculation engine for India's plastic waste Extended Producer Responsibility (EPR) regulations (Schedule II of the Plastic Waste Management Rules, 2016 and subsequent MoEFCC & CPCB amendments).

Built on **Flask + LangChain + LangGraph**, featuring:
- **Statutory Legal Q&A Assistant**: Grounded in official CPCB notifications, with citation badges and confidence ratings.
- **Multi-Model LLM Routing**: Supports **Google Gemini** (recommended), **Anthropic Claude**, and **OpenAI**, with automated fallback to zero-dependency **Mock Mode**.
- **Interactive EPR Liability & Penalty Calculator**: Computes Category I–IV statutory recycling targets, mandatory recycled-content requirements, certificate procurement budgets, and Environmental Compensation (EC) penalty exposures with a 3-year refund schedule.
- **CPCB Portal Registration Readiness Checklist**: Practical compliance guide for Producers, Importers, Brand Owners (PIBOs), and Sellers.

---

## Architecture

```
Browser  -->  Flask (app.py)  -->  LangGraph pipeline (rag/chain.py)
                                       │
                                       ├─► retrieve_node: TF-IDF retriever
                                       │   (rag/retriever.py) over rag/knowledge_base.py
                                       │
                                       └─► generate_node:
                                           ├── Live Mode: Google Gemini (gemini-2.5-flash)
                                           ├── Live Mode: Anthropic Claude (claude-3-5-sonnet)
                                           ├── Live Mode: OpenAI (gpt-4o)
                                           └── Mock Mode: (zero API key fallback)
```

- **Retrieval**: `langchain_community.retrievers.TFIDFRetriever` over statutory knowledge chunks with exact legal clause citations.
- **Generation**: Strict system prompt enforcing zero hallucinations, explicit citation tags (e.g. `[kb004]`), and distinction between verified gazette rules vs reported market estimates.
- **Deterministic Calculator** (`rag/calculator.py`): Full mathematical computation engine covering Category I (Rigid), Category II (Flexible), Category III (Multi-layered MLP), and Category IV (Compostable) obligations, market certificate prices, and Section 15 EPA 1986 penalty exposures.

---

## Quickstart

### 1. Setup Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key (Optional for Live Mode)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your preferred key:
```ini
# Option A: Google Gemini (Recommended)
GEMINI_API_KEY=your_gemini_api_key

# Option B: Anthropic Claude
# ANTHROPIC_API_KEY=your_anthropic_api_key

# Option C: OpenAI
# OPENAI_API_KEY=your_openai_api_key
```
*(If no API key is provided, the copilot runs automatically in **Mock Mode**, displaying raw retrieved legal chunks with zero setup).*

### 3. Start the Application
```bash
.venv/bin/python app.py
```
Open **http://localhost:5000** in your browser.

---

## Project Structure

```
epr-copilot/
├── app.py                  # Flask web server & REST API endpoints
├── rag/
│   ├── __init__.py
│   ├── knowledge_base.py   # Ground-truth statutory CPCB knowledge chunks
│   ├── retriever.py        # Keyword/TF-IDF retrieval engine
│   ├── chain.py            # LangGraph multi-model RAG workflow
│   └── calculator.py       # Deterministic EPR liability & penalty engine
├── templates/
│   └── index.html          # Polished tabbed UI (Q&A, Calculator, Checklist)
├── .env.example            # Environment variable template
├── .gitignore              # Ignores .venv, .env, __pycache__
├── requirements.txt        # Frozen dependencies
└── README.md               # Documentation & technical guide
```

---

## API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/status` | `GET` | Returns active LLM provider status and mode |
| `/api/ask` | `POST` | Legal Q&A query grounded in statutory citations |
| `/api/calculate` | `POST` | Computes Category I–IV targets, certificate budget, and penalty liability |
| `/api/target/<fy>` | `GET` | Returns statutory recycling & recycled content target percentages |
| `/api/deadline` | `GET` | Returns annual return statutory deadlines and typical extension windows |
| `/api/kb` | `GET` | Exposes all knowledge chunks with citations and confidence levels |
