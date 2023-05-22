import pytest
from fastapi.testclient import TestClient

from app.main import app


# Here inject Postgres connection if needed
@pytest.fixture(scope="module")
def test_app():
    test_client = TestClient(app)
    yield test_client
