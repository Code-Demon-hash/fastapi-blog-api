from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import AuthorBase, AuthorCreate, Token
from ..crud import create_author, get_author_by_name
from ..dependencies import get_db
from .security.author_authentication import create_access_token, authenticate_author, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/author", tags=["authors"])

@router.post("/signup", response_model=AuthorBase)
async def register_author(author: AuthorCreate, db: Session = Depends(get_db)):
    existing_user = get_author_by_name(db, author.username)
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
