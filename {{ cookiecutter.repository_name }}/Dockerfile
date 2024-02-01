FROM python:3.10-slim-bookworm AS base
LABEL maintainer="caerulescens <caerulescens.github@proton.me>"
ARG HOST=0.0.0.0 \
ARG PORT=8000 \
ARG WORKERS=1 \
ARG LOG_LEVEL=info \
ARG BACKLOG=2048 \
ARG TIMEOUT_KEEP_ALIVE=5 \
ARG TIMEOUT_GRACEFUL_SHUTDOWN=30 \
ARG USER=appuser \
ARG USER_GID=10001
ARG USER_UID=10001
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
    UVICORN_HOST=$HOST \
    UVICORN_PORT=$PORT \
    UVICORN_WORKERS=$WORKERS \
    UVICORN_LOG_LEVEL=$LOG_LEVEL \
    UVICORN_LOOP=auto \
    UVICORN_HTTP=auto \
    UVICORN_WS=auto \
    UVICORN_INTERFACE=auto \
    UVICORN_BACKLOG=$BACKLOG \
    UVICORN_TIMEOUT_KEEP_ALIVE=$TIMEOUT_KEEP_ALIVE \
    UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN=$TIMEOUT_GRACEFUL_SHUTDOWN
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
WORKDIR /opt
COPY src/{{ cookiecutter.package_name }}/ /opt/{{ cookiecutter.package_name }}
USER $USER
ENTRYPOINT ["tini", "--", "uvicorn", "{{ cookiecutter.package_name }}.main:app"]
EXPOSE $PORT
