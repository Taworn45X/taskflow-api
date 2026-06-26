"""Database setup — a thin SQLModel/SQLite layer."""
import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")

# check_same_thread=False lets the SQLite connection be shared across requests.
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Create tables on startup."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency that yields a DB session per request."""
    with Session(engine) as session:
        yield session
