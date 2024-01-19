# cookiecutter-fastapi

A [`cookiecutter`](https://github.com/cookiecutter/cookiecutter) template for [`fastapi`](https://github.com/tiangolo/fastapi) projects.

## dependencies

| name                                       | description                                |
|--------------------------------------------|--------------------------------------------|
| [pyenv](https://github.com/pyenv/pyenv)    | python version management                  |
| [poetry](https://github.com/python-poetry) | python packaging and dependency management |

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

> [!IMPORTANT]
> `src/cookiecutter-fastapi` is not currently used.

package:
```shell
poetry build
```

## usage

run:
```shell
cookiecutter https://github.com/generic-infrastructure/cookiecutter-fastapi
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
