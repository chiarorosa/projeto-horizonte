from fastapi.testclient import TestClient

from app.main import create_app


def test_health_responde_ok():
    res = TestClient(create_app()).get("/health")

    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
