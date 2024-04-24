from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import HTMLResponse
from engine import get_db, models, schemas
from engine.schemas import Post
from typing import List, Optional
from sqlalchemy.orm import Session

main = APIRouter()


@main.get("/", response_class=HTMLResponse)
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


@main.get("/posts/search/", response_model=List[Post])
def search_posts(
        query: Optional[str] = Query(...,
                                     description="Search posts by"
                                     " title or content"),
        db: Session = Depends(get_db)):
    """ Search for specific blog posts based on title or content """

    query = f"%{query}%"
    posts = db.query(models.Post).filter(
        (models.Post.title.like(query)) | (models.Post.content.like(query))
    ).all()
    if not posts:
        raise HTTPException(
            status_code=404, detail="No post matches your query")
    return posts
