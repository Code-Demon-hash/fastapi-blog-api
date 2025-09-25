from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from ..schemas import UserCreate, UserResponse, UserSchema, Token
from ..crud import create_user, get_user
from ..dependencies import get_db
from ..authentication import create_access_token, verify_password, get_password_hash, get_current_user, get_current_active_user, oauth2_scheme, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models import UserModel


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create_account", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data['hashed_password'] = hashed_password
    user_data.pop('password', None)
    new_user = create_user(db, user)
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or Password"
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
