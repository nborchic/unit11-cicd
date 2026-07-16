# Unit 11 Demo — CI/CD-for-ML with GitHub Actions

A tiny, runnable **CI/CD pipeline for a model** you drop onto your HW4-style repo. It shows the
one thing CrowdStrike was missing: **a gate that blocks a bad artifact from shipping.**

The pipeline on every push:

```
build image  →  pytest  →  MODEL EVAL GATE (accuracy ≥ threshold)  →  [deploy: canary → 100%]
                                     │
                        fails ──►  pipeline goes RED, deploy is BLOCKED
```

The **core demo runs entirely on GitHub-hosted runners at $0** — no Azure needed. The deploy job is
an optional stub that reuses your Unit 10 Azure Container Apps floor (see the workflow comments).

## Run it locally first (dry-run before class)

```bash
pip install -r requirements.txt
pytest -q                       # unit tests
python train.py                 # trains model.pkl + writes metrics.json
python eval_gate.py             # the gate: exits non-zero if accuracy < EVAL_THRESHOLD (default 0.80)
docker build -t fraud-api .     # build the image
```

## The three demo beats

- **Beat 1 — green run.** Push to `main` (or run the workflow). Everything passes; deploy step reports "gate passed."
- **Beat 2 — the gate blocks a bad model.** Re-run the workflow with **`degrade = true`** (Actions → Run workflow),
  or bump **`eval_threshold`** to `0.99`. `train.py` produces a deliberately weak model, `eval_gate.py` fails,
  and **the deploy job never runs.** Say it out loud: *this is the Content Validator CrowdStrike didn't have.*
- **Beat 3 — staged rollout.** Point at the `deploy` job: it only runs `needs: ci` (after the gate) and rolls out
  **canary 10% → 100%** — the staged rollout CrowdStrike skipped. (Enable the real `az` steps if you want it live.)

## Files

| File | Role |
|------|------|
| `.github/workflows/ci-cd.yml` | the pipeline (build → test → **eval gate** → deploy) |
| `train.py` | trains a small fraud classifier; `DEGRADE=1` makes it fail the gate |
| `eval_gate.py` | the gate — asserts holdout accuracy ≥ `EVAL_THRESHOLD` |
| `app/main.py` | FastAPI service: `GET /health`, `POST /predict` (matches your HW4 API) |
| `tests/test_app.py` | pytest: model loads, `/predict` returns a valid score |
| `Dockerfile` | container image for the service |

## Bridge to HW4 (optional)

This lab rehearses real HW4 muscle: the **"Use this template → keep it Public"** flow is exactly how you
create and submit your HW4 repo; the fraud **`/health` + `/predict`** service is the one HW4 deploys; and the
**Azure Container Apps** target here *is* **HW4 Part 3**. See **`hw4-bridge/`** for an optional workflow that
automates your HW4 Part 3 Azure ship (bonus — the required path is still `deploy_azure.sh` in Cloud Shell).
Today's lab does **not** cover HW4's Kubernetes work (Part 1 — replicas/HPA/probes), and the CI/CD + eval gate
is a professional add-on, not an HW4 requirement.

**Capability framing:** GitHub Actions = *CI/CD automation / pipeline-as-code*. Alternatives: Azure DevOps
Pipelines (managed), GitLab CI, Jenkins (OSS), CML/DVC (ML-specific). Chosen here because you already have GitHub +
a repo, it's free on hosted runners, and it turns your repo into a real CI/CD-for-ML pipeline with zero Azure spend.
