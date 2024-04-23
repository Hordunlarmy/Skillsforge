#!/usr/bin/python3
""" A Blogging Platform API """
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from engine import get_db, create_db, models, schemas
from engine.schemas import (UserBase,
                            User, Post, Comment, UserCreate,  UserLogin,
                            PostCreate, CommentCreate)
from auth.secure import (Token, get_password_hash, verify_password,
                         authenticate_user, create_access_token,
                         ACCESS_TOKEN_EXPIRE_MINUTES)
from datetime import timedelta
from typing import List
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


@app.post("/signup/", response_model=User)
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


@app.get("/get_users/", response_model=List[User])
async def get_users(db: Session = Depends(get_db)):
    """ Returns All Users"""

    users_data = db.query(models.User).all()
    if not users_data:
        raise HTTPException(status_code=404, detail="No users found")
    return [schemas.User.from_orm(user) for user in users_data]


@app.post("/posts/", response_model=Post)
async def create_post(user: UserBase, post: PostCreate, db: Session = Depends(get_db)):
    """ route to create validated posts """

    user = db.query(models.User).filter(models.User.id == user.id).first()
    if user:
        new_post = models.Post(
            user_id=user.id, title=post.title, content=post.content)
    else:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Error while creating post")

    return new_post

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
