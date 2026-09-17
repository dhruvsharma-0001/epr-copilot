# EPR Compliance Copilot -- Prototype

A working RAG prototype for a plastic-waste EPR compliance assistant, built on
Flask + LangChain + LangGraph. This is Phase 3 (and a slice of Phase 4) of the
build plan: a citation-grounded Q&A assistant over a small EPR knowledge base,
plus two deterministic lookup tools (deadline, recycling target).

## Read this before anything else

**The knowledge base (`rag/knowledge_base.py`) is built from secondary
reporting, not verified primary legal text.** It has NOT been reviewed by an
environmental compliance professional. Every chunk is tagged `"reported"` or
`"needs_verify"` -- the app surfaces that flag to the user, it does not hide
it. Do not use this to make a real compliance decision. Do not sell access to
this exact knowledge base to anyone. This exists to prove the architecture
works, so you can then do the real work of Phase 0 (get a domain expert) and
Phase 2 (source verified primary text) from the build plan.

## Architecture

```
Browser  -->  Flask (app.py)  -->  LangGraph pipeline (rag/chain.py)
                                       |
                                       +--> retrieve_node: TF-IDF retriever
                                       |    (rag/retriever.py) over
                                       |    rag/knowledge_base.py
                                       |
                                       +--> generate_node: mock (no key)
                                            or live (ChatAnthropic, if
                                            ANTHROPIC_API_KEY is set)
```

- **Retrieval**: `langchain_community.retrievers.TFIDFRetriever` -- pure
  scikit-learn TF-IDF, no embedding model to download, fully transparent.
  Swap for an embeddings-based retriever (Chroma/FAISS + OpenAI or Voyage
  embeddings) once the knowledge base grows past a few hundred chunks --
  TF-IDF only matches on shared vocabulary, it will miss paraphrased
  questions that don't share keywords with the source text.
- **Generation**: a 3-node LangGraph graph (`retrieve -> generate ->` done).
  Runs in **mock mode** with zero setup (returns the raw retrieved chunks,
  clearly labeled), or **live mode** if you set `ANTHROPIC_API_KEY`, in which
  case it routes the same retrieved chunks through Claude with a strict
  "answer only from context, cite every claim, flag needs_verify chunks"
  system prompt.
- **Calculator** (`rag/calculator.py`): deliberately NOT an LLM. It only
  returns the two data points we actually have (70% target for FY 2026-27,
  100% for FY 2028-29) and says "not available" for anything else, instead
  of a model inventing a plausible-looking full schedule.

## Setup

```bash
cd epr-copilot
pip install -r requirements.txt
```

Run in mock mode (no API key, works immediately):

```bash
python3 app.py
```

Open http://localhost:5000 -- you'll see a "MOCK MODE" badge, and questions
will return the raw retrieved chunks instead of a synthesized answer. This
is the right way to first validate the *retrieval* quality on its own.

Run in live mode:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # your own key
python3 app.py
```

You'll see a "LIVE -- Claude connected" badge, and questions get a real
synthesized, cited answer. (You can also put the key in a `.env` file in
the project root -- it's loaded automatically via `python-dotenv`.)

Sanity-check the retrieval layer on its own, without Flask:

```bash
python3 -m rag.retriever
python3 -m rag.chain
```

## Project layout

```
epr-copilot/
  app.py                  Flask routes
  rag/
    knowledge_base.py      The curated (unverified!) content chunks
    retriever.py            TF-IDF retrieval over the knowledge base
    chain.py                 LangGraph pipeline: retrieve -> generate
    calculator.py            Deterministic deadline/target lookups
  templates/
    index.html               Minimal front end
  requirements.txt
```

## What to do next (mapped to the earlier build plan)

1. **Phase 0** -- find an actual EPR consultant or environmental compliance
   professional and get them to review `knowledge_base.py`. This matters
   more than any code change.
2. **Phase 2** -- replace every chunk's `text` with content sourced directly
   from the official MoEFCC gazette notifications and CPCB circulars, and
   resolve every chunk currently flagged `confidence="needs_verify"`
   (kb004, kb008, kb011).
3. **Phase 3 hardening** -- add LangSmith tracing (`LANGCHAIN_TRACING_V2=true`
   + `LANGCHAIN_API_KEY`) so you can evaluate answer quality against a test
   set your domain expert checks, before anyone else uses this.
4. **Phase 4** -- add the n8n-based deadline reminder layer (annual return,
   QR labeling, renewal) on top of the calculator functions already here.
5. Only after 1-3 are solid: think about a real embeddings-based retriever,
   auth, and a production WSGI server (this Flask dev server is not meant
   to be exposed to the internet).

## Known limitations (being upfront)

- 14 knowledge chunks, covering a fraction of the actual rule set. Real
  coverage needs the complete rules + amendments + CPCB circulars.
- Category III/IV definitions are explicitly marked incomplete (kb004) --
  don't answer category-boundary questions confidently until this is fixed.
- TF-IDF retrieval will miss questions phrased very differently from the
  source text (e.g. slang, indirect phrasing). Test with your actual target
  users' real questions, not just the sample queries here.
- No authentication, no rate limiting, no production deployment config --
  this is a local prototype, not something to put on the open internet
  as-is.
