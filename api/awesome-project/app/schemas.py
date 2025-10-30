from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .models import BlogStatus


class AdminUserCreate(BaseModel):
    username: str
    password: str

    class Config: 
        orm_mode = True

class AdminUserRead(BaseModel):
    id: int
    username: str
    is_superuser: bool

class UserSchema(BaseModel):
    username: str
    password: str
    disabled: bool | None = None

    class Config: 
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str 

    class Config:
        orm_mode = True

class UserRead(BaseModel):
    id: int
    username: str 

    class Config: 
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    id: int
    username: str
    email_address: EmailStr
    
    class Config: 
        orm_mode = True

class AuthorCreate(BaseModel):
    username: str
    email_address: EmailStr
    password: str

    class Config: 
        orm_mode = True

class AuthorRead(BaseModel):
    id: int
    username: str
    email_address: EmailStr

class BlogCreate(BaseModel):
    title: str
    content: str
    status: BlogStatus

    class Config: 
        orm_mode = True
        
class BlogPost(BlogCreate):
    id: int
    author_id: int
    created_at: datetime
    content: str
    status: BlogStatus
    
    class Config: 
        orm_mode = True

class BlogUpdate(BaseModel):

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    blog_id: int
    content: str
    
    class Config: 
        orm_mode = True

class CommentRead(BaseModel):   
    id: int
    content: str
    users: List[UserRead] = []
    created_at: datetime

    class Config:
        orm_mode = True

class BlogRead(BaseModel):
    id: int
    title: str
    content: str
    
    class Config:
        orm_mode = True

class LikeCreate(BaseModel):
    user_id: int
    blog_id: Optional[int] = None
    comment_id: Optional[int] = None

class ReadLikes(BaseModel):
    id: int
    user_id: int
    user_name: str
    blog_id: Optional[int] = None
    comment_id: Optional[int] = None

    class Config:
        orm_mode = True


