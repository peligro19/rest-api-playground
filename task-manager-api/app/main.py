from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routes import tasks
from .models import SQLModel
from .database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown: (Optional cleanup code here)

app = FastAPI(title="📝 Task Manager API", lifespan=lifespan)

app.include_router(tasks.router)
