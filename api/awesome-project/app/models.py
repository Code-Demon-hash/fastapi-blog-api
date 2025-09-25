from datetime import datetime
from sqlalchemy import String, Integer, Column, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
# import the Base class which is typically the declarative base for SQLAlchemy models
from .core import Base



# define a UserModel class representing a user_account in the database
class UserModel(Base):
    __tablename__ = "user_account"      # name of the table in the database

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)


# defining Authors class representing authors blogs
class Authors(Base):
    __tablename__ = "authors"       

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(), default=datetime.now())


# defining Blogs class representing blog posts
class Blogs(Base):
    __tablename__ = "blogging_site"     

    id = Column(Integer, primary_key=True)
    content = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    author = Column(String, nullable=False)