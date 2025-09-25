from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import BlogCreate, BlogResponse, UserSchema
from ..authentication import get_current_user
from ..dependencies import get_db
from ..models import Blogs

router = APIRouter(prefix="/blogs", tags=["blogs"])

@router.post("/", response_model=BlogResponse)
def create_blog_post(
    blog: BlogCreate, 
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user), # assuming you have authentication
):
    new_blog = Blogs(
        title=blog.title,
        content=blog.content,
        author=current_user.username  # set author automatically
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
