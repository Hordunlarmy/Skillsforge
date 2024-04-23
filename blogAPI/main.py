#!/usr/bin/python3
""" A Blogging Platform API """
import uvicorn
import routes
from fastapi import FastAPI
from engine import create_db

app = FastAPI()
create_db()

app.include_router(routes.main)
app.include_router(routes.user)
app.include_router(routes.post)


if __name__ == "__main__":
    uvicorn.run("main:app", reload="True")
