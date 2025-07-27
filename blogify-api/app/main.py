from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import blog, user
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    create_db_and_tables()
    yield
    # Shutdown logic (if needed)

app = FastAPI(
    title="📝 Blogify API",
    lifespan=lifespan
)

# Register routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(blog.router, prefix="/blogs", tags=["Blogs"])
