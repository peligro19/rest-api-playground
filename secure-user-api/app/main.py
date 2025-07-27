from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import user
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Logic
    # Database & Tables Create
    create_db_and_tables()
    yield
    # Shutdown Logic

app = FastAPI(
    title="🔐 Secure User Registry API",
    lifespan=lifespan
)

# Register routers
app.include_router(user.router, prefix="/user", tags=["Users"])