import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def server_api() -> TestClient:
    """
    FastAPI TestClient fixture.
    :return:
    """
    with TestClient(app) as c:
        yield c
