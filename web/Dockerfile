# Web version of the study workspace: a static site served by nginx.
#
# Three stages, because the web app has no backend and no data of its own -- it
# reads the JSON the CLI generates from the Markdown exams. So we generate that
# first, build the site against it, and ship only the result.
#
#   docker compose up web    ->  http://localhost:8080
#
# Progress (attempts, scores, flashcard state) lives in each viewer's browser
# localStorage, one record per track. Nothing is stored server side, so the same
# image can be run locally by one person or hosted once for the whole team.

# --------------------------------------------------------------- 1. exam data
FROM ghcr.io/astral-sh/uv:debian AS data

ENV UV_PYTHON=3.14 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_INSTALL_DIR=/opt/python \
    UV_LINK_MODE=copy

WORKDIR /app
COPY cli/pyproject.toml cli/uv.lock /app/cli/
RUN uv sync --project /app/cli --frozen --no-install-project

COPY cli/ /app/cli/
# The generator resolves these from the repo root, so they have to be present.
COPY practice_exams/                        /app/practice_exams/
COPY study_packs/                           /app/study_packs/
COPY practice_exams_developer_foundations/  /app/practice_exams_developer_foundations/
COPY study_packs_developer_foundations/     /app/study_packs_developer_foundations/
COPY practice_exams_architect_professional/ /app/practice_exams_architect_professional/
COPY study_packs_architect_professional/    /app/study_packs_architect_professional/

RUN uv sync --project /app/cli --frozen \
 && /opt/venv/bin/ccafc import \
 && /opt/venv/bin/ccdvf import \
 && /opt/venv/bin/ccarp import

# ------------------------------------------------------------- 2. static build
FROM docker.io/library/node:22-alpine AS build

WORKDIR /app/web
COPY web/package.json web/package-lock.json ./
RUN npm ci

COPY web/ ./
# sync-data.mjs looks for this at <repo root>/cli/data/generated.
COPY --from=data /app/cli/data/generated /app/cli/data/generated

# "/" when serving from the root of a host or container. For a subpath -- a
# GitHub Pages project site, say -- build with --build-arg BASE_PATH=/name/
ARG BASE_PATH=/
RUN node scripts/sync-data.mjs \
 && npx tsc -b \
 && npx vite build --base="$BASE_PATH"

# -------------------------------------------------------------------- 3. serve
FROM docker.io/library/nginx:alpine

COPY web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/web/dist /usr/share/nginx/html

EXPOSE 80
