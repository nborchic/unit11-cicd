"""The eval GATE. Loads the trained model, scores the holdout, and FAILS (exit 1)
if accuracy is below EVAL_THRESHOLD. This is the check that blocks a bad model from
reaching deploy — the 'Content Validator' CrowdStrike didn't have for its content pipeline.
"""
import json
import os
import sys

import joblib
import numpy as np
from sklearn.metrics import accuracy_score

THRESHOLD = float(os.environ.get("EVAL_THRESHOLD", "0.80"))


def main() -> int:
    model = joblib.load("model.pkl")
    Xho = np.load("holdout_X.npy")
    yho = np.load("holdout_y.npy")
    acc = accuracy_score(yho, model.predict(Xho))

    with open("metrics.json", "w") as f:
        json.dump({"holdout_accuracy": round(float(acc), 4), "threshold": THRESHOLD}, f, indent=2)

    if acc < THRESHOLD:
        print(f"❌ EVAL GATE FAILED: accuracy {acc:.4f} < threshold {THRESHOLD:.2f} — DEPLOY BLOCKED.")
        return 1
    print(f"✅ EVAL GATE PASSED: accuracy {acc:.4f} ≥ threshold {THRESHOLD:.2f} — ok to deploy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
