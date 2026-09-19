import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
    assert data["kb_chunks"] >= 16
    assert "is_live" in data
    assert "provider" in data


def test_status_endpoint(client):
    res = client.get("/api/status")
    assert res.status_code == 200
    data = res.get_json()
    assert "is_live" in data
    assert "provider" in data
    assert "label" in data


def test_ask_endpoint_valid(client):
    res = client.post("/api/ask", json={"question": "What is Category I plastic packaging?"})
    assert res.status_code == 200
    data = res.get_json()
    assert "answer" in data
    assert "citations" in data
    assert len(data["citations"]) > 0


def test_ask_endpoint_validation_errors(client):
    # Empty question
    res = client.post("/api/ask", json={"question": ""})
    assert res.status_code == 400
    assert "required" in res.get_json()["error"]

    # Too short (< 3 chars)
    res = client.post("/api/ask", json={"question": "hi"})
    assert res.status_code == 400
    assert "at least 3 characters" in res.get_json()["error"]

    # Too long (> 1000 chars)
    res = client.post("/api/ask", json={"question": "a" * 1001})
    assert res.status_code == 400
    assert "must not exceed 1000 characters" in res.get_json()["error"]


def test_calculate_endpoint(client):
    res = client.post("/api/calculate", json={
        "pibo_type": "Brand Owner",
        "fiscal_year": "2026-27",
        "tonnages": {"cat_1": 100, "cat_2": 200}
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_introduced_packaging_mt"] == 300.0
    assert data["potential_ec_penalty_exposure_inr"] > 0


def test_target_endpoint(client):
    res = client.get("/api/target/2026-27")
    assert res.status_code == 200
    data = res.get_json()
    assert data["found"] is True
    assert data["recycling_targets_pct"]["cat_1"] == 70


def test_deadline_endpoint(client):
    res = client.get("/api/deadline")
    assert res.status_code == 200
    data = res.get_json()
    assert "statutory_date" in data


def test_kb_endpoint(client):
    res = client.get("/api/kb")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 16
    for item in data:
        assert "id" in item
        assert "title" in item
        assert "text_preview" in item
