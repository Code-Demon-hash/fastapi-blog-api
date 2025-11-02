from fastapi import FastAPI
from .routers import authors, admin_user, users, blogs, comments, likes
from .core import Base, engine
from contextlib import asynccontextmanager



Base.metadata.create_all(bind=engine)



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)



app = FastAPI(lifespan=lifespan)



app.include_router(admin_user.admin_router)
app.include_router(authors.router)
app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(comments.router)
app.include_router(likes.router)