from fastapi import FastAPI
from src.api.v1.auth import router as auth_router
from src.api.v1.protected import router as protected_router
from src.api.v1.tasks import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from src.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    from src.models.user import User  # Import here to ensure models are registered
    from src.models.task import Task  # Import here to ensure models are registered
    SQLModel.metadata.create_all(engine)
    yield
    # Cleanup on shutdown


app = FastAPI(title="Authentication API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(protected_router, prefix="/api/v1", tags=["protected"])
app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
def read_root():
    return {"Hello": "World"}