
# 📝 Task Manager API

A simple task management REST API built with **FastAPI**, **SQLModel**, and **PostgreSQL**/**MySQL**.


![alt text](image.png)

---

## 📁 Project Structure

```
task_manager_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── crud.py
│   └── routes/
│       ├── __init__.py
│       └── tasks.py
├── alembic/
│   └── ...
├── requirements.txt
├── .env
└── README.md
```


## ✅ Features Covered

- RESTful API with FastAPI
- Pydantic models for validation
- PostgreSQL as the database
- SQLModel/SQLAlchemy as ORM
- CRUD operations: Create, Read, Update, Delete
- Environment config via `.env`
- Step-by-step feature additions

---

## 🔨 Step-by-Step Guide

### 1. Environment Setup

```bash
python -m venv venv

source venv/bin/activate  # On Linux

venv\Scripts\activate # On Windows
# or
venv\Scripts\activate.bat # On Windows

pip install fastapi[all] psycopg2-binary sqlmodel
```

### 2. `requirements.txt`

```
fastapi
uvicorn
sqlmodel
psycopg2-binary
python-dotenv
```

### 3. `.env`

```
DATABASE_URL=postgresql://username:password@localhost/task_db
```

### 4. `app/database.py`

```python
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

### 5. `app/models.py`

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = False
```

### 6. `app/schemas.py`

```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool
```

### 7. `app/crud.py`

```python
from sqlmodel import Session, select
from .models import Task

def create_task(session: Session, task: Task):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks(session: Session):
    return session.exec(select(Task)).all()

def get_task(session: Session, task_id: int):
    return session.get(Task, task_id)

def update_task(session: Session, task_data: Task):
    session.add(task_data)
    session.commit()
    session.refresh(task_data)
    return task_data

def delete_task(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
    return task
```

### 8. `app/routes/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate
from .. import crud

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=Task)
def create(task: TaskCreate, session: Session = Depends(get_session)):
    task_obj = Task(**task.dict())
    return crud.create_task(session, task_obj)

@router.get("/", response_model=list[Task])
def read_all(session: Session = Depends(get_session)):
    return crud.get_tasks(session)

@router.get("/{task_id}", response_model=Task)
def read(task_id: int, session: Session = Depends(get_session)):
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    db_task = crud.get_task(session, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.dict().items():
        setattr(db_task, key, value)
    return crud.update_task(session, db_task)

@router.delete("/{task_id}")
def delete(task_id: int, session: Session = Depends(get_session)):
    task = crud.delete_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
```

### 9. `app/main.py`

```python
from fastapi import FastAPI
from .routes import tasks
from .models import SQLModel
from .database import engine

app = FastAPI(title="📝 Task Manager API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(tasks.router)
```

### 🚀 Run the App

```bash
uvicorn app.main:app --reload
```

---

## ✅ Next Add-on Ideas

- JWT-based authentication
- User model & task ownership
- Filtering, searching, pagination
- Testing with Pytest
- Dockerize the API
