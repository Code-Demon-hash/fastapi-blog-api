from fastapi import FastAPI
from .routers import users, blogs
from .core import Base, engine
from contextlib import asynccontextmanager



Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)



app = FastAPI(lifespan=lifespan)


app.include_router(users.router)
app.include_router(blogs.router)