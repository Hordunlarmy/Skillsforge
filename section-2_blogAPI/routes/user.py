from fastapi import Depends, HTTPException, APIRouter, status, Path
from engine import get_db, models, schemas
from engine.schemas import UserData, User, UserCreate, UserLogin
from auth import user_dependency, oauth2
from auth.schemas import Token, TokenData
from auth.secure import (get_password_hash, verify_password,
                         authenticate_user, create_access_token,
                         current_user, ACCESS_TOKEN_EXPIRE_MINUTES)
from datetime import timedelta
from typing import List, Annotated
from sqlalchemy.orm import Session


user = APIRouter()
user_dependency = Annotated[TokenData, Depends(current_user)]


@user.post("/signup/", response_model=User)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """ Create and Returns new user """

    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (
            models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username or email already exists."
        )

    new_user = models.User(username=user.username, email=user.email,
                           password=get_password_hash(user.password))
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e))

    return new_user


@user.post("/login/", response_model=Token)
async def login(user: oauth2, db: Session = Depends(get_db)):
    """Validate And Authenticate User"""

    old_user = authenticate_user(user.username, user.password, db)
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


@user.get("/users/", response_model=List[UserData])
async def read_users(current_user: user_dependency,
                     db: Session = Depends(get_db)):
    """ Returns All Users"""

    users_data = db.query(models.User).all()
    if not users_data:
        raise HTTPException(status_code=404, detail="No users found")
    return [schemas.UserData.from_orm(user) for user in users_data]


@user.delete("/users/{user_id}")
async def delete_user(current_user: user_dependency,
                      user_id: str = Path(...,
                                          description="The ID of the"
                                          " User to delete"),
                      db: Session = Depends(get_db)):
    """ Delete a user account """
    user_to_delete = db.query(models.User).filter(
        models.User.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    if user_to_delete.id != current_user.id:
        raise HTTPException(
            status_code=404, detail="You can't delete another user's account")

    try:
        db.delete(user_to_delete)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"User {user_to_delete.id} deleted successfully"}
