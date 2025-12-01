from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Blogs, Comments
from .security.user_authentication import get_current_user
from ..schemas import CommentCreate, CommentRead, BlogStatus
from ..crud import create_comment, get_comment_by_blog_id
from ..dependencies import get_db



router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/{blog_id}", status_code=status.HTTP_201_CREATED)
async def create_comment_for_blog(blog_id: int,
                                  comment: CommentCreate,
                                  db: Session = Depends(get_db)
):
    new_comment = create_comment(db, blog_id, comment)
    return new_comment


@router.get("/{blog_id}", response_model=CommentRead)
async def read_comments_on_blog(blog_id: int, db: Session = Depends(get_db)):
    post = db.execute(select(Blogs).where(Blogs.id == blog_id, Blogs.status==BlogStatus.PUBLISHED)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Blog not found")
    comments = get_comment_by_blog_id(db, blog_id) 
    return comments
