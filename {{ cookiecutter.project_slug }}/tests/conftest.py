import asyncio
import sys
from asyncio import AbstractEventLoop
from collections.abc import Callable, Iterator

import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    """
    Create an event loop.

    `pytest-async-sqlalchemy` shares a database connection between tests
    for performance reasons, but the default `event_loop` fixture defined by
    `pytest-asyncio` is function scoped;
    it kills the database connection after each test.

    :return:
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _database_url() -> str:
    """
    Build a database url.

    :return:
    """
    ...
    return ""


@pytest.fixture(scope="session")
def init_database() -> Callable[..., None]:
    """
    Initialize a test fixture using sqlalchemy.

    :return:
    """
    from src.app.db.base_class import Base  # isort: skip

    return Base.metadata.create_all


@pytest.fixture(scope="session")
def server_api() -> Iterator[TestClient]:
    """
    FastAPI TestClient fixture.

    :return:
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_response() -> Iterator[aioresponses]:
    """
    Async HTTP response mocker.

    :return:
    """
    with aioresponses() as m:
        yield m
