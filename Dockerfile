# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first to leverage layer caching
# Use the base requirements to keep image lean; override if needed via build args
COPY requirements/base.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Copy project
COPY . /app

# Ensure static directory exists
RUN mkdir -p /app/static && mkdir -p /app/media

# Collect static during build to speed up runtime (optional; depends on settings)
# If collectstatic fails due to settings, you can disable this step.
RUN python manage.py collectstatic --noinput || echo "collectstatic skipped"

EXPOSE 8000

# Default command: run with Daphne (ASGI) for WebSockets
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
