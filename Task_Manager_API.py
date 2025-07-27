# Complete Task Manager API Project using FastAPI + SQLModel + JWT + PostgreSQL

# ========================
# 1. project structure
# ========================
# task_manager_api/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py
# │   ├── config.py
# │   ├── database.py
# │   ├── models.py
# │   ├── schemas.py
# │   ├── crud.py
# │   ├── auth.py
# │   └── routes/
# │       ├── __init__.py
# │       ├── users.py
# │       └── tasks.py
# ├── .env
# ├── requirements.txt
# └── README.md

# ========================
# 2. requirements.txt
# ========================
# fastapi
# uvicorn
# sqlmodel
# psycopg2-binary
# python-dotenv
# passlib[bcrypt]
# python-jose

# ========================
# 3. .env file
# ========================
# DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskdb
# SECRET_KEY=your-secret-key
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# ========================
# 4. app/config.py
# ========================
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ========================
# 5. app/database.py
# ========================
from sqlmodel import create_engine, SQLModel, Session
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    import app.models
    SQLModel.metadata.create_all(engine)

# ========================
# 6. app/models.py
# ========================
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(foreign_key="user.id")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str
    password: str

# ========================
# 7. app/schemas.py
# ========================
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskRead(TaskCreate):
    id: int
    completed: bool
    timestamp: datetime
    class Config:
        orm_mode = True

# ========================
# 8. app/auth.py
# ========================
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from . import schemas, models, config, database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.exec(select(models.User).where(models.User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

# ========================
# 9. app/crud.py
# ========================
from sqlmodel import Session, select
from .models import User, Task
from .auth import get_password_hash


def get_user_by_username(db: Session, username: str):
    return db.exec(select(User).where(User.username == username)).first()

def create_user(db: Session, user_data):
    hashed_pw = get_password_hash(user_data.password)
    user = User(username=user_data.username, email=user_data.email, password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_task(db: Session, task_data, user_id: int):
    task = Task(**task_data.dict(), owner_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, user_id: int):
    return db.exec(select(Task).where(Task.owner_id == user_id)).all()

def get_task(db: Session, task_id: int, user_id: int):
    return db.exec(select(Task).where(Task.id == task_id, Task.owner_id == user_id)).first()

def update_task(db: Session, task: Task, data):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()

# ========================
# 10. app/routes/users.py
# ========================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, crud, auth

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_session)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_session)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ========================
# 11. app/routes/tasks.py
# ========================
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .. import schemas, database, crud, auth

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_session), current_user=Depends(auth.get_current_user)):
    return crud.create_task(db, task, current_user.id)

@router.get("/", response_model=list[schemas.TaskRead])
def read_tasks(db: Session = Depends(database.get_session), current_user=Depends(auth.get_current_user)):
    return crud.get_tasks(db, current_user.id)

@router.get("/{task_id}", response_model=schemas.TaskRead)
def read_task(task_id: int, db: Session = Depends(database.get_session), current_user=Depends(auth.get_current_user)):
    task = crud.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, task_data: schemas.TaskCreate, db: Session = Depends(database.get_session), current_user=Depends(auth.get_current_user)):
    task = crud.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, task, task_data)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_session), current_user=Depends(auth.get_current_user)):
    task = crud.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return {"detail": "Task deleted"}

# ========================
# 12. app/main.py
# ========================
from fastapi import FastAPI
from .database import init_db
from .routes import users, tasks

app = FastAPI(title="Task Manager API")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users.router)
app.include_router(tasks.router)

# ========================
# To run the project:
# ========================
# uvicorn app.main:app --reload
# Open browser at http://127.0.0.1:8000/docs
