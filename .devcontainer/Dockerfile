# First stage: Get uv binary from official image
FROM ghcr.io/astral-sh/uv:latest AS uv

# Second stage: Build development environment
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary from first stage
COPY --from=uv /uv /usr/local/bin/uv

# Set working directory
WORKDIR /workspace

# Install development tools via uv
RUN uv pip install --system ruff pytest pytest-cov

# Verify installations
RUN uv --version && ruff --version && pytest --version
