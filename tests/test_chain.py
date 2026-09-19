from rag.chain import get_graph, ask, get_llm_status, DISCLAIMER


def test_get_graph_singleton():
    g1 = get_graph(k=4)
    g2 = get_graph(k=4)
    assert g1 is g2, "get_graph should return cached singleton instance"


def test_ask_mock_mode():
    result = ask("What are the QR code labeling requirements for plastic packaging?")
    assert result["question"] == "What are the QR code labeling requirements for plastic packaging?"
    assert len(result["citations"]) > 0
    assert result["disclaimer"] == DISCLAIMER
    assert "answer" in result
    assert len(result["answer"]) > 0


def test_get_llm_status():
    status = get_llm_status()
    assert "is_live" in status
    assert "provider" in status
    assert "label" in status
