from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import AdminUser, UserModel, Authors, Blogs, Comments
from .schemas import AdminUserCreate, UserCreate, BlogCreate, AuthorCreate, CommentCreate




def create_user(db: Session, user: UserCreate):
    user_db = UserModel(username=user.username, hashed_password=user.password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def get_user_by_username(db: Session, username: str):
    user = db.execute(select(UserModel).where(UserModel.username == username)).scalar_one_or_none()
    print(f"Retrieved user for username '{username}': {user}")
    return user


def create_author(db: Session, author: AuthorCreate):
    author_db = Authors(username=author.username, 
                        email_address=author.email_address,
                        hashed_password=author.password)
    db.add(author_db)
    db.commit()
    db.refresh(author_db)
    return author_db

def get_author_by_name(db: Session, username: str):
    return db.execute(select(Authors).where(Authors.username == username)).scalar_one_or_none()


def create_a_blog(db: Session, blog: BlogCreate, author_id: int):
    new_post = Blogs(title=blog.title,
                     content=blog.content,
                     author_id=author_id,
                     status=blog.status) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def create_comment(db: Session, comment: CommentCreate, user_name: str):
    new_comment = Comments(blog_id=comment.blog_id,
                               content=comment.content,
                               users=user_name)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

#def create_like(db: Session, like: LikeCreate):
