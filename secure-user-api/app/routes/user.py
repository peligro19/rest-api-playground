from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..database import get_session
from ..models import User
from ..schemas import UserCreate, UserLogin, UserPublic
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserPublic)
def register(user: UserCreate, session: Session = Depends(get_session)):
    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    session.add(db_user)
    try:
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user

@router.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    query = select(User).where(User.email == user.email)
    db_user = session.exec(query).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
