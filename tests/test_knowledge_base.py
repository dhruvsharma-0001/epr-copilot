from rag.knowledge_base import KNOWLEDGE_BASE


def test_knowledge_base_structure():
    assert len(KNOWLEDGE_BASE) >= 16, "Knowledge base should contain at least 16 chunks"

    seen_ids = set()
    valid_confidences = {"verified", "reported", "needs_verify"}

    for chunk in KNOWLEDGE_BASE:
        assert "id" in chunk, "Chunk missing 'id'"
        assert "title" in chunk, f"Chunk {chunk.get('id')} missing 'title'"
        assert "text" in chunk, f"Chunk {chunk.get('id')} missing 'text'"
        assert "citation" in chunk, f"Chunk {chunk.get('id')} missing 'citation'"
        assert "confidence" in chunk, f"Chunk {chunk.get('id')} missing 'confidence'"

        chunk_id = chunk["id"]
        assert chunk_id not in seen_ids, f"Duplicate chunk id: {chunk_id}"
        seen_ids.add(chunk_id)

        assert chunk["confidence"] in valid_confidences, (
            f"Chunk {chunk_id} has invalid confidence: {chunk['confidence']}"
        )
        assert len(chunk["text"].strip()) > 30, f"Chunk {chunk_id} text is too short"
