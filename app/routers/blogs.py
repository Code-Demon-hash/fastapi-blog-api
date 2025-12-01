from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .security.author_authentication import get_current_author
from .security.admin_authentication import get_current_admin
from ..schemas import BlogCreate, BlogPost, BlogUpdate, UserReadBlog, BlogInfoSchema
from ..enums import BlogStatus
from ..crud import create_a_blog, is_admin
from ..dependencies import get_db
from ..models import Blogs, Authors, AdminUser, UserReadsBlogs


router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/create", response_model=BlogPost)
async def create_blog(blog: BlogCreate,
                      author_id: int,
                      db: Session = Depends(get_db)):
    new_blog = create_a_blog(db, blog, author_id)
    return new_blog


@router.put("/{blog_id}/submit", status_code=status.HTTP_202_ACCEPTED)
async def submit_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_in_db = db.execute(select(Blogs).where(Blogs.id == blog_id)).scalar_one_or_none()
    if not blog_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Blog not found")
    is_admin(db, blog_in_db)
    blog_in_db.status = BlogStatus.PUBLISHED
    db.commit()
    db.refresh(blog_in_db)
    return blog_in_db
    

@router.get("/", response_model=List[UserReadBlog])
async def read_blogs(limit: int = 10, 
                    skip: int = 0,
                    search: Optional[str] = "",
                    db: Session = Depends(get_db)
):
    results = db.query(Blogs).filter(Blogs.title.contains(search), 
                                     Blogs.status==BlogStatus.PUBLISHED).limit(limit).offset(skip).all()
    return results


@router.get("/{id}", response_model=BlogInfoSchema)
async def read_blog(id: int, db: Session = Depends(get_db)):
    post = db.execute(select(Blogs).filter(Blogs.status==BlogStatus.PUBLISHED).where(Blogs.id==id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Blog not found")
    return post


@router.put("/update/{id}", response_model=BlogCreate)
async def update_blog_post(blog: BlogUpdate, id: int, db: Session = Depends(get_db)):
    post_in_db = db.execute(select(Blogs).where(Blogs.id == id)).scalar_one_or_none()
    if not post_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Blog does not exist"
        )
    update_data = blog.model_dump(exclude_unset=True)
    if not update_data: 
        pass
    else:
        stmt = update(Blogs).where(Blogs.id == id).values(update_data)
        db.execute(stmt)
        db.commit()
    updated_post = db.execute(select(Blogs).where(Blogs.id == id)).scalar_one_or_none()
    return updated_post


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_post(id: int, db: Session = Depends(get_db)):
    blog_post = db.execute(select(Blogs).where(Blogs.id == id)).scalar_one_or_none()
    if not blog_post:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"blog_post with id not found")
    db.delete(blog_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)