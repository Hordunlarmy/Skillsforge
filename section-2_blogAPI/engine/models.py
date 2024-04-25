import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from engine import Base


class User(Base):
    """Blueprint for Users attributes"""

    __tablename__ = "user"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    posts = relationship("Post", back_populates="author",
                         cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="commenter", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(Base):
    """Class to create instances of user posts"""

    __tablename__ = "post"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    date_posted = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    author = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(Base):
    """Class to create instances of comments"""

    __tablename__ = 'comment'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(Text, nullable=False)
    date_posted = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(String, ForeignKey(
        'post.id', ondelete='CASCADE'), nullable=False)
    commenter = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"Comment('{self.id}', '{self.text}', '{self.date_posted}')"
