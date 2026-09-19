# Future Upgrades & Roadmap — EPR Compliance Copilot

This document outlines planned improvements, architectural upgrades, and enterprise features for upcoming releases of **EPR Compliance Copilot**, following the official **v1.0.0** release.

---

## 📍 Current Release: v1.0.0 (Baseline Foundation)

- ✅ **Statutory Legal Q&A Assistant**: Grounded in 22 official CPCB/MoEFCC knowledge chunks with citations (`[kb001]` to `[kb022]`).
- ✅ **Deterministic Liability Calculator**: Accurate Category I–IV recycling targets, recycled content mandates, certificate costs, and 3-year EC penalty refund schedules.
- ✅ **Multi-Model LLM Routing**: Auto-routing across Groq (`qwen/qwen3.8-27b`), OpenRouter (`deepseek/deepseek-r1:free`), Gemini (`gemini-2.5-flash`), Claude, and OpenAI with zero-cost Mock Mode.
- ✅ **Production Hardening**: 64 KB request ceiling, `NaN`/`Inf` numerical sanitization, thread-safe LangGraph singleton caching.
- ✅ **Frontend & UX**: Clean separated CSS/JS, print-ready PDF audit reports, interactive CPCB filing checklist.
- ✅ **DevOps & Testing**: 18 automated unit and integration tests, Docker & Docker Compose setup, GitHub Actions CI matrix, and `/health` probe.

---

## 🚀 Upcoming Releases & Future Upgrades

### 📦 Milestone v1.1 — Hybrid Retrieval & CPCB Form VII Generator
*Target: Q4 2026*

1. **Hybrid Retrieval (Dense Embeddings + BM25 with Reciprocal Rank Fusion)**:
   - Combine dense vector embeddings (`chromadb` + `sentence-transformers/all-MiniLM-L6-v2`) with sparse keyword matching (`rank_bm25.BM25Okapi`).
   - Improves semantic recall on colloquial queries (e.g. *"What happens if I miss my filing deadline?"*).
2. **CPCB Form VII Annual Return Auto-Populator**:
   - Generate ready-to-copy JSON and Excel files matching CPCB's official annual return template (Form VII).
   - Pre-fills Category I–IV tonnages, target percentages, and recycler credit transaction numbers.
3. **Automated Deadline Notification Webhooks**:
   - Integration with Slack, Microsoft Teams, and email to send automated countdown alerts 60, 30, 15, and 7 days prior to statutory deadlines (June 30).

---

### 📦 Milestone v1.2 — Multi-Modal Invoice & BOM Parser
*Target: Q1 2027*

1. **PDF & Excel Packaging BOM (Bill of Materials) Parser**:
   - Allow Brand Owners and Importers to upload supplier invoices, packaging specifications, or ERP exports.
   - Use vision/OCR and structured extraction to automatically classify packaging materials into Categories I, II, III, and IV.
   - Eliminates manual data entry into the liability calculator.
2. **QR Code & Barcode Compliance Validator**:
   - Upload a packaging artwork file (PDF/PNG) to verify Rule 11 labeling compliance.
   - Checks presence of CPCB EPR registration number, polymer recycling symbol (1-7), and scannable QR code.

---

### 📦 Milestone v1.3 — Real-Time Streaming & Semantic Caching
*Target: Q2 2027*

1. **Server-Sent Events (SSE) Streaming**:
   - Add `/api/ask/stream` endpoint for token-by-token streaming.
   - Reduces Time-to-First-Token (TTFT) to $< 800$ms on reasoning models (e.g. DeepSeek R1, Qwen).
2. **Semantic FAQ Caching (Redis / In-Memory)**:
   - Cache frequent compliance queries (similarity threshold $> 0.96$).
   - Returns instant responses ($< 15$ms) with zero token consumption and zero API cost.

---

### 📦 Milestone v2.0 — Autonomous Agentic Copilot
*Target: Q3 2027*

1. **Unified Natural Language Tool-Calling Agent**:
   - Convert the copilot into an autonomous agent where the LLM can call `calculate_liability` and `lookup_deadline` as tools during a conversation.
   - Example prompt: *"I manufactured 150 MT of PET bottles and 80 MT of plastic pouches in 2026-27, what are my targets and what does CPCB require for labeling?"*  
     The agent computes exact numbers and cites relevant legal rules in a single turn.
2. **Corrective RAG (CRAG) & Active Self-Correction**:
   - Evaluate retrieved documents; if confidence is low, reformulate queries with statutory acronym expansion (`PIBO`, `PWM`, `PWP`, `SUP`).
   - If information does not exist in statutory gazettes, explicitly inform the user rather than guessing.
3. **Multi-Lingual Localization for Indian MSMEs**:
   - Native query and answer support in **Hindi (हिंदी)**, **Gujarati (ગુજરાતી)**, **Marathi (मराठी)**, and **Tamil (தமிழ்)** to serve manufacturing clusters in Gujarat, Maharashtra, and Tamil Nadu.

---

### 🏢 Enterprise Edition — Multi-Tenant Compliance Suite

1. **Multi-Tenant Account Management**:
   - Organization-level dashboards for corporate groups with multiple brand subsidiaries.
   - Role-based access control (Admin, Compliance Manager, Auditor).
2. **SPCB Inspection & Audit Defense Pack**:
   - One-click generation of comprehensive audit binders for State Pollution Control Board (SPCB) physical facility inspections.
   - Includes verified recycler certificates, weighbridge receipts, and statutory calculation sheets.
3. **CPCB Portal Change Watcher**:
   - Automated crawler checking [cpcb.nic.in/epr](https://cpcb.nic.in/epr/) weekly for new circulars, amendments, and deadline extensions, alerting compliance officers to regulatory changes.

---

*To propose a new feature or contribute to an upcoming milestone, please see [`CONTRIBUTING.md`](CONTRIBUTING.md) or open an issue on GitHub.*
