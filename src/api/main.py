"""
FastAPI serving app.

PROVIDED: app setup, model/feature-store load at startup, /health, /model/info,
and the request/response schemas (so input validation → HTTP 422 works for free).
YOU IMPLEMENT: the bodies of /predict and /predict_batch (graded: FastAPI Serving, 16 pts).
"""
from __future__ import annotations

import os
import time
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.api.fraud_detector import FraudDetector
from src.streaming.feature_store import FeatureStore

app = FastAPI(title="TrustBank Fraud Detection API")

# Loaded once at startup (do NOT load the model per-request).
detector = FraudDetector()
store = FeatureStore()


class Transaction(BaseModel):
    customer_id: str
    amount: float
    merchant_category: str
    is_online: bool
    timestamp: str
    transaction_id: Optional[str] = None


class FraudPrediction(BaseModel):
    transaction_id: Optional[str] = None
    fraud_probability: float
    is_fraud: int
    model_version: str
    latency_ms: float


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/model/info")
async def model_info():
    return {"model_version": detector.model_version}


@app.post("/predict", response_model=FraudPrediction)
async def predict_fraud(transaction: Transaction):
    """
    Predict fraud probability for a transaction.
    """

    start_time = time.perf_counter()

    try:
        customer_features = store.get_customer_features(
            transaction.customer_id
        ) or {
            "transaction_count": 0,
            "avg_amount": 0.0,
        }

        model_features = {
            "amount": transaction.amount,
            "merchant_category": transaction.merchant_category,
            "is_online": transaction.is_online,
            "transaction_count_24h": customer_features.get(
                "transaction_count", 0
            ),
            "avg_amount_24h": customer_features.get(
                "avg_amount", 0.0
            ),
        }

        result = detector.predict(model_features)

        latency_ms = (time.perf_counter() - start_time) * 1000

        return FraudPrediction(
            transaction_id=transaction.transaction_id,
            fraud_probability=float(result["fraud_probability"]),
            is_fraud=int(result["is_fraud"]),
            model_version=detector.model_version,
            latency_ms=latency_ms,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {exc}",
        ) from exc


@app.post("/predict_batch", response_model=List[FraudPrediction])
async def predict_fraud_batch(
    transactions: List[Transaction],
):
    """
    Predict fraud probabilities for multiple transactions.
    """

    predictions = []

    for transaction in transactions:
        prediction = await predict_fraud(transaction)
        predictions.append(prediction)

    return predictions