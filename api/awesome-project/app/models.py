from datetime import datetime
from sqlalchemy import String, Integer, Column, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .core import Base



class UserModel(Base):
    __tablename__ = "user_account"      # name of the table in the database

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)


class Authors(Base):
    __tablename__ = "authors"       

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(), default=datetime.now())


class Blogs(Base):
    __tablename__ = "blogging_site"     

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    author = Column(String, nullable=False)