from fastapi import FastAPI, status
from models.model import Base, CreateUser
from users.user import UserSchema
from app.engine import Session, engine



app = FastAPI()

@app.post("/adduser/", status_code=status.HTTP_201_CREATED)
async def add_user(request: UserSchema):
    get_user = CreateUser(request.name, request.password)
    Session.add(get_user)
    Session.commit()
    return get_user