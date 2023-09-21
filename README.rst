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

`uvicorn`_::

    docker compose up -d postgres
    uvicorn app.main:app --reload

`build`_::

    docker build .

`compose`_::

    docker compose up

`test`_::

    pytest .

`coverage`_::

    coverage run -m pytest
    coverage report -m

`docs`_::

    make -C docs html

`pre-commit`_::

    pre-commit run

`ruff`_::

    ruff .

.. _cpython: https://www.python.org/
.. _poetry: https://python-poetry.org/
.. _docker: https://www.docker.com/
.. _make: https://www.gnu.org/software/make/
.. _uvicorn: https://www.uvicorn.org/
.. _gunicorn: https://gunicorn.org/
.. _build: https://docs.docker.com/engine/reference/commandline/build/
.. _compose: https://docs.docker.com/get-started/08_using_compose/
.. _test: https://docs.pytest.org/en/7.4.x/
.. _coverage: https://coverage.readthedocs.io/en/7.3.1/
.. _docs: https://www.sphinx-doc.org/en/master/
.. _pre-commit: https://pre-commit.com/
.. _ruff: https://docs.astral.sh/ruff/
