from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas import BlogCreate, BlogRead
from app.crud import create_blog, get_blogs

router = APIRouter()


@router.post("/", response_model=BlogRead)
def create(blog: BlogCreate, session: Session = Depends(get_session)):
    return create_blog(blog, session)

@router.get("/", response_model=list[BlogRead])
def read_all(session: Session = Depends(get_session)):
    return get_blogs(session)
