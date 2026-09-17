"""
The RAG pipeline for EPR Compliance Copilot, built as a LangGraph graph:

    retrieve_node -> generate_node

Supports multiple generation modes, auto-selected based on environment keys:

  - GOOGLE GEMINI: Set GEMINI_API_KEY or GOOGLE_API_KEY
  - ANTHROPIC CLAUDE: Set ANTHROPIC_API_KEY
  - OPENAI: Set OPENAI_API_KEY
  - MOCK MODE (default, no API key needed): returns the retrieved chunks
    directly, clearly labeled. This lets you run and test the retrieval
    half of the system immediately with zero API budget.

The system prompt is deliberately strict: the model is told to answer only
from the provided chunks, to cite the chunk id for every claim, and to
flag anything sourced from a chunk marked confidence="needs_verify".
"""

import os
from typing import TypedDict, List, Optional, Tuple, Any

from langchain_core.documents import Document
from rag.retriever import build_retriever

DISCLAIMER = (
    "This is a prototype research assistant, not a compliance authority. "
    "Every answer must be verified against official CPCB / MoEFCC "
    "notifications and reviewed by a qualified EPR consultant or "
    "environmental lawyer before you rely on it for an actual filing."
)

SYSTEM_PROMPT = """You are a research assistant for India's plastic waste EPR \
(Extended Producer Responsibility) rules under the Plastic Waste Management Rules \
and CPCB guidelines.

Rules you must follow, no exceptions:
1. Answer ONLY using the context chunks provided below. Do not use outside \
knowledge, even if you believe you know the answer.
2. Cite the chunk id (e.g. [kb007]) for every specific claim you make.
3. If a chunk you rely on has confidence="needs_verify", say so explicitly \
in your answer -- do not present it with the same confidence as a verified chunk.
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


def get_active_llm() -> Tuple[str, Optional[Any]]:
    """
    Detects which LLM provider is configured in the environment.
    Priority order:
      1. GEMINI_API_KEY or GOOGLE_API_KEY
      2. ANTHROPIC_API_KEY
      3. OPENAI_API_KEY
      4. Fallback to mock mode
    """
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=gemini_key,
                temperature=0,
                max_output_tokens=1024,
            )
            return f"live (Gemini: {model_name})", llm
        except Exception as e:
            print(f"[warning] Failed to initialize Gemini: {e}")

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            from langchain_anthropic import ChatAnthropic
            model_name = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
            llm = ChatAnthropic(
                model=model_name,
                api_key=anthropic_key,
                temperature=0,
                max_tokens=1000,
            )
            return f"live (Claude: {model_name})", llm
        except Exception as e:
            print(f"[warning] Failed to initialize Claude: {e}")

    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI
            model_name = os.environ.get("OPENAI_MODEL", "gpt-4o")
            llm = ChatOpenAI(
                model=model_name,
                api_key=openai_key,
                temperature=0,
                max_tokens=1000,
            )
            return f"live (OpenAI: {model_name})", llm
        except Exception as e:
            print(f"[warning] Failed to initialize OpenAI: {e}")

    return "mock", None


def get_llm_status() -> dict:
    """Returns provider status information for frontend rendering."""
    provider_name, _ = get_active_llm()
    is_live = provider_name != "mock"
    return {
        "is_live": is_live,
        "provider": provider_name,
        "label": f"LIVE -- {provider_name.split('(')[1].rstrip(')')}" if is_live else "MOCK MODE -- no API key set",
    }


def retrieve_node(state: GraphState, retriever) -> GraphState:
    docs = retriever.invoke(state["question"])
    return {**state, "retrieved_docs": docs}


def _format_context(docs: List[Document]) -> str:
    lines = []
    for d in docs:
        m = d.metadata
        flag = " (NEEDS VERIFICATION)" if m.get("confidence") == "needs_verify" else ""
        lines.append(f"[{m['id']}] {m['title']}{flag}\nSource: {m['citation']}\n{d.page_content}")
    return "\n\n".join(lines)


def generate_node_mock(state: GraphState) -> GraphState:
    """Mock generator: returns raw retrieved chunks directly."""
    docs = state["retrieved_docs"]
    if not docs:
        answer = "No relevant chunks found in the knowledge base for this question."
    else:
        parts = ["[MOCK MODE -- no API key configured, showing raw retrieved chunks]\n"]
        for d in docs:
            m = d.metadata
            flag = "  <-- NEEDS VERIFICATION, do not treat as confirmed" if m.get("confidence") == "needs_verify" else ""
            parts.append(f"[{m['id']}] {m['title']}{flag}\nSource: {m['citation']}\n{d.page_content}\n")
        answer = "\n".join(parts)
    return {**state, "answer": answer, "mode": "mock"}


def generate_node_live(state: GraphState, llm, provider_name: str) -> GraphState:
    """Live generator using the active LLM provider."""
    context = _format_context(state["retrieved_docs"])
    prompt = SYSTEM_PROMPT.format(context=context, question=state["question"])
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    return {**state, "answer": content, "mode": provider_name}


def build_graph(k: int = 4):
    """Builds the LangGraph pipeline with dynamic model routing."""
    from langgraph.graph import StateGraph, END

    retriever = build_retriever(k=k)
    provider_name, llm = get_active_llm()

    graph = StateGraph(GraphState)
    graph.add_node("retrieve", lambda s: retrieve_node(s, retriever))

    if llm is not None:
        graph.add_node("generate", lambda s: generate_node_live(s, llm, provider_name))
    else:
        graph.add_node("generate", generate_node_mock)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


def ask(question: str, k: int = 4) -> dict:
    """Convenience wrapper: run the graph once and return structured response."""
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
    status = get_llm_status()
    print(f"Status: {status}")
    out = ask("What are the QR code labeling requirements for plastic packaging?")
    print(f"Mode: {out['mode']}\n")
    print(out["answer"])
    print("\nCitations:", [c["id"] for c in out["citations"]])
