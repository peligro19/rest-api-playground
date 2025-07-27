from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import tasks
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    create_db_and_tables()
    yield
    # Shutdown logic (if needed)

app = FastAPI(
    title="📝 Task Manager API",
    lifespan=lifespan
)

app.include_router(tasks.router) 
