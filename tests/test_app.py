"""Unit tests that run in CI before the eval gate."""
import subprocess
import sys

from fastapi.testclient import TestClient

# ensure a model exists for the /predict test
subprocess.run([sys.executable, "train.py"], check=True)

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict_shape():
    r = client.post("/predict", json={"features": [0.1, -0.2, 0.3, 0.0, 1.1, -0.5]})
    assert r.status_code == 200
    body = r.json()
    assert "fraud_score" in body
    assert 0.0 <= body["fraud_score"] <= 1.0
    assert isinstance(body["is_fraud"], bool)
