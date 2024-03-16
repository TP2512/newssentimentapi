import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def test_app():
    # Setup: Create a test client for the FastAPI app
    with TestClient(app) as client:
        yield client  # Test runs here


# Example test function using the test_app fixture
@pytest.mark.filterwarnings("ignore:.*The 'app' shortcut is now deprecated.*")
def test_read_main(test_app):
    # Test code using the FastAPI test client
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Not Authorised"}
