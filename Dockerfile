FROM python:3.11-slim-bookworm AS base

LABEL maintainer="caerulescens <caerulescens.github@proton.me>"

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

RUN apt-get update \
    && apt-get install --no-install-recommends --assume-yes curl\
    && apt-get clean

FROM base AS builder

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM base AS development

WORKDIR $PYSETUP_PATH

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install

WORKDIR /opt/generic-infrastructure

COPY ./app/ ./app

EXPOSE $UVICORN_PORT

CMD ["uvicorn", "app.main:app"]

FROM base AS production

COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /opt/generic-infrastructure

COPY ./app/ ./app

EXPOSE $UVICORN_PORT

CMD ["uvicorn", "app.main:app"]
