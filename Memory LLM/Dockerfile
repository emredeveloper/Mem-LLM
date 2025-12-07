# ============================================================================
# Mem-LLM Docker Image
# ============================================================================
# Build: docker build -t mem-llm .
# Run:   docker run -p 8000:8000 mem-llm
# ============================================================================

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-optional.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn[standard] websockets

# Copy application code
COPY . .

# Install mem-llm package
RUN pip install --no-cache-dir -e .

# Create directories for data persistence
RUN mkdir -p /app/memories /app/data

# Expose port for API server
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command - start API server
CMD ["python", "-m", "mem_llm.api_server"]
