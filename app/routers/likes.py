from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Likes, Blogs
from ..crud import create_like_post
from ..schemas import PostLike, ReadLikes
from .security.user_authentication import get_current_active_user
from ..dependencies import get_db


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/like", response_model=ReadLikes)
async def like_post(like: PostLike,
                 current_user = Depends(get_current_active_user), 
                 db: Session = Depends(get_db)):
    post = db.execut(select(Blogs).where(Blogs.id == like.blog_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = "Blog not found")
    user_like_post = create_like_post(db, like, current_user.user_name)
    return user_like_post
          

@router.get("/likes/blog/{blog_id}", response_model=ReadLikes)
def get_blog_with_likes(blog_id: int, db: Session = Depends(get_db)):
    likes = db.execute(select(Likes).where(Likes.blog_id == blog_id)).scalar_one_or_none()
    return likes
