"""
Retrieval layer for the EPR Compliance Copilot prototype.

Uses LangChain's TFIDFRetriever (scikit-learn under the hood) instead of an
embedding model. This is a deliberate choice for the prototype stage:

  - No model weights to download, no vector DB to run -- works instantly,
    anywhere, offline.
  - It's transparent and debuggable: you can literally inspect the TF-IDF
    scores and see why a chunk was or wasn't retrieved, which is valuable
    while you're still validating the knowledge base itself.

When you move past prototype stage and the knowledge base grows past a few
hundred chunks, swap this for a real embedding-based retriever (e.g.
OpenAIEmbeddings / VoyageAIEmbeddings + a vector store like Chroma or FAISS).
TF-IDF is a keyword-matching method -- it will miss semantically similar
questions that don't share vocabulary with the source text.
"""

from langchain_core.documents import Document
from langchain_community.retrievers import TFIDFRetriever

from rag.knowledge_base import KNOWLEDGE_BASE


def build_retriever(k: int = 4) -> TFIDFRetriever:
    """
    Builds a TF-IDF retriever over the knowledge base.

    Args:
        k: number of chunks to retrieve per query.
    """
    documents = [
        Document(
            page_content=chunk["text"],
            metadata={
                "id": chunk["id"],
                "title": chunk["title"],
                "citation": chunk["citation"],
                "confidence": chunk["confidence"],
            },
        )
        for chunk in KNOWLEDGE_BASE
    ]

    retriever = TFIDFRetriever.from_documents(documents, k=k)
    return retriever


if __name__ == "__main__":
    # Quick manual sanity check: run `python3 -m rag.retriever` from the
    # project root and see what gets retrieved for a sample question.
    retriever = build_retriever(k=3)
    sample_questions = [
        "What are the QR code labeling requirements?",
        "What happens if I miss my annual EPR filing deadline?",
        "How much does an EPR certificate cost?",
    ]
    for q in sample_questions:
        print(f"\nQuery: {q}")
        results = retriever.invoke(q)
        for r in results:
            print(f"  [{r.metadata['id']}] {r.metadata['title']} "
                  f"(confidence={r.metadata['confidence']})")
