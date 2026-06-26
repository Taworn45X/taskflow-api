"""TaskFlow API — a small RESTful to-do service built with FastAPI."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="TaskFlow API",
    description="A small RESTful to-do API (FastAPI + SQLite).",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


@app.get("/", tags=["meta"])
def root():
    return {"name": "TaskFlow API", "docs": "/docs", "health": "/health"}
