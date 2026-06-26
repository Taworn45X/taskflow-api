"""CRUD endpoints for tasks."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Priority, Task, TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def _get_or_404(task_id: int, session: Session) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Task {task_id} not found")
    return task


@router.get("", response_model=List[TaskRead])
def list_tasks(
    session: Session = Depends(get_session),
    done: Optional[bool] = Query(default=None, description="Filter by completion state"),
    priority: Optional[Priority] = Query(default=None),
):
    """List tasks, optionally filtered by done state and/or priority."""
    statement = select(Task)
    if done is not None:
        statement = statement.where(Task.done == done)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    return session.exec(statement.order_by(Task.created_at.desc())).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    return _get_or_404(task_id, session)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, session: Session = Depends(get_session)):
    task = Task.model_validate(payload)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)):
    task = _get_or_404(task_id, session)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = _get_or_404(task_id, session)
    session.delete(task)
    session.commit()
