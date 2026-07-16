"""FastAPI serving layer — matches your HW4 fraud API shape (port 8000).

GET  /health   -> liveness/readiness (no model dependency, used by probes)
POST /predict  -> returns a fraud score for a 6-feature transaction
"""
import os

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="fraud-api", version="1.0")

_MODEL = None


def _model():
    global _MODEL
    if _MODEL is None and os.path.exists("model.pkl"):
        _MODEL = joblib.load("model.pkl")
    return _MODEL


class Transaction(BaseModel):
    features: list[float]  # length 6


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(txn: Transaction):
    m = _model()
    if m is None:
        return {"error": "model not loaded"}
    x = np.asarray(txn.features, dtype=float).reshape(1, -1)
    proba = float(m.predict_proba(x)[0, 1])
    return {"fraud_score": round(proba, 4), "is_fraud": bool(proba >= 0.5)}
