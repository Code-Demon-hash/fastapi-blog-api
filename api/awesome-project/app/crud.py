from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import UserModel, Authors, Blogs
from .schemas import UserCreate, BlogCreate, AuthorBase


def create_user(db: Session, user: UserCreate):
    user_db = UserModel(username=user.username, hashed_password=user.password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def get_user(db: Session, username: str):
    return db.execute(select(UserModel).where(UserModel.username == username)).scalar_one_or_none()

def create_author(db: Session, author: AuthorBase):
    author_db = Authors(name=author.name, email=author.email)
    db.add(author_db)
    db.commit()
    db.refresh(author_db)
    return author_db

def create_blog(db: Session, blog: BlogCreate):
    new_post = Blogs(title=blog.title,
                     content=blog.content,
                     author=blog.author) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post