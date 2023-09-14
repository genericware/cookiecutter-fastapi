=============
 fastapi-app
=============

:Author: caerulescens <caerulescens.github@proton.me>
:Description:


=========
 install
=========

+------------+--------------------------------------------+
| dependency | description                                |
+============+============================================+
| `make`_    | generates executables                      |
+------------+--------------------------------------------+
| `cpython`_ | programming language                       |
+------------+--------------------------------------------+
| `poetry`_  | packaging and dependency management        |
+------------+--------------------------------------------+

configure ``poetry``::

    poetry install
    poetry shell

configure ``pre-commit``::

    pre-commit install

=======
 usage
=======

run::

    poetry run uvicorn app.main:app

docker-build::

    docker build .

docker-compose::

    docker compose up

test::

    poetry run pytest

coverage::

    poetry run coverage run -m pytest
    poetry run coverage report -m

docs::

    poetry run make -C docs html

pre-commit::

    pre-commit run

.. _make: https://www.gnu.org/software/make/
.. _cpython: https://www.python.org/
.. _poetry: https://python-poetry.org/