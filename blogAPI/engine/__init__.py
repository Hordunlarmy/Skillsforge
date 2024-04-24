#!/usr/bin/python3
""" configure database with sqlalchemy """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

SQLALCHEMY_DATABASE_URL = config("database", default="sqlite:///./blog.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    # Create database if it doesnt already exist
    from engine import models
    models.Base.metadata.create_all(bind=engine)
