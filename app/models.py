"""Task models — one table model plus request/response schemas."""
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(SQLModel, table=True):
    """A single to-do item stored in the database."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Priority = Field(default=Priority.medium)
    done: bool = Field(default=False)
    created_at: datetime = Field(default_factory=_now)


class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Priority = Priority.medium


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[Priority] = None
    done: Optional[bool] = None


class TaskRead(SQLModel):
    id: int
    title: str
    description: Optional[str]
    priority: Priority
    done: bool
    created_at: datetime
