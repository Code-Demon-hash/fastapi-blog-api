from __future__ import annotations

from typing import List
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .enums import BlogStatus
from .core import Base



class AdminUser(Base):
    __tablename__ = "admin_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email_address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=True)
    author: Mapped[List["Authors"]] = relationship(back_populates="admin_user")


class Authors(Base):
    __tablename__ = "authors"     

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)  
    email_address: Mapped[str] = mapped_column(String, unique=True, nullable=False)   
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)   
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    admin_user_id: Mapped[int] = mapped_column(ForeignKey("admin_user.id"))
    admin_user: Mapped["AdminUser"] = relationship(back_populates="author")
    blog: Mapped[List["Blogs"]] = relationship(back_populates="author")


class UserModel(Base):
    __tablename__ = "users"    

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    like: Mapped[List["Likes"]] = relationship(back_populates="user")
    comment: Mapped[List["Comments"]] = relationship(back_populates="user")
    reads: Mapped[List["UserReadsBlogs"]] = relationship(
        back_populates="user"
    )


class Blogs(Base):
    __tablename__ = "blogs"    

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False) 
    title: Mapped[str] = mapped_column(String, nullable=False) 
    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Authors"] = relationship(back_populates="blog")
    like: Mapped[List["Likes"]] = relationship(back_populates="blog")
    comment: Mapped[List["Comments"]] = relationship(back_populates="blog")
    readers: Mapped[List["UserReadsBlogs"]] = relationship(
        back_populates="blog"
    )
    status: Mapped[BlogStatus] = mapped_column(Enum(BlogStatus), server_default="DRAFT")


class UserReadsBlogs(Base):
    __tablename__ = "user_reads_blog"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )
    blog_id: Mapped[int] = mapped_column(
        ForeignKey("blogs.id"), primary_key=True
    )
    user: Mapped["UserModel"] = relationship(back_populates="reads")
    blog: Mapped["Blogs"] = relationship(back_populates="readers")


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    like: Mapped[List["Likes"]] = relationship(back_populates="comment")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="comment")
    blog_id: Mapped[int] = mapped_column(ForeignKey("blogs.id"))
    blog: Mapped["Blogs"] = relationship(back_populates="comment")


class Likes(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"))
    comment: Mapped["Comments"] = relationship(back_populates="like")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="like")
    blog_id: Mapped[int] = mapped_column(ForeignKey("blogs.id"))
    blog: Mapped["Blogs"] = relationship(back_populates="like")