# MicroAI DAO - Unified Docker Image
# Supports: API, Live Data Server, EXECAI Client

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json for Node dependencies
COPY package.json package-lock.json* ./
RUN npm install --production 2>/dev/null || true

# Copy source code
COPY src/ ./src/
COPY api/ ./api/
COPY services/ ./services/
COPY contracts/ ./contracts/

# Expose ports
# 5000 - Flask API
# 8787 - Live Data Server
EXPOSE 5000 8787

# Default command - run Flask API
CMD ["python", "api/app.py"]
