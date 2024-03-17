from jose import JWTError, jwt
from datetime import datetime, timedelta
from models import schema as sc
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database.database_connection import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from loggers import configure_logger
import os
from dotenv import load_dotenv
from config import settings
# used symmetric cryptography using HS256 algo


load_dotenv()
logger = configure_logger()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# SECRET_KEY = os.getenv("SECRET_KEY")             # "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # private key
# ALGORITHM = os.getenv("ALGORITHM")               # "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")     # "60"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            logger.error("token is missing")
            raise credentials_exception
        token_data = sc.TokenData(id=id)
    except JWTError:
        logger.error("getting current user failed due to token or other parameter")
        raise credentials_exception
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(get_database)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user_data = await db["UserBase"].find_one({"_id": ObjectId(token.id)}, {"password": 0})
    if not user_data:
        logger.error("token invalid")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token Invalid")
    return user_data
