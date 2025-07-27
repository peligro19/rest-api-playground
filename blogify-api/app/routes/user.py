from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas import UserCreate, UserRead
from app.crud import create_user, get_user

router = APIRouter()


@router.post("/", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(user, session)

@router.get("/{user_id}", response_model=UserRead)
def read(user_id: int, session: Session = Depends(get_session)):
    return get_user(user_id, session)
