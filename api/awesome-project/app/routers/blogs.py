from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .security.author_authentication import get_current_author
from ..schemas import BlogCreate, BlogPost, BlogUpdate
from ..crud import create_a_blog
from ..dependencies import get_db
from ..models import Blogs, Authors


router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", response_model=BlogPost)
async def create_blog(blog: BlogCreate, 
                      current_author: Authors = Depends(get_current_author), 
                      db: Session = Depends(get_db)
):
    new_blog = create_a_blog(db, blog, author_id=current_author.author_id)
    return new_blog


@router.post("/{blog_id}/submit", response_model=BlogPost)
async def submit_blog(blog_id: int,
                      current_author: Authors = Depends(get_current_author),
                      db: Session = Depends(get_db)
):
    blog_in_db = db.execute(select(Blogs).where(Blogs.id == blog_id)).scalar_one_or_none()
    if not blog_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Blog not found")
    blog_in_db.status = "PENDING"
    db.commit()
    db.refresh(blog_in_db)
    return blog_in_db

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