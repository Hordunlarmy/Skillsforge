from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime


class User(BaseModel):
    """ Base User Model"""
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(User):
    """ Pydantic validation for user data creation"""

    password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserData(BaseModel):
    """ User Base Model"""
    id: str
    username: str
    email: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """ User Login Blueprint"""

    email: EmailStr
    password: str


class CommentCreate(BaseModel):
    """ pydantic model for comments """

    text: str


class Comment(BaseModel):
    """ response model for comments route """

    id: str
    post_id: str
    text: str
    date_posted: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    """ Pydantic model for creating posts """
    title: str
    content: str


class Post(BaseModel):
    """ pydantic response model for post route"""

    id: str
    user_id: str
    title: str
    content: str
    date_posted: datetime
    comments: List[Comment] = []

    class Config:
        from_attributes = True
