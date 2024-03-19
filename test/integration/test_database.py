import pytest
from database import database_connection as dc
from pymongo import errors
# from config import settings


# Check database connection
# @pytest.mark.asyncio
# async def test_get_database():
#     # Call the get_database function
#     db = await dc.get_database()
#     # Assertions
#     assert str(db) == f"AsyncIOMotorDatabase(Database(MongoClient(host=['{settings.mongodb_url}:27017'], " \
#                       "document_class=dict, tz_aware=False, connect=False, serverselectiontimeoutms=2000, " \
#                       "driver=DriverInfo(name='Motor', version='3.3.2', platform='asyncio')), " \
#                       "{settings.mongodb_database}))"


# Test insertion
@pytest.mark.asyncio
async def test_insert_data():
    # Prepare data for insertion
    data = {"username": "John_251293", "email": "john@example.com", "password": "T@rkesh2512"}
    # Insert data into the database
    test_db = await dc.get_database()
    await test_db["UserBase"].insert_one(data)
    # Verify that the data has been inserted
    result = await test_db["UserBase"].find_one({"email": "john@example.com"})
    assert result is not None
    assert result["username"] == "John_251293"


# Duplicate Key
@pytest.mark.asyncio
async def test_duplicate_data():
    # Prepare data for insertion
    data = {"username": "John_251293", "email": "john@example.com", "password": "T@rkesh2512"}
    # Insert data into the database
    test_db = await dc.get_database()
    try:
        await test_db["UserBase"].insert_one(data)
    except errors.DuplicateKeyError:
        assert True
    # assert result["username"] == "John_251293"


# Test update
@pytest.mark.asyncio
async def test_update_data():
    test_db = await dc.get_database()
    # Prepare data for update
    criteria = {"email": "john@example.com"}
    new_data = {"$set": {"email": "johnwick@example.com"}}
    # Update data in the database
    await test_db["UserBase"].update_one(criteria, new_data)
    # Verify that the data has been updated
    result = await test_db["UserBase"].find_one({"email": "johnwick@example.com"})
    assert result["email"] == "johnwick@example.com"


# Test deletion
@pytest.mark.asyncio
async def test_delete_data():
    test_db = await dc.get_database()
    # Prepare data for deletion
    criteria = {"username": "John_251293"}
    # Delete data from the database
    await test_db["UserBase"].delete_one(criteria)
    # Verify that the data has been deleted
    result = await test_db["UserBase"].find_one(criteria)
    assert result is None
