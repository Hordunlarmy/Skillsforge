from fastapi import Depends, HTTPException, APIRouter, Path
from fastapi.responses import HTMLResponse
from engine import get_db, models, schemas
from engine.schemas import Comment, CommentCreate
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from auth import user_dependency


comment = APIRouter()


@comment.post("/comments/", response_model=Comment)
async def create_comment(current_user: user_dependency, comment: CommentCreate,
                         user_id: str = Path(...,
                                             description="The post user ID"),
                         post_id: str = Path(...,
                                             description="The ID of the"
                                             " post to comment on"),
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
async def read_comments(current_user: user_dependency,
                        db: Session = Depends(get_db)):
    """ Return a list of all comments """

    comments = db.query(models.Comment).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found")
    return [schemas.Comment.from_orm(comment) for comment in comments]


@comment.get("/comments/{id}", response_model=Comment)
async def read_comment(current_user: user_dependency,
                       comment_id: str = Path(...,
                                              description="The ID of the"
                                              " comment to retrieve"),
                       db: Session = Depends(get_db)):
    """ Retrieve a comment """

    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    return comment


@comment.put("/comments/{id}", response_model=Comment)
async def update_comment(current_user: user_dependency, comment: CommentCreate,
                         comment_id: str = Path(...,
                                                description="The ID of the"
                                                " comment to update"),
                         db: Session = Depends(get_db)):

    """ Update a comment """

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


@comment.delete("/comments/{id}")
async def delete_comment(current_user: user_dependency,
                         comment_id: str = Path(...,
                                                description="The ID of the"
                                                " comment to delete"),
                         db: Session = Depends(get_db)):
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
