# Multi-stage Dockerfile for development and production
ARG PYTHON_VERSION=3.12

# Base stage with common dependencies
FROM python:${PYTHON_VERSION}-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Development stage
FROM base as development

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install all dependencies including dev
RUN uv sync --frozen --all-extras

# Copy source code
COPY . .

# Install pre-commit hooks
RUN uv run pre-commit install --install-hooks

# Set up development environment
CMD ["/bin/bash"]

# Testing stage
FROM base as testing

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install all dependencies
RUN uv sync --frozen --all-extras

# Copy source code
COPY . .

# Run tests
RUN uv run pytest --cov=claude_prompts_tweaks --cov-report=xml --cov-fail-under=90

# Security scanning stage
FROM base as security

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with security tools
RUN uv sync --frozen --all-extras

# Copy source code
COPY . .

# Run security scans
RUN uv run bandit -r claude_prompts_tweaks -ll && \
    uv run safety check && \
    uv run pip-audit

# Builder stage
FROM base as builder

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install production dependencies only
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Build the package
RUN uv build

# Production stage
FROM python:${PYTHON_VERSION}-slim as production

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy built package from builder
COPY --from=builder /app/dist/*.whl /tmp/

# Install the package
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*.whl

# Switch to non-root user
USER appuser

# Set entrypoint
ENTRYPOINT ["claude-prompts-tweaks"]
CMD ["--help"]

# CI stage for GitHub Actions
FROM base as ci

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install all dependencies
RUN uv sync --frozen --all-extras

# Copy source code
COPY . .

# Pre-install pre-commit hooks to speed up CI
RUN uv run pre-commit install --install-hooks && \
    uv run pre-commit run --all-files || true

# Default to running tests
CMD ["uv", "run", "pytest"]