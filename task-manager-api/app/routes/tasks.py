from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate
from .. import crud

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=Task)
def create(task: TaskCreate, session: Session = Depends(get_session)):
    task_obj = Task(**task.model_dump())
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
