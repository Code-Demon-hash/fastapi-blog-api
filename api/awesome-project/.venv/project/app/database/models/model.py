from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Column
from database.database import Base


class Base(DeclarativeBase):
    pass


class CreateUser(Base):
    __tablename__ = "user_account"

    id = Column(Integer, Primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)