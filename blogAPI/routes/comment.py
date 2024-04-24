from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from engine import get_db, models, schemas
from engine.schemas import Comment, CommentCreate
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session


comment = APIRouter()


@comment.post("/comments/", response_model=Comment)
async def create_comment(user_id: str, post_id: str, comment: CommentCreate,
                         db: Session = Depends(get_db)):
    """ route to create validated comments """

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        new_comment = models.Comment(
            user_id=user_id, post_id=post.id, text=comment.text)
    else:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e))

    return new_comment


@comment.get("/comments/", response_model=List[Comment])
async def read_comments(db: Session = Depends(get_db)):
    """ Return a list of all comments """
    comments = db.query(models.Comment).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found")
    return [schemas.Comment.from_orm(comment) for comment in comments]


@comment.get("/comments/{comment_id}", response_model=Comment)
async def read_comment(comment_id: str, db: Session = Depends(get_db)):
    """ Return a comment by its id """

    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    return comment


@comment.put("/comments/{comment_id}", response_model=Comment)
async def update_comment(comment_id: str, comment: CommentCreate,
                         db: Session = Depends(get_db)):
    """ Update a comment by its id and return updated comment """

    comment_to_update = db.query(models.Comment).filter(
        models.Comment.id == comment_id).first()

    if not comment_to_update:
        raise HTTPException(status_code=404, detail="comment doesnt exist")

    comment_to_update.text = comment.text
    comment_to_update.date_commented = datetime.utcnow()

    try:
        db.commit()
        db.refresh(comment_to_update)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return comment_to_update


@comment.delete("/comments/{comment_id}")
async def delete_comment(comment_id: str, db: Session = Depends(get_db)):
    """ Delete a comment by its id """

    comment_to_delete = db.query(models.Comment).filter(
        models.Comment.id == comment_id).first()

    if comment_to_delete is None:
        raise HTTPException(status_code=404, detail="comment doesnt exist")
    deleted_id = comment_to_delete.id

    try:
        db.delete(comment_to_delete)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e))

    return {"message": f"comment {deleted_id} deleted successfully"}
