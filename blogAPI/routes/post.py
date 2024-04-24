from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from engine import get_db, models, schemas
from engine.schemas import Post, PostCreate
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

post = APIRouter()


@post.post("/posts/", response_model=Post)
async def create_post(user_id: str, post: PostCreate,
                      db: Session = Depends(get_db)):
    """ route to create validated posts """

    user = db.query(models.User).filter(models.User.id == user_id).first()
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
            status_code=400, detail=str(e))

    return new_post


@post.get("/posts/", response_model=List[Post])
async def read_posts(db: Session = Depends(get_db)):
    """ Return a list of all posts """

    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return [schemas.Post.from_orm(post) for post in posts]


@post.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: str, db: Session = Depends(get_db)):
    """ Return a post by its id """

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@post.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: str, post: PostCreate,
                      db: Session = Depends(get_db)):
    """ Update a post by its id and return updated post """

    post_to_update = db.query(models.Post).filter(
        models.Post.id == post_id).first()
    post_to_update.title = post.title
    post_to_update.content = post.content
    post_to_update.date_posted = datetime.utcnow()

    try:
        db.commit()
        db.refresh(post_to_update)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e))

    return post_to_update


@post.delete("/posts/{post_id}")
async def delete_post(post_id: str, db: Session = Depends(get_db)):
    """ Delete a post by its id """

    post_to_delete = db.query(models.Post).filter(
        models.Post.id == post_id).first()

    if post_to_delete is None:
        raise HTTPException(status_code=404, detail="Post doesnt exist")
    deleted_id = post_to_delete.id

    try:
        db.delete(post_to_delete)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e))

    return {"message": f"Post {deleted_id} deleted successfully"}
