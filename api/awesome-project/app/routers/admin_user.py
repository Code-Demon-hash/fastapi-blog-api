from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import AdminUserCreate, AdminUserRead, Token
from ..crud import create_admin, get_admin_by_name
from ..dependencies import get_db
from ..authentication import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


admin_router = APIRouter(prefix="/dmin", tags=["admin_users"])

@admin_router.post("/", response_model=AdminUserRead)
async def register_author(admin: AdminUserCreate, db: Session = Depends(get_db)):
    author_create = create_admin(db, admin.username)

@admin_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin_user = get_admin_by_name(db, form_data.username)
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