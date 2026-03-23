from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from .routers import authors, admin_user, users, blogs, comments, likes
from .core import Base, engine
from .enums import BlogStatus
from .models import Blog
from .dependencies import get_db
from .routers.security.author_authentication import settings
from contextlib import asynccontextmanager



Base.metadata.create_all(bind=engine)



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)



app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

templates = Jinja2Templates(directory="frontend/templates")



app.include_router(admin_user.admin_router)
app.include_router(authors.router)
app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(comments.router)
app.include_router(likes.router)




@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Blog).options(selectinload(Blog.author)).filter(Blog.status==BlogStatus.PUBLISHED).order_by(Blog.created_at.desc()).all()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request, "posts": posts}
    )

@app.get("/", include_in_schema=False)
async def register(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
        {"title": "Register"},
    )