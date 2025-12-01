from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import AdminUser, UserModel, Authors, Blogs, Comments, Likes
from .schemas import AdminUserCreate, UserCreate, BlogCreate, AuthorCreate, CommentCreate, LikePost



def create_admin(db: Session, admin: AdminUserCreate):
    admin_db = AdminUser(username=admin.username,
                         email_address=admin.email_address,
                         hashed_password=admin.password)
    db.add(admin_db)
    db.commit()
    db.refresh(admin_db)
    return admin_db

def get_admin_by_name(db: Session, username: str):
    return db.execute(select(AdminUser).where(AdminUser.username == username)).scalar_one_or_none()


def create_user(db: Session, user: UserCreate):
    user_db = UserModel(username=user.username, hashed_password=user.password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def get_user_by_username(db: Session, username: str):
    return db.execute(select(UserModel).where(UserModel.username == username)).scalar_one_or_none()


def create_author(db: Session, author: AuthorCreate, admin_user_id: int):
    author_db = Authors(username=author.username, 
                        email_address=author.email_address,
                        hashed_password=author.password,
                        admin_user_id=admin_user_id)
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


def is_admin(db: Session, admin: AdminUser):
    verify_user = db.execute(select(AdminUser).where(AdminUser.id == admin.id)).scalar_one_or_none()
    if not verify_user:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,
                             detail="Not authorized to perform requested action")
    return verify_user


def create_comment(db: Session, blog_id: int, comment: CommentCreate):
    new_comment = Comments(blog_id=blog_id,
                           user_id=comment.user_id,
                           content=comment.content)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comment_by_blog_id(db: Session, blog_id: int):
    return db.execute(select(Comments).where(Comments.blog_id==blog_id)).scalar_one_or_none()


def create_like_post(db: Session, like: LikePost, blog_id: int):
    like_on_post = Likes(user_id=like.user_id,
                         blog_id=blog_id)
    db.add(like_on_post)
    db.commit()
    db.refresh(like_on_post)
    return like_on_post