======================
 cookiecutter-fastapi
======================

:Author: caerulescens <caerulescens.github@proton.me>
:Description: ``cookiecutter`` template for ``fastapi``

==============
 dependencies
==============

+------------+--------------------------------------------+
| dependency | description                                |
+============+============================================+
| `pyenv`_   | python version management                  |
+------------+--------------------------------------------+
| `poetry`_  | python packaging and dependency management |
+------------+--------------------------------------------+
| `docker`_  | cross-platform container tools             |
+------------+--------------------------------------------+

=========
 install
=========

development::

    poetry install
    pre-commit install

production::

    poetry install --without dev

=======
 build
=======

package::

    poetry build

image (development)::

    docker build . -t app-development:0.1.0 --target development

image (production)::

    docker build . -t app-production:0.1.0 --target production

=====
 run
=====

app::

    python -m app

container::

    docker run --init app-development:0.1.0

stack::

    docker compose up

test::

    pytest .

coverage::

    coverage run -m pytest && coverage report -m

matrix::

    tox run

doc::

    make -C docs html

check::

    pre-commit run

format::

    black .

lint::

    ruff .

type::

    mypy .

.. _pyenv: https://github.com/pyenv
.. _poetry: https://github.com/python-poetry
.. _docker: https://github.com/docker
