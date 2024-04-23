from fastapi import Depends, HTTPException, APIRouter
from engine import get_db, models, schemas
from engine.schemas import UserBase, User, UserCreate, UserLogin
from auth.secure import (Token, get_password_hash, verify_password,
                         authenticate_user, create_access_token,
                         ACCESS_TOKEN_EXPIRE_MINUTES)
from datetime import timedelta
from typing import List
from sqlalchemy.orm import Session


user = APIRouter()


@user.post("/signup/", response_model=User)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """ Returns user id """

    new_user = models.User(username=user.username, email=user.email,
                           password=get_password_hash(user.password))
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Error while creating user")

    return new_user


@user.post("/login/", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Validate And Authenticate User"""

    old_user = authenticate_user(user.email, user.password, db)
    if not old_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": old_user.id, "username": old_user.username,
              "email": old_user.email},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user.get("/users/", response_model=List[User])
async def read_users(db: Session = Depends(get_db)):
    """ Returns All Users"""

    users_data = db.query(models.User).all()
    if not users_data:
        raise HTTPException(status_code=404, detail="No users found")
    return [schemas.User.from_orm(user) for user in users_data]
