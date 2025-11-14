from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .security.author_authentication import get_current_author
from .security.admin_authentication import get_current_admin
from ..schemas import BlogCreate, BlogPost, BlogUpdate, UserReadBlog
from ..crud import create_a_blog, get_all
from ..dependencies import get_db
from ..models import Blogs, Authors, AdminUser, UserReadsBlogs


router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: BlogCreate,
                      author_id: int,
                      db: Session = Depends(get_db)):
    new_blog = create_a_blog(db, blog, author_id)
    return new_blog


@router.get("/", response_model=UserReadBlog)
async def read_blogs(db: Session = Depends(get_db)):
    return get_all(db)
    

@router.get("/", response_model=List[UserReadBlog])
async def read_blog(blog_id: int, db: Session = Depends(get_db)):
    post = db.get(UserReadsBlogs, blog_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Blog not found")
    return post


@router.put("/{blog_id}/submit", response_model=BlogPost)
async def submit_blog(blog_id: int,
                      db: Session = Depends(get_db)):
    blog_in_db = db.execute(select(Blogs).where(Blogs.id == blog_id)).scalar_one_or_none()
    if not blog_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Blog not found")
    blog_in_db.status = "PUBLISHED"
    db.commit()
    db.refresh(blog_in_db)
    return blog_in_db


@router.put("/update/{id}", response_model=BlogCreate)
async def update_blog_post(blog: BlogUpdate, id: int, db: Session = Depends(get_db)):
    post_in_db = db.execute(select(Blogs).where(Blogs.id == id)).scalar_one_or_none()
    if not post_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Blog with id does not exist'
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