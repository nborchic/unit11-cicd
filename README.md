# Project 2 – Real-Time Fraud Detection System

## Overview

This project implements a real-time fraud detection system using FastAPI, Redis, Kafka, Docker, and Nginx. Transactions are processed through a streaming pipeline where customer features are stored in Redis and used by a fraud detection API to generate predictions. The system also demonstrates blue-green deployment and includes automated testing and performance benchmarking.

---

## Features

- FastAPI REST API for fraud prediction
- Single and batch prediction endpoints
- Redis feature store with TTL support
- Kafka-based transaction streaming
- Docker containerization
- Blue-green deployment with Nginx
- Automated testing using pytest
- Performance testing for latency and throughput

---

## Project Structure

```text
src/
├── api/
├── streaming/
├── monitoring/
├── models/
tests/
deployment/
Dockerfile
docker-compose.yml
docker-compose.blue-green.yml
requirements.txt
README.md
```

---

## Prerequisites

Before running the project, install:

- Python 3.11+
- Docker Desktop
- Git

---

## Setup

Create the environment file and generate the seed dataset:

```bash
cp .env.example .env
python data/generate_seed.py
```

(Optional) Train the baseline model:

```bash
python -m src.models.train
```

A fallback model is available if a trained model is not present.

---

## Running the System

Build and start all containers:

```bash
docker compose up --build
```

The application will be available at:

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Kafka | localhost:29092 |

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /model_info` | Model information |
| `POST /predict` | Predict fraud for a single transaction |
| `POST /predict_batch` | Predict fraud for multiple transactions |

---

## Running Tests

Execute the automated tests:

```bash
pytest -q tests/
```

---

## Performance Testing

Run the performance benchmark:

```bash
python tests/test_performance.py --n 1000 --url http://localhost:8000
```

The benchmark reports:

- Throughput (requests/second)
- p50 latency
- p95 latency
- p99 latency
- Maximum latency
- Error rate

---

## Blue-Green Deployment

Start the blue-green deployment environment:

```bash
docker compose -f deployment/docker-compose.blue-green.yml up --build
```

Switch traffic between the Blue and Green deployments:

```bash
bash deployment/switch_traffic.sh
```

The stable endpoint is available at:

```
http://localhost:8080
```

---

## Technologies Used

- Python
- FastAPI
- Kafka
- Redis
- Docker
- Docker Compose
- Nginx
- Pytest

---

## Author

Nicholas Borchich

DATA-789 – Project 2

East Carolina University