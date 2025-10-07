from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserSchema(BaseModel):
    username: str
    password: str
    disabled: bool | None = None

    class Config: 
        from_attrubutes = True
        use_enum_values = True

class UserCreate(BaseModel):
    password: str = Field(alias="password")
    username: str

    class Config:
        from_attributes = True
        use_enum_values = True

class UserResponse(BaseModel):
    id: int
    username: str 

    class Config: 
        from_attributes = True
        use_enum_values = True

class UserIn(BaseModel):
    id: int

    class Config: 
        from_attributes = True
        use_enum_values = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class BlogCreate(BaseModel):
    title: str
    content: str
    author: str

    class Config: 
        from_attributes = True
        
class BlogPost(BlogCreate):
    id: int
    created_at: datetime
    content: str
    
    class Config: 
        from_attributes = True

class BlogUpdate(BaseModel):

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    name: str
    email: EmailStr
    
    class Config: 
        from_attributes = True

class AuthorCreate(BaseModel):
    password: str

    class Config: 
        from_attributes = True

class Email(BaseModel):
    email: EmailStr

    class Config: 
        from_attributes = True