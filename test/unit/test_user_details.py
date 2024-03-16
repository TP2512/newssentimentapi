# Contains tests for endpoints related to fetching user details.
from fastapi import HTTPException, status
from bson import ObjectId
from endpoints.users import get_user
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app
import pytest


# using fixture
@pytest.fixture
async def mock_user_data():
    return {
        "_id": ObjectId("65ea1ca599b9a1b3aa159dc1"),
        "username": "test_user",
        "email": "test@example.com",
        "created_date": "2024-03-15"
    }


@pytest.fixture
async def mock_db(mock_user_data):
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = mock_user_data
    mock_db = AsyncMock()
    mock_db.__getitem__.return_value = mock_collection
    return mock_db


@pytest.fixture
async def mock_current_user():
    return {"_id": ObjectId("65ea1ca599b9a1b3aa159dc1")}


@pytest.mark.asyncio
async def test_get_user(mock_db, mock_current_user):
    response = await get_user("65ea1ca599b9a1b3aa159dc1", db=mock_db, current_user=mock_current_user)
    assert response.id == "65ea1ca599b9a1b3aa159dc1"

    with pytest.raises(HTTPException) as exc_info:
        await get_user("65ea1ca599b9a1b3aa159dc2", db=mock_db, current_user=mock_current_user)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    # Test user not found
    mock_db.return_value.find_one.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        await get_user("65ea1ca599b9a1b3aa159dc1", db=mock_db, current_user=mock_current_user)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
# --------------------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_user():
    mock_collection = AsyncMock()
    mock_user_data = {
        "_id": ObjectId("65ea1ca599b9a1b3aa159dc1"),
        "username": "test_user",
        "email": "test@example.com",
        "created_date": "2024-03-15"
    }
    mock_collection.find_one.return_value = mock_user_data
    mock_db = AsyncMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_current_user = {"_id": ObjectId("65ea1ca599b9a1b3aa159dc1")}
    response = await get_user("65ea1ca599b9a1b3aa159dc1", db=mock_db, current_user=mock_current_user)
    assert response.id == "65ea1ca599b9a1b3aa159dc1"

    with pytest.raises(HTTPException) as exc_info:
        await get_user("65ea1ca599b9a1b3aa159dc2", db=mock_db, current_user=mock_current_user)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    # Test user not found
    mock_collection.find_one.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        await get_user("65ea1ca599b9a1b3aa159dc1", db=mock_db, current_user=mock_current_user)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.fixture(scope='module')
def client_conn():
    """return a client connection with fastapi"""
    client = TestClient(app)
    return client


def test_get_user_wrong_user_id_without_token(client_conn):
    response = client_conn.get("/users/1223")
    assert response.json() == {'detail': 'Not authenticated'}
    assert response.status_code == 401
