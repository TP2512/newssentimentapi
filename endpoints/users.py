from fastapi import HTTPException, status, Depends, Response, APIRouter
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from database.database_connection import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from models import schema as sc
from utils import utils, oauth2
from loggers import configure_logger


logger = configure_logger()
router = APIRouter()


# Create user
@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(user: sc.UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_exists = await db["UserBase"].find_one({"email": user.email})
    if user_exists:
        logger.warning(f"Email Already Exists:{user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")
    user_exists = await db["UserBase"].find_one({"username": user.username})
    if user_exists:
        logger.warning(f"Username Already Exists:{user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exists")
    user_dict = user.dict()
    hashed_password = utils.get_hashed_password(user_dict["password"])
    user_dict["password"] = hashed_password
    result = await db["UserBase"].insert_one(user_dict)
    return sc.UserResponse(id=str(result.inserted_id), username=user.username,
                           email=user.email, created_date=user_dict["created_date"])


# Get All Users
@router.get("/users", response_model=List[sc.UserResponse], status_code=status.HTTP_200_OK)
async def get_user(db: AsyncIOMotorDatabase = Depends(get_database),
                   current_user: dict = Depends(oauth2.get_current_user)):
    if "admin" != current_user["username"]:
        logger.warning(f"Not authorised to perform requested action i.e get all user details:{str(current_user['_id'])}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")
    users = []
    async for user_data in db["UserBase"].find():
        user_response = sc.UserResponse(id=str(user_data["_id"]), username=user_data["username"],
                                        email=user_data["email"], created_date=user_data["created_date"])
        users.append(user_response)
        logger.info(f"sent all users details for user:{str(current_user['_id'])}")
    return users


# Get User Details
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database),
                   current_user: dict = Depends(oauth2.get_current_user)):
    if user_id != str(current_user["_id"]):
        logger.error(f"not authorised user:{str(current_user['_id'])}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")
    user_data = await db["UserBase"].find_one({"_id": ObjectId(user_id)})
    if user_data:
        user_data["id"] = str(user_data["_id"])
        logger.info(f"sent users details of himself for user:{str(current_user['_id'])}")
        return sc.UserResponse(id=str(user_data["id"]), username=user_data["username"],
                               email=user_data["email"], created_date=user_data["created_date"])
    logger.error(f"User Not Found:{str(current_user['_id'])}")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


# Delete user
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database),
                      current_user: dict = Depends(oauth2.get_current_user)):
    if user_id != str(current_user["_id"]):
        logger.error(f"not authorised user:{str(current_user['_id'])}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")
    result = await db["UserBase"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        logger.error(f"User Not Found:{str(current_user['_id'])}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update user
@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: sc.UserCreate, db: AsyncIOMotorDatabase = Depends(get_database),
                      current_user: dict = Depends(oauth2.get_current_user)):
    if user_id != str(current_user["_id"]):
        logger.error(f"not authorised user:{str(current_user['_id'])}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")
    user_dict = user.dict()
    try:
        result = await db["UserBase"].replace_one({"_id": ObjectId(user_id)}, user_dict)
        if result.modified_count == 0:
            logger.error(f"User Not Found:{str(current_user['_id'])}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        logger.info(f"user's details of himself updated:{str(current_user['_id'])}")
        return {"message": "User updated"}
    except DuplicateKeyError:
        logger.error(f"Email already exists while updating:{str(current_user['_id'])}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Exists")
