# ============================================================
# Base image
# ============================================================
FROM python:3.14-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/venv/bin:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# ============================================================
# Builder
# ============================================================
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN uv venv /venv

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv export --frozen --no-dev --output-file requirements.txt

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r requirements.txt

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --no-deps .

RUN rm -rf /app/.venv || true

# ============================================================
# Runtime
# ============================================================
FROM base

COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /usr/local/bin/uvx /usr/local/bin/uvx

RUN useradd --system --uid 1000 --no-create-home appuser

COPY --from=builder /venv /venv
COPY --from=builder /app /app

RUN chown -R appuser:appuser /venv /app

WORKDIR /app
USER appuser

EXPOSE 8000

ENV UV_NO_CACHE=1


ENV PYTHONPATH=/app/src

CMD ["gunicorn", \
    "-w", "4", \
    "-k", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0:8000", \
    "--access-logfile", "/dev/null", \
    "--error-logfile", "/dev/null", \
    "user_pool.setup.main:create_entry_point()"]
