# ========================
# Stage 1: Builder
# ========================
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Copy dependency file first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# ========================
# Stage 2: Runtime
# ========================
FROM python:3.11-slim

# Set environment
ENV TZ=UTC

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y cron tzdata && \
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Set permissions for data and cron directories
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Install cron job
RUN chmod 0644 cron/2fa-cron && crontab cron/2fa-cron

# Expose API port
EXPOSE 8080

# Start cron and API server
CMD cron && uvicorn app:app --host 0.0.0.0 --port 8080
