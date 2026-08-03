# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# Stage 1/2 — builder: resolves and installs dependencies into a venv.
# Kept separate from the runtime stage so the uv binary, pyproject.toml and
# uv.lock never end up in the image that actually ships — none of them are
# needed once the venv exists.
# ---------------------------------------------------------------------------
# Both base images are pinned to an exact version, never `latest`: a moving
# tag means two builds of the same commit can silently produce different
# images. Bump these deliberately when you want a newer Python/uv patch.
FROM python:3.13.14-slim AS builder

# uv is shipped as a single static binary — copying it out of its official
# image is faster and more reproducible than `pip install uv`.
COPY --from=ghcr.io/astral-sh/uv:0.12.0 /uv /bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Dependencies are their own layer, installed before the source is copied: as
# long as pyproject.toml / uv.lock are unchanged, rebuilds reuse the cache and
# take seconds instead of minutes.
# --frozen: install exactly uv.lock, never re-resolve. If this step fails with
# "the lockfile is not up-to-date", run `uv lock` and commit the result.
# --no-install-project: this project has no [build-system]; only its
# dependencies are installed, the source is used from /app/backend directly.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# ---------------------------------------------------------------------------
# Stage 2/2 — runtime: only the venv and the application source. No uv
# binary, no lockfiles, no pip cache — every dependency in uv.lock ships a
# manylinux wheel for cp313, so no compiler was ever needed either.
# ---------------------------------------------------------------------------
FROM python:3.13.14-slim

LABEL org.opencontainers.image.title="metadata-analysis-llm-for-sdc" \
      org.opencontainers.image.description="LLM pipeline normalizing SDC metadata workbooks for rtauargus" \
      org.opencontainers.image.source="https://github.com/InseeFrLab/metadata-analysis-llm-for-sdc"

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# app.py writes uploaded workbooks to <project root>/uploads/temp, i.e.
# /app/uploads/temp here. The container runs as a non-root user, so the
# directory has to exist and belong to that user before it drops privileges.
RUN useradd --create-home --uid 1000 appuser \
 && mkdir -p /app/uploads/temp \
 && chown -R 1000:1000 /app
USER 1000
ENV HOME=/home/appuser

EXPOSE 5000

# Reports container health to `docker run`/`docker ps` and to `docker compose`
# restart policies. Kubernetes ignores this instruction entirely — the
# readinessProbe in deploy/deployment.yaml is what governs the pod there —
# but it's what makes `docker run` alone (step 2 of DEPLOY.md, before the
# cluster is involved) report unhealthy if gunicorn never comes up.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:5000/ui_kits/sdc-pipeline/', timeout=2)" || exit 1

# --workers 1 is a hard requirement, not a tuning choice: app.py keeps `sessions`
# and `jobs` in module-level dicts and runs the LLM calls in background threads.
# With two workers, a /api/jobs/<id> poll would land on the process that never
# started that job and answer 404 at random. Concurrency comes from --threads.
#
# --timeout 120 is generous for the request handlers, which all return
# immediately (the long work happens in background threads, not in a request).
CMD ["gunicorn", \
     "--chdir", "/app/backend", \
     "--workers", "1", \
     "--threads", "8", \
     "--timeout", "120", \
     "--bind", "0.0.0.0:5000", \
     "--access-logfile", "-", \
     "app:app"]
