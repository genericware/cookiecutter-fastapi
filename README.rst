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

    todo

image::

    docker build . -t cookiecutter-fastapi:0.1.0

=====
 run
=====

app::

    uvicorn app.main:app

container::

    docker run --init cookiecutter-fastapi:0.1.0

compose::

    docker compose up

tests::

    pytest .

coverage::

    coverage run -m pytest && coverage report -m

docs::

    make -C docs html

checks::

    pre-commit run

formating::

    black .

linting::

    ruff .

analysis::

    mypy .

.. _pyenv: https://github.com/pyenv
.. _poetry: https://github.com/python-poetry
.. _docker: https://github.com/docker
