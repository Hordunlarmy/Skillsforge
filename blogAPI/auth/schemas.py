from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
    username: str
    email: str
    exp: datetime
    authenticated: bool = True
