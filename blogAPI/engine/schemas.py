from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CommentBase(BaseModel):
    text: str


class Comment(CommentBase):
    id: int
    post_id: int
    created_date: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str


class Post(PostBase):
    id: int
    created_date: datetime
    comments: List[Comment] = []

    class Config:
        from_attributes = True
