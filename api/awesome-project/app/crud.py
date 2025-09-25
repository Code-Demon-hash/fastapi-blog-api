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
    return db.query(UserModel).filter(UserModel.username == username).first()

def create_author(db: Session, author: AuthorBase):
    author_db = Authors(name=author.name, email=author.email)
    db.add(author_db)
    db.commit()
    db.refresh(author_db)
    return author_db

def create_blog(db: Session, blog: BlogCreate):
    new_blog = Blogs(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog