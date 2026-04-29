# Single-stage container for KundliKosh API.
# Use this with Render / Fly.io / Railway / HuggingFace Spaces — all have free tiers.
FROM python:3.11-slim

WORKDIR /app

# Install system deps (pyswisseph builds tiny C extension)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy engine first (cache-friendly)
COPY engine /app/engine
COPY api    /app/api

# Install
RUN pip install --no-cache-dir -e /app/engine \
    && pip install --no-cache-dir 'fastapi>=0.110' 'uvicorn[standard]>=0.29' 'pydantic>=2'

ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app/engine
EXPOSE 8000

# Render/Fly inject $PORT — fall back to 8000 locally
CMD ["sh", "-c", "uvicorn api.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
