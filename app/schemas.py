from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from .models import BlogStatus


class AdminUserCreate(BaseModel):
    model_config = ConfigDict(extra='ignore')

    username: str
    email_address: EmailStr
    password: str


class AdminUserRead(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: int
    username: str
    is_superuser: bool


class UserSchema(BaseModel):
    model_config = ConfigDict(extra='ignore')

    username: str
    disabled: bool | None = None


class UserCreate(BaseModel):
    model_config = ConfigDict(extra='ignore')

    username: str
    password: str 


class UserRead(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: int
    username: str 


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class AuthorBase(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: int
    username: str
    email_address: EmailStr
    

class AuthorCreate(BaseModel):
    model_config = ConfigDict(extra='ignore')

    username: str
    email_address: EmailStr
    password: str


class BlogCreate(BaseModel):
    model_config = ConfigDict(extra='ignore')

    title: str
    content: str
    status: BlogStatus

        
class BlogPost(BlogCreate):
    model_config = ConfigDict(extra='ignore')
    
    id: int
    author_id: int
    created_at: datetime
    content: str
    status: BlogStatus = BlogStatus.PUBLISHED
    

class BlogUpdate(BaseModel):
    model_config = ConfigDict(extra='ignore')


class CommentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blog_id: int
    content: str


class CommentRead(BaseModel):   
    model_config = ConfigDict(extra='ignore')

    id: int
    content: str
    user_id: int
    created_at: datetime


class UserReadBlog(BaseModel):
    model_config = ConfigDict(extra='ignore')

    creator: AuthorBase
    blog: BlogPost


class PostLike(BaseModel):
    model_config = ConfigDict(extra='ignore')

    blog_id: int


class ReadLikes(PostLike):
    model_config = ConfigDict(extra='ignore')

    id: int
    user_id: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    secret_key: str = Field('SECRET_KEY')