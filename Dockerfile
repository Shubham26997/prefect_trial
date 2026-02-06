# Multi-stage Dockerfile for Prefect workflows
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user for security
# RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
# FROM base as deevelopment

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest \
    black \
    isort \
    flake8

# Copy source code
COPY . .

# Change ownership to appuser
# RUN chown -R appuser:appuser /app

# USER appuser

# Default command for development - run the workflow
# CMD ["python", "task.py"]

# Production stage
# FROM base as production

# Copy only necessary files
COPY task.py .
COPY requirements.txt .

# Change ownership to appuser
# RUN chown -R appuser:appuser /app

# USER appuser

# Health check
# HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
#     CMD python -c "import prefect; print('Prefect is healthy')" || exit 1

# Default command for production
# CMD ["python", "task.py"]

# Server stage - for running Prefect server
# FROM base as server

COPY . .
# RUN chown -R appuser:appuser /app

# USER appuser

EXPOSE 4200

# Health check for server
# HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
#     CMD curl -f http://localhost:4200/api/health || exit 1

CMD ["prefect", "server", "start", "--host", "0.0.0.0", "--port", "4200"]