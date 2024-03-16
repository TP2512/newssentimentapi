from fastapi import APIRouter, Depends, status, HTTPException
from database import database_connection as dc
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import pymongo.errors
from loggers import configure_logger


logger = configure_logger()
router = APIRouter(tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_credential: OAuth2PasswordRequestForm = Depends(),
                     db: AsyncIOMotorDatabase = Depends(dc.get_database)):
    try:
        collection = db["UserBase"]
        user_by_email = await collection.find_one({"email": user_credential.username})
        user_by_username = await collection.find_one({"username": user_credential.username})
    except pymongo.errors.ConnectionFailure:
        logger.critical(f"database connection problem")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

    if user_by_email is not None:
        user = user_by_email
    elif user_by_username is not None:
        user = user_by_username
    else:
        user = None
    if not user:
        logger.error(f"Invalid credentials user not found:{user_credential.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not utils.verify(user_credential.password, user["password"]):
        logger.error(f"Invalid credentials wrong password:{user_credential.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"user_id": str(user["_id"])})
    logger.info(f"User Logged in User ID:{str(user['_id'])}")
    return {"access_token": access_token, "token_type": "Bearer"}
