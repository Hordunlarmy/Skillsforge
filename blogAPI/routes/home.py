from fastapi import APIRouter
from fastapi.responses import HTMLResponse

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
