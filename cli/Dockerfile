# Study-workspace image for the Claude certification CLI.
#
# Python 3.14 and every dependency are installed at BUILD time into /opt --
# deliberately outside /app, because the repository is bind-mounted over /app at
# run time. The result: runs start instantly, need no network, and never write a
# .venv into your working tree.
#
# Practice exams, study packs, generated data, and your saved progress all live
# in the mounted repo, so they persist between runs and survive image rebuilds.

FROM ghcr.io/astral-sh/uv:debian

ENV UV_PYTHON=3.14 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_INSTALL_DIR=/opt/python \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    TERM=xterm-256color \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app

# 1. Dependencies only. Cached until pyproject.toml or uv.lock changes.
COPY cli/pyproject.toml cli/uv.lock /app/cli/
RUN uv sync --project /app/cli --frozen --no-install-project

# 2. The CLI itself, installed editable so it resolves REPO_ROOT to the /app mount.
COPY cli/ /app/cli/
RUN uv sync --project /app/cli --frozen \
 && chmod -R a+rX /opt/venv /opt/python

# ccafc / ccdvf / ccarp are all on PATH; override --entrypoint to switch tracks.
ENTRYPOINT ["ccafc"]
