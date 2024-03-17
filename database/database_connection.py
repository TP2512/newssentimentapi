from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError
from fastapi import HTTPException, status
from loggers import configure_logger
from dotenv import load_dotenv
import os
from config import settings

load_dotenv()
logger = configure_logger()
# MongoDB configuration
# noraml conf  "mongodb://localhost:27017"   "news_aggregator_db"
# MONGODB_URL = os.getenv("MONGODB_URL")
# DATABASE_NAME = os.getenv("MONGODB_DATABASE")
MONGODB_URL = str(settings.mongodb_url)
DATABASE_NAME = str(settings.mongodb_database)


# Dependency to get MongoDB database instance
async def get_database() -> AsyncIOMotorDatabase:
    try:
        client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=2000)
        db = client[DATABASE_NAME]
        await client.server_info()  # Test connection
        return db
    except ServerSelectionTimeoutError:
        logger.critical(f"database connection have issue {MONGODB_URL}:{DATABASE_NAME}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database Unavailable")

    # client = AsyncIOMotorClient(MONGODB_URL)
    # db = client[DATABASE_NAME]
    # return db

if __name__ == '__main__':
    import asyncio
    asyncio.run(get_database())
