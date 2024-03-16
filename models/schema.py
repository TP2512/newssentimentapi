from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional, Text
from datetime import datetime


class NewsInput(BaseModel):
    news_article: Text


class NewsResponse(BaseModel):
    sentiment: str


class NewsFeed(BaseModel):
    id: Optional[int]
    title: Optional[str]
    news: Optional[str]
    created_date: Optional[str]

    # noinspection PyMethodParameters
    @field_validator('news')
    def check_content_length(cls, v):
        if v and len(v.split()) > 200:
            raise ValueError("Content should not exceed 200 words")
        return v

    # noinspection PyMethodParameters
    @field_validator('*')
    def check_at_least_one_input_given(cls, values):
        if not any(values.values()):
            raise ValueError("'At least one input field (title, news, created_date) must be provided")
        return values


# Pydantic model for user data
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_date: datetime = datetime.now()

    # noinspection PyMethodParameters
    @field_validator('username')
    def validate_username(cls, v):
        if not any(char.isalnum() for char in v):
            raise ValueError('Username must contain at least one alphanumeric character')
        if not any(char.isascii() and not char.isalnum() for char in v):
            raise ValueError('Username must contain at least one special character')
        if len(v) < 8:
            raise ValueError('Username must be at least 8 characters long')
        return v

    # noinspection PyMethodParameters
    @field_validator('password')
    def validate_password(cls, v, **kwargs):
        if not v:
            raise ValueError('Password cannot be Null')
        if not any(char.isascii() and not char.isalnum() for char in v):
            raise ValueError('password must contain at least one special character')
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters long')
        if v == kwargs.get("username"):
            raise ValueError("Password cannot be the same as username")
        return v


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    created_date: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
