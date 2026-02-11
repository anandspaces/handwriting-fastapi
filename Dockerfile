FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    WORKERS=4 \
    TIMEOUT=1800

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install build dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel Cython

# Install Python dependencies (including gunicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Create necessary directories with proper permissions
RUN mkdir -p /tmp /app/logs && \
    chmod 1777 /tmp && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run with Gunicorn and multiple workers
# --preload: Load app before forking (shared memory via copy-on-write)
# --workers: Number of parallel worker processes
# --worker-class: Use Uvicorn workers for async support
# --timeout: Request timeout
# Replace the CMD in your Dockerfile with:
CMD uvicorn app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers ${WORKERS} \
    --timeout-keep-alive ${TIMEOUT} \
    --log-level info