# Use a lightweight Python 3.13 image as the base
FROM python:3.13-slim AS builder

# Install uv by copying it from the official distribution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory and environment
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /home/my_library

COPY pyproject.toml uv.lock .
# Install dependencies first for better caching
# Requires pyproject.toml and uv.lock in your project root
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev


# Final runtime stage
FROM python:3.13-slim

WORKDIR /home/my_library

# Copy the virtual environment from the builder
COPY --from=builder /home/my_library/.venv /home/my_library/.venv

# Ensure the virtual environment is used
ENV PATH="/home/my_library/.venv/bin:$PATH"

# Copy your application source code
COPY app app
COPY alembic.ini .docker.env .