from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Likes
from ..schemas import LikeCreate, ReadLikes
from ..dependencies import get_db


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/like")
def like_content(like: LikeCreate, db: Session = Depends(get_db)):
    liked_already = db.execute(select(Likes).where(Likes.user_id == like.user_id)),
    ((Likes.blog_id == like.blog_id) | (Likes.comment_id == like.comment_id
                               )).scalar_one_or_none()
    if liked_already:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail = "Already liked this content")
    create_new_like_content = Likes(like.model_dump()) 
    db.add(create_new_like_content)
    db.commit()
    db.refresh(create_new_like_content)
    return create_new_like_content                  

@router.get("/likes/blog/{blog_id}", response_model=ReadLikes)
def get_likes_for_blog(blog_id: int, db: Session = Depends(get_db)):
    likes = db.execute(select(Likes).where(Likes.blog_id == blog_id)).scalar_one_or_none()
    return likes

@router.get("/likes/comment/{comment_id}", response_model=ReadLikes)
def get_likes_for_comment(comment_id: int, db: Session = Depends(get_db)):
    likes = db.execute(select(Likes).where(Likes.comment_id == comment_id)).scalar_one_or_none()
    return likes