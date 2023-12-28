FROM python:3.11-slim-bookworm AS base
LABEL maintainer="caerulescens <caerulescens.github@proton.me>"
ARG USER=appuser
ARG USER_GID=10001
ARG USER_UID=10000
ENV \
    # os
    TZ=UTC \
    DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NOWARNINGS=yes \
    PYSETUP_PATH=/opt/pysetup \
    VENV_PATH=/opt/pysetup/.venv \
    # python
    PYTHONUNBUFFERED=true \
    PYTHONDONTWRITEBYTECODE=true \
    PYTHONFAULTHANDLER=true \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=true \
    PIP_DISABLE_PIP_VERSION_CHECK=true \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.7.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VIRTUALENVS_OPTIONS_NO_PIP=true \
    POETRY_INSTALLER_MODERN_INSTALLATION=true \
    POETRY_NO_INTERACTION=true \
    POETRY_NO_ANSI=true \
    POETRY_INSTALLER_PARALLEL=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true \
    # uvicorn
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000 \
    UVICORN_WORKERS=1 \
    UVICORN_LOG_LEVEL=debug \
    UVICORN_LOOP=auto \
    UVICORN_HTTP=auto \
    UVICORN_WS=auto \
    UVICORN_INTERFACE=auto \
    UVICORN_BACKLOG=2048 \
    UVICORN_TIMEOUT_KEEP_ALIVE=5 \
    UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN=30
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
RUN set -ex \
    && groupadd --system --gid "${USER_GID}" "${USER}" \
    && useradd --system --uid "${USER_UID}" --gid "${USER_GID}" --no-create-home "${USER}" \
    && apt-get update \
    && apt-get install -y tini \
    && apt-get purge -y --auto-remove \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder
WORKDIR $PYSETUP_PATH
RUN pip install poetry=="${POETRY_VERSION}"
COPY poetry.lock pyproject.toml ./
RUN --mount=type=cache,target="${POETRY_CACHE_DIR}" poetry install --without dev --no-root

FROM base AS runtime
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
WORKDIR /opt/generic-infrastructure
COPY src/app/ /opt/generic-infrastructure/app
USER $USER
ENTRYPOINT ["tini", "--", "uvicorn", "app.main:app"]
EXPOSE $UVICORN_PORT
