FROM python:3.11.5-bookworm as python-base

LABEL maintainer="caerulescens <caerulescens.github@proton.me>"

ENV PYTHONUNBUFFERED=1 \
    # prevent .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip environment variables
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry environment variables
    # see https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.6.1 \
    # install poetry at this location
    POETRY_HOME="/opt/poetry" \
    # create a virtual environment in the project's root
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # skip interactive questions
    POETRY_NO_INTERACTION=1 \
    DEBCONF_NOWARNINGS="yes" \
    \
    # paths
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    TZ="UTC"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# update package manager cache
RUN apt-get update \
    && apt-get install -y

FROM python-base as builder-base

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# create pysetup directory
RUN mkdir -p $PYSETUP_PATH
WORKDIR $PYSETUP_PATH

# poetry dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev

FROM python-base as development
WORKDIR $PYSETUP_PATH

# select development image
ENV FASTAPI_ENV=development

# copy in poetry + virtual environment
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# cache runtime deps for quick builds
RUN poetry install

# mountpoint
COPY ./app /opt/generic-infrastructure/app
WORKDIR /opt/generic-infrastructure

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python-base as production

# select production image
ENV FASTAPI_ENV=production

# copy in virtual environment
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# mountpoint
COPY ./app /opt/generic-infrastructure/app
WORKDIR /opt/generic-infrastructure

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8000", "--workers", "4", "--timeout", "14400"]
