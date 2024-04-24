from .secure import current_user
from .schemas import TokenData
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

oauth2 = Annotated[OAuth2PasswordRequestForm, Depends()]
user_dependency = Annotated[TokenData, Depends(current_user)]
