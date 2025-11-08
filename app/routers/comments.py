from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Blogs
from ..schemas import CommentCreate, CommentRead, ReadLikes
from ..crud import create_comment
from ..dependencies import get_db
from .security.user_authentication import get_current_active_user



router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/comments/", status_code=status.HTTP_201_CREATED)
async def create_comment_route(comment: CommentCreate,
                         db: Session = Depends(get_db),
                         current_user = Depends(get_current_active_user)):
    post = db.execute(select(Blogs).where(Blogs.id == comment.blog_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Blog does not exist")
    comment_service = create_comment(db, comment, current_user.username)
    return comment_service


@router.get("/blog/{blog_id}/comment", response_model=CommentRead)
async def read_comments_on_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.execute(select(Blogs).where(Blogs.id == blog_id)).scalar_one_or_none()
    if not blog:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Blog not found")
    return blog
