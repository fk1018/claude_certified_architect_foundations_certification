FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

ENV TERM=xterm-256color
ENV UV_PYTHON=3.14
ENV UV_PROJECT_ENVIRONMENT=/app/cli/.venv

ENTRYPOINT ["uv", "run", "--project", "/app/cli", "ccafc"]
