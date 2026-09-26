import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.health import router as health_router
from app.routes.packaging import router as packaging_router
from app.services.database import connect_db, close_db
from app.services.recommendation import (
    load_model,
    load_commodities,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database
    connect_db()

    # ML model
    load_model()

    # Dataset-backed commodity list
    load_commodities()

    yield

    # Shutdown
    close_db()


app = FastAPI(
    title="Food Packaging Recommendation API",
    version="1.0.0",
    description=(
        "Prototype AI backend for intelligent "
        "food packaging recommendations."
    ),
    lifespan=lifespan,
)


origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5173,http://localhost:5174",
    ).split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_router,
    prefix="/api",
)

app.include_router(
    packaging_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "name": "Food Packaging Recommendation API",
        "status": "running",
        "docs": "/docs",
    }
