from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..schemas import UserCreate, UserRead, UserSchema, Token
from ..crud import create_user, get_user_by_username
from ..dependencies import get_db
from .security.user_authentication import create_access_token, get_current_active_user, get_password_hash, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES 
from ..models import UserModel


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create_account", response_model=UserRead)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user_create = create_user(db, user)
    return user_create

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
        )
    return Token(access_token=access_token, token_type="bearer") 
   

@router.get("/user_id")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_item = db.get(UserModel, user_id)
    if not user_item:
        raise HTTPException(
            status_code=404,
            detail="User not found"
            )
    return user_item


@router.get("/me")
def read_current_user(current_user: UserSchema = Depends(get_current_active_user)):
    return current_user
