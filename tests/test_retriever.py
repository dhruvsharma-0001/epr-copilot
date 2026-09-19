from rag.retriever import build_retriever


def test_build_retriever():
    retriever = build_retriever(k=3)
    assert retriever is not None

    results = retriever.invoke("QR code labeling")
    assert len(results) <= 3
    assert len(results) > 0

    # Ensure metadata is preserved on retrieved Document objects
    for doc in results:
        assert "id" in doc.metadata
        assert "title" in doc.metadata
        assert "citation" in doc.metadata
        assert "confidence" in doc.metadata
        assert len(doc.page_content) > 0
