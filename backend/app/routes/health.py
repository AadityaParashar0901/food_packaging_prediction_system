from fastapi import APIRouter

from app.services.database import database_status
from app.services.recommendation import (
    model_status,
    dataset_status,
)


router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    model = model_status()
    dataset = dataset_status()
    database = database_status()

    healthy = (
        model["loaded"]
        and dataset["loaded"]
        and database.get("connected", True)
    )

    return {
        "success": True,
        "status": "healthy" if healthy else "degraded",
        "database": database,
        "model": model,
        "dataset": dataset,
    }
