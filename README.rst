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
| `cpython`_ | programming language                       |
+------------+--------------------------------------------+
| `poetry`_  | packaging and dependency management        |
+------------+--------------------------------------------+
| `docker`_  | generates executables                      |
+------------+--------------------------------------------+
| `make`_    | generates executables                      |
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


.. _cpython: https://www.python.org/
.. _poetry: https://python-poetry.org/
.. _docker: https://www.docker.com/
.. _make: https://www.gnu.org/software/make/
