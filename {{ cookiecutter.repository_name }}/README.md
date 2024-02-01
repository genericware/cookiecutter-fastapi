# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## dependencies

| name                                       | description                                |
|--------------------------------------------|--------------------------------------------|
| [pyenv](https://github.com/pyenv/pyenv)    | python version management                  |
| [poetry](https://github.com/python-poetry) | python packaging and dependency management |
| [docker](https://github.com/docker)        | container tools                            |

## install

development:
```shell
poetry install
poetry shell
pre-commit install
```

production:
```shell
poetry install --without dev
```

## build

package:
```shell
poetry build
```

image:
```shell
docker build . -t cookiecutter-fastapi-development:{{ cookiecutter.version }}
```

## usage

run:
```shell
python -m {{ cookiecutter.package_name }}
```

container:
```shell
docker run app-development:{{ cookiecutter.version }} --target runtime
```

stack:
```shell
docker compose up
```

[//]: # (How to recreate `alembic` database migrations:)
[//]: # (1. Create an environment: `alembic init --template async alembic`)
[//]: # (2. Edit the alembic.ini file to set `sqlalchemy.url`)
[//]: # (3. Create a migration script: `alembic revision -m "init_db"`)
[//]: # (4. Run first migration: `alembic upgrade head`)
[//]: # (see: https://alembic.sqlalchemy.org/en/latest/index.html)
migrations:
```shell
alembic revision -m "<message>"
alembic upgrade head
```

test:
```shell
tox run
```

doc:
```shell
make -C docs html
```

check:
```shell
pre-commit run
```
