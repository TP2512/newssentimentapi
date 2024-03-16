from fastapi.testclient import TestClient
from main import app
import pytest


@pytest.fixture(scope='module')
def client_conn():
    """return a client connection with fastapi"""
    client = TestClient(app)
    return client


@pytest.mark.parametrize("username,password,response_code",
                         [('Tarkesh_2512', 'Tarkesh_251293', 200),
                          ('abcd', 'abcd', 401),
                          ('', '', 422)])
def test_login_scene(client_conn, username, password, response_code):
    response = client_conn.post("/login", data={"username": username, "password": password})
    assert response.status_code == response_code


def test_read_main(client_conn):
    response = client_conn.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Not Authorised"}


def test_missing_credentials(client_conn):
    response = client_conn.post("/login", data={})
    assert response.status_code == 422
    assert response.json() == {"detail": [{"type": "missing", "loc": ["body", "username"], "msg": "Field required",
                                           "input":None, "url": "https://errors.pydantic.dev/2.6/v/missing"},
                                          {"type": "missing", "loc": ["body", "password"], "msg": "Field required",
                                           "input": None, "url":"https://errors.pydantic.dev/2.6/v/missing"}]}


# without pytest
client2 = TestClient(app)


def test_successful_login():
    # Assuming your authentication endpoint is /login and accepts POST requests with username and password
    response = client2.post("/login", data={"username": "Tarkesh_2512", "password": "Tarkesh_251293"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_invalid_credentials():
    response = client2.post("/login", data={"username": "invalid_user", "password": "invalid_password"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
