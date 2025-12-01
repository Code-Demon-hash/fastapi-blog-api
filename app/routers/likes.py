from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Likes, Blogs
from ..crud import create_like_post
from ..schemas import LikePost, BlogStatus
from ..dependencies import get_db


router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/{blog_id}", status_code=status.HTTP_201_CREATED)
async def like_post(blog_id: int,
                    like: LikePost, 
                    db: Session = Depends(get_db), 
                    direction: int = Query(..., le=1)
):
    post = db.execute(select(Blogs).where(Blogs.id == blog_id, Blogs.status==BlogStatus.PUBLISHED)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = "Blog not found")
    like_query = db.execute(select(Likes).where(Likes.id == blog_id, Likes.user_id==like.user_id))
    found_like = like_query.scalar_one_or_none()
    if direction == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User has already liked post")
        new_like = create_like_post(db, like, blog_id)
        db.add(new_like)
        db.commit()
        return {"message": "Successfully added like"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote does not exist")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted like"}