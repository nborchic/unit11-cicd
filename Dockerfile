# =========================================================
# Stage 1: Builder
# Install Python dependencies
# =========================================================
FROM python:3.11-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# =========================================================
# Stage 2: Runtime
# =========================================================
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl for Docker HEALTHCHECK
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages
COPY --from=builder /install /usr/local

# Copy project files
COPY src/ ./src/
COPY models/ ./models/
COPY data/ ./data/

# Create a non-root user
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1


CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]