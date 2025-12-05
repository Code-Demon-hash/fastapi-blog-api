from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Like, Blog
from ..crud import create_like
from ..schemas import LikePost, BlogStatus
from ..dependencies import get_db                                   


router = APIRouter(prefix="/like", tags=["likes"])


@router.post("/{blog_id}", status_code=status.HTTP_201_CREATED)
async def create_like_on_blog(blog_id: int, like: LikePost, db: Session = Depends(get_db)):
    post = db.execute(select(Blog).where(Blog.id == blog_id, Blog.status==BlogStatus.PUBLISHED)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Blog not found")
    new_like = create_like(db, like, blog_id)
    return new_like


@router.delete("/delete{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_like(id: int, db: Session = Depends(get_db)):
    like = db.execute(select(Like).where(Like.id == id)).scalar_one_or_none()
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detil="Like not found")
    db.delete(like)
    db.commit()
    return {"message": "Like removed successfully"}