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

## run

app:
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

test:
```shell
pytest .
```

coverage:
```shell
coverage run -m pytest && coverage report -m
```

matrix:
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

format:
```shell
black .
```

lint:
```shell
ruff .
```

type:
```shell
mypy .
```
