"""
The actual RAG pipeline, built as a small LangGraph graph:

    retrieve_node -> generate_node -> format_node

Two generation modes, auto-selected:

  - MOCK MODE (default, no API key needed): returns the retrieved chunks
    directly, clearly labeled. This lets you run and test the *retrieval*
    half of the system immediately, with zero setup. Useful for iterating
    on the knowledge base itself before you spend any API budget.

  - LIVE MODE (set ANTHROPIC_API_KEY): routes the retrieved chunks through
    Claude for a real synthesized, cited answer.

The system prompt is deliberately strict: the model is told to answer only
from the provided chunks, to cite the chunk id for every claim, and to
flag anything sourced from a chunk marked confidence="needs_verify". This
mirrors the citation-grounding discipline described in the build plan --
it's the single most important design constraint in this whole prototype.
"""

import os
from typing import TypedDict, List

from langchain_core.documents import Document
from rag.retriever import build_retriever

DISCLAIMER = (
    "This is a prototype research assistant, not a compliance authority. "
    "Every answer must be verified against the official CPCB / MoEFCC "
    "notifications and reviewed by a qualified EPR consultant or "
    "environmental lawyer before you rely on it for an actual filing."
)

SYSTEM_PROMPT = """You are a research assistant prototype for India's plastic \
waste EPR (Extended Producer Responsibility) rules.

Rules you must follow, no exceptions:
1. Answer ONLY using the context chunks provided below. Do not use outside \
knowledge, even if you believe you know the answer.
2. Cite the chunk id (e.g. [kb007]) for every specific claim you make.
3. If a chunk you rely on has confidence="needs_verify", say so explicitly \
in your answer -- do not present it with the same confidence as a \
confidence="reported" chunk.
4. If the provided chunks do not contain enough information to answer the \
question, say exactly that. Do not fill the gap with a plausible-sounding \
guess.
5. Never state a specific percentage, date, rupee amount, or clause number \
that does not appear verbatim in the provided context.

Context chunks:
{context}

Question: {question}

Answer (with inline [chunk_id] citations):"""


class GraphState(TypedDict):
    question: str
    retrieved_docs: List[Document]
    answer: str
    mode: str


def retrieve_node(state: GraphState, retriever) -> GraphState:
    docs = retriever.invoke(state["question"])
    return {**state, "retrieved_docs": docs}


def _format_context(docs: List[Document]) -> str:
    lines = []
    for d in docs:
        m = d.metadata
        flag = " (NEEDS VERIFICATION)" if m["confidence"] == "needs_verify" else ""
        lines.append(f"[{m['id']}] {m['title']}{flag}\nSource: {m['citation']}\n{d.page_content}")
    return "\n\n".join(lines)


def generate_node_mock(state: GraphState) -> GraphState:
    """No API key configured -- return the retrieved chunks directly instead
    of a synthesized answer. Proves the retrieval pipeline works end-to-end
    without spending a single API call."""
    docs = state["retrieved_docs"]
    if not docs:
        answer = "No relevant chunks found in the knowledge base for this question."
    else:
        parts = ["[MOCK MODE -- no ANTHROPIC_API_KEY set, showing raw retrieved chunks]\n"]
        for d in docs:
            m = d.metadata
            flag = "  <-- NEEDS VERIFICATION, do not treat as confirmed" if m["confidence"] == "needs_verify" else ""
            parts.append(f"[{m['id']}] {m['title']}{flag}\nSource: {m['citation']}\n{d.page_content}\n")
        answer = "\n".join(parts)
    return {**state, "answer": answer, "mode": "mock"}


def generate_node_live(state: GraphState) -> GraphState:
    """Real generation via Claude, grounded strictly in retrieved chunks."""
    from langchain_anthropic import ChatAnthropic

    context = _format_context(state["retrieved_docs"])
    prompt = SYSTEM_PROMPT.format(context=context, question=state["question"])

    # Model name matches Anthropic's current API string as of this writing.
    # Change if your account/SDK expects a different model identifier.
    llm = ChatAnthropic(model="claude-sonnet-5", max_tokens=1000, temperature=0)
    response = llm.invoke(prompt)
    return {**state, "answer": response.content, "mode": "live"}


def build_graph(k: int = 4):
    """Builds the LangGraph pipeline. Falls back to mock generation
    automatically if ANTHROPIC_API_KEY isn't set."""
    from langgraph.graph import StateGraph, END

    retriever = build_retriever(k=k)
    use_live = bool(os.environ.get("ANTHROPIC_API_KEY"))

    graph = StateGraph(GraphState)
    graph.add_node("retrieve", lambda s: retrieve_node(s, retriever))
    graph.add_node("generate", generate_node_live if use_live else generate_node_mock)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


def ask(question: str, k: int = 4) -> dict:
    """Convenience wrapper: run the graph once and return a clean dict for
    the Flask layer to serialize."""
    app = build_graph(k=k)
    result = app.invoke({"question": question, "retrieved_docs": [], "answer": "", "mode": ""})

    citations = [
        {
            "id": d.metadata["id"],
            "title": d.metadata["title"],
            "citation": d.metadata["citation"],
            "confidence": d.metadata["confidence"],
        }
        for d in result["retrieved_docs"]
    ]

    return {
        "question": question,
        "answer": result["answer"],
        "citations": citations,
        "mode": result["mode"],
        "disclaimer": DISCLAIMER,
    }


if __name__ == "__main__":
    # Quick manual test: python3 -m rag.chain
    out = ask("What are the QR code labeling requirements for plastic packaging?")
    print(f"Mode: {out['mode']}\n")
    print(out["answer"])
    print("\nCitations:", [c["id"] for c in out["citations"]])
