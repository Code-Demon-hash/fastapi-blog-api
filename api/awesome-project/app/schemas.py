# import necessary modules from pydantic for data validation and modeling
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


class UserSchema(BaseModel):
    username: str
    password: str
    disabled: bool | None = None

    # Configuration class for addtional model options
    class Config: 
        from_attrubutes = True
        use_enum_values = True

class UserCreate(BaseModel):
    password: str = Field(alias="password")
    username: str

    class Config:
        from_attributes = True
        use_enum_values = True

# Schema for user_data returned in responses
class UserResponse(BaseModel):
    id: int
    username: str 

    class Config: 
        from_attributes = True
        use_enum_values = True

# Schema for representing a user input, possibily during login or other operations
class UserIn(BaseModel):
    id: int

    class Config: 
        from_attributes = True
        use_enum_values = True

# Schema for authentication tokens
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data, typically used for decoding token payloads
class TokenData(BaseModel):
    username: str

class BlogCreate(BaseModel):
    title: str
    content: str
    author: str

    class Config: 
        from_attributes = True
        
class BlogResponse(BlogCreate):
    id: int
    created_at: datetime
    author_id: int
    
    class Config: 
        from_attributes = True

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