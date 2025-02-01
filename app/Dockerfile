# Use lightweight Python 3.11 base image
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Production Stage ---
FROM python:3.11-slim

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m trader && mkdir /app && chown trader /app
USER trader
WORKDIR /app

# Copy application code
COPY --chown=trader:trader app/ ./app/

# Set default environment variables
ENV BERA_RPC="https://rpc.berachain.com" \
    RWA_API="https://api.ondo.finance/v1/yields" \
    CAPITAL=10000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

# Expose metrics port (for Prometheus)
EXPOSE 8000

# Run the bot
CMD ["python", "app/main.py"]