FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends make git \
    && rm -rf /var/lib/apt/lists/* \
    && git config --system --add safe.directory /repo
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /usr/local/bin/uv
WORKDIR /build
COPY generate/pyproject.toml generate/pyproject.toml
COPY generate/braingen generate/braingen
COPY dashboard/pyproject.toml dashboard/uv.lock dashboard/
# Third-party deps only; braingen and the dashboard are imported from the mount.
RUN cd dashboard && uv export --frozen --no-hashes --no-emit-project --no-emit-package braingen -o /tmp/req.txt \
    && uv pip install --system --no-cache -r /tmp/req.txt
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    BRAIN_REPO=/repo \
    PYTHONPATH=/repo/docs-arc42-brain/_system/dashboard:/repo/docs-arc42-brain/_system/generate
WORKDIR /repo/docs-arc42-brain/_system/dashboard
EXPOSE 4211
CMD ["gunicorn", "--bind", "0.0.0.0:4211", "--worker-class", "gthread", "--workers", "1", "--threads", "8", "app:create_app()"]
