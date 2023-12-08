======================
 cookiecutter-fastapi
======================

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

install::

    poetry install
    pre-commit install

=======
 usage
=======

run(``uvicorn``)::

    uvicorn app.main:app --reload

build(``docker``)::

    docker build . -t cookiecutter-fastapi:0.1.0

run(``docker``)::

    docker run --init cookiecutter-fastapi:0.1.0

compose::

    docker compose up

test::

    pytest .

coverage::

    coverage run -m pytest && coverage report -m

docs::

    make -C docs html

pre-commit::

    pre-commit run

black::

    black .

ruff::

    ruff .

mypy::

    mypy .


.. _cpython: https://www.python.org/
.. _poetry: https://python-poetry.org/
.. _docker: https://www.docker.com/
.. _make: https://www.gnu.org/software/make/
