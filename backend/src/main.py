from fastapi import FastAPI
from src.api.v1.auth import router as auth_router
from src.api.v1.protected import router as protected_router
from src.api.v1.tasks import router as tasks_router
from src.api.v1.chat.router import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_db_and_tables()
    yield
    # Cleanup on shutdown


app = FastAPI(title="Authentication API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=(os.getenv("ALLOWED_ORIGINS") or "http://localhost:3000,*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(protected_router, prefix="/api/v1", tags=["protected"])
app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])
app.include_router(chat_router, tags=["chat"])

@app.get("/")
def read_root():
    return {"Hello": "World"}