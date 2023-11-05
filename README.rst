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
| `docker`_  | container tools                            |
+------------+--------------------------------------------+
| `make`_    | generates executables                      |
+------------+--------------------------------------------+

install::

    poetry install
    pre-commit install

=======
 usage
=======

run::

    docker compose up -d postgres
    uvicorn app.main:app

build::

    docker build .

compose::

    docker compose up

test::

    pytest .

coverage::

    coverage run -m pytest
    coverage report -m

docs::

    make -C docs html

pre-commit::

    pre-commit run

ruff::

    ruff .

.. _cpython: https://www.python.org/
.. _poetry: https://python-poetry.org/
.. _docker: https://www.docker.com/
.. _make: https://www.gnu.org/software/make/
