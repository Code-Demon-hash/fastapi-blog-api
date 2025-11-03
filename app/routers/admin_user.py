from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import AdminUserCreate, AdminUserRead, Token
from ..crud import create_admin, get_admin_by_name
from ..dependencies import get_db
from .security.admin_authentication import authenticate_admin, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES




admin_router = APIRouter(prefix="/admin", tags=["admins"])



@admin_router.post("/", response_model=AdminUserRead)
async def register_admin(admin: AdminUserCreate, db: Session = Depends(get_db)):
    existing_user = get_admin_by_name(db, admin.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered")
    hashed_password = get_password_hash(admin.password)
    admin.password = hashed_password
    admin_create = create_admin(db, admin)
    return admin_create


@admin_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin_user = authenticate_admin(db, form_data.username, form_data.password)
    if not admin_user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or Password",
            headers={"WWW-Authenticate": "Bearer"}
            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin_user.username}, expires_delta=access_token_expires
        )
    return Token(access_token=access_token, token_type="bearer")