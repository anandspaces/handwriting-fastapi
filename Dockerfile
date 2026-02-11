FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install build dependencies (including Cython for PyYAML)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel Cython

# Install Python dependencies (including gunicorn)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Create a non-root user early
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

# Default command (will be overridden by docker-compose)
CMD ["python", "app.py"]