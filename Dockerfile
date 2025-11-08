# Multi-stage build: Stage 1 - Build dependencies
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2 - Runtime image (smaller)
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy built dependencies from builder stage
COPY --from=builder /root/.local /root/.local
RUN mkdir /app/service && mkdir /app/tests

# Copy application code
COPY service/ ./service/
COPY tests/ ./tests/
COPY .env.example .env

# Install app in editable mode
RUN pip install --no-cache-dir --user -e .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run the app
CMD ["python", "service/__init__.py"]
