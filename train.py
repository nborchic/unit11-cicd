"""Train a small fraud classifier and write model.pkl + metrics.json.

Deterministic (fixed seed). Set DEGRADE=1 to train on shuffled labels so the model
fails the eval gate on purpose — this powers Demo Beat 2 (the gate blocks a bad deploy).
"""
import json
import os

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

RNG = np.random.default_rng(42)
DEGRADE = os.environ.get("DEGRADE", "0") == "1"


def make_data(n=4000):
    # 6 numeric features; fraud (y=1) is a linearly separable-ish minority
    X = RNG.normal(size=(n, 6))
    signal = X[:, 0] * 1.6 + X[:, 1] * 1.1 - X[:, 2] * 0.9 + RNG.normal(scale=0.5, size=n)
    y = (signal > 1.0).astype(int)
    return X, y


def main():
    X, y = make_data()
    split = int(0.75 * len(X))
    Xtr, Xho, ytr, yho = X[:split], X[split:], y[:split], y[split:]

    ytr_fit = ytr.copy()
    if DEGRADE:
        # scramble 60% of training labels -> a deliberately bad model (Beat 2)
        idx = RNG.choice(len(ytr_fit), size=int(0.6 * len(ytr_fit)), replace=False)
        ytr_fit[idx] = 1 - ytr_fit[idx]

    model = LogisticRegression(max_iter=1000).fit(Xtr, ytr_fit)
    acc = accuracy_score(yho, model.predict(Xho))

    joblib.dump(model, "model.pkl")
    np.save("holdout_X.npy", Xho)
    np.save("holdout_y.npy", yho)
    with open("metrics.json", "w") as f:
        json.dump({"holdout_accuracy": round(float(acc), 4), "degraded": DEGRADE}, f, indent=2)
    print(f"Trained model. holdout_accuracy={acc:.4f} degraded={DEGRADE}")


if __name__ == "__main__":
    main()
