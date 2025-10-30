from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from ..models import Authors
from ..schemas import AuthorBase, AuthorCreate, Token
from ..crud import create_author
from ..dependencies import get_db
from .security.author_authentication import create_access_token, authenticate_author, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/author", tags=["authors"])

@router.post("/signup", response_model=AuthorBase)
async def register_author(author: AuthorCreate, db: Session = Depends(get_db)):
    existing_user = db.execute(select(Authors).where(Authors.username==author.username)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered")
    hashed_password = get_password_hash(author.password)
    author.password = hashed_password
    author_create = create_author(db, author)
    return author_create

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    author = authenticate_author(db, form_data.username, form_data.password)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or Password",
            headers={"WWW-Authenticate": "Bearer"}
            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": author.username}, expires_delta=access_token_expires
        )
    return Token(access_token=access_token, token_type="bearer")
   

'''
@router.get("/get_author_id", response_model=AuthorBase)
def read_author_works(author_id, db: Session = Depends(get_db)):
    author = get_author_by_name(db, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Author not found")
    fetch_blogs_by_author = get_blogs_by_author_id(db, author_id)
    return fetch_blogs_by_author
'''
    