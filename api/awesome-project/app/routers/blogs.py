from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from ..schemas import BlogCreate, BlogPost, BlogUpdate
from ..crud import create_blog
from ..dependencies import get_db
from ..models import Blogs

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", response_model=BlogPost, status_code=status.HTTP_201_CREATED)
def create_new_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    blog_create = create_blog(db=db, blog=blog)
    return blog_create

@router.put("/update/{id}", response_model=BlogCreate)
def update_blog_post(blog: BlogUpdate, id: int, db: Session = Depends(get_db)):
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
def delete_blog_post(id: int, db: Session = Depends(get_db)):
    blog_post = db.execute(select(Blogs).where(Blogs.id == id)).scalar_one_or_none()
    if not blog_post:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"blog_post with id not found")
    db.delete(blog_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)