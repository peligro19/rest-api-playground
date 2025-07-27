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
