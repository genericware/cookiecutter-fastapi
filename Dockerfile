FROM python:3.11.5-bookworm as python-base

LABEL maintainer="caerulescens <caerulescens.github@proton.me>"

### Python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.4.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named ``.venv``
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    DEBCONF_NOWARNINGS="yes" \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    TZ="UTC"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# update package manager cache to install updates
RUN apt-get update \
    && apt-get install -y

# ``builder-base`` stage is used to build deps + create our virtual environment
FROM python-base as builder-base

# todo: github actions
# github personal access token
#ARG GITHUB_TOKEN

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

RUN mkdir -p $PYSETUP_PATH
WORKDIR $PYSETUP_PATH

# todo: github actions
# poetry dependencies
# example http-basic configuration when one poetry module depends on another poetry module during build
# RUN poetry config --local repositories.<repository-name> https://github.com/organization-name/repository-name.git
# RUN poetry config --local http-basic.<repository-name> organization-name $GITHUB_TOKEN
COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev

FROM python-base as development
WORKDIR $PYSETUP_PATH

# development image is used during development / testing
ENV FASTAPI_ENV=development

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install

# mountpoint of our code
COPY ./app /opt/generic-infrastructure/app
WORKDIR /opt/generic-infrastructure

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# production image used for runtime
FROM python-base as production
ENV FASTAPI_ENV=production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./app /opt/generic-infrastructure/app
WORKDIR /opt/generic-infrastructure

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8000", "--workers", "4", "--timeout", "14400"]
