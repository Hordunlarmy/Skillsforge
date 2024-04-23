#!/usr/bin/python3
""" A Blogging Platform API """
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from engine import get_db, create_db, models
from engine.schemas import UserBase, UserCreate,  UserLogin
from auth.secure import (Token, get_password_hash, verify_password,
                         authenticate_user, create_access_token,
                         ACCESS_TOKEN_EXPIRE_MINUTES)
from datetime import timedelta
from sqlalchemy.orm import Session

app = FastAPI()
create_db()


@app.get("/", response_class=HTMLResponse)
async def home():
    """ Returns an html content """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Blogging Platform API</title>
    </head>
    <body>
        <h1>MY BLOGGING PLATFORM API</h1>
        <p>Welcome to my blogging platform API. Use my API to create, read,
        update, and delete blog posts and comments.</p>
    </body>
    </html>
    """


@app.post("/signup/", response_model=UserBase)
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


@app.post("/login/", response_model=Token)
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


# @app.post("/posts/", response_model=models.Post)
# async def create_post_api(db: Session = Depends(get_db)):
#    pass
#
#
# @app.get("/posts/", response_model=List[Post])
# async def read_posts():
#    pass
#
#
# @app.get("/posts/{post_id}", response_model=Post)
# async def read_post(post_id: int):
#    pass
#
#
# @app.put("/posts/{post_id}", response_model=Post)
# async def update_post_api(post_id: int, post: PostUpdate):
#    pass
#
#
# @app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post_api(post_id: int):
#    pass
#    return {"detail": "Post deleted successfully"}
if __name__ == "__main__":
    uvicorn.run("main:app", reload="True")
