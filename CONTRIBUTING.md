# Contributing to EPR Compliance Copilot

Thank you for your interest in contributing to **EPR Compliance Copilot**! We welcome contributions to expand statutory knowledge chunks, improve retrieval precision, refine calculation logic, and enhance the UI.

## Code of Conduct

Please be respectful, collaborative, and constructive when opening issues or submitting pull requests.

## How to Contribute

### 1. Setting Up the Development Environment
```bash
git clone https://github.com/<your-username>/epr-copilot.git
cd epr-copilot

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies including development tools
pip install -r requirements.txt pytest ruff mypy
```

### 2. Adding or Updating Knowledge Base Chunks
All statutory knowledge chunks live in `rag/knowledge_base.py`. Every chunk must include:
- `id`: Unique identifier (e.g. `kb023`).
- `title`: Concise statutory subject title.
- `citation`: Exact official gazette notification, rule, clause, or circular reference.
- `confidence`: One of `"verified"` (direct gazette text), `"reported"` (industry/CPCB guidance), or `"needs_verify"` (transitional/provisional).
- `text`: Verbatim or strictly grounded statutory prose.

### 3. Running the Test Suite
Before submitting any pull request, ensure all tests pass:
```bash
pytest tests/ -v
```

### 4. Submitting a Pull Request
1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature-name`.
3. Commit your changes: `git commit -m "feat: description of change"`.
4. Push to your branch: `git push origin feat/your-feature-name`.
5. Open a Pull Request with a clear description and any relevant CPCB circular references.
