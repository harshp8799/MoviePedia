# Production image for the Movie Pedia API. Runs on Cloud Run / Render / any container host.
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install runtime deps first (better layer caching).
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# App code.
COPY app ./app

# Run as a non-root user.
RUN useradd --create-home --uid 10001 appuser
USER appuser

# Cloud Run / Render provide $PORT; default to 8080 locally.
ENV PORT=8080
EXPOSE 8080

# gunicorn with uvicorn workers; honors $PORT. Workers tuned for a small instance.
CMD exec gunicorn app.main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 2 \
    --bind "0.0.0.0:${PORT}" \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
