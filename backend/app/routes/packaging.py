from fastapi import APIRouter, HTTPException

from app.schemas.packaging import PackagingInput
from app.services.recommendation import (
    get_commodities,
    get_recommendation,
    model_status,
    predict_requirements,
)


router = APIRouter(
    prefix="/packaging",
    tags=["packaging"],
)


@router.get("/commodities")
def commodities():
    """
    Return the canonical commodity list used by the model dataset.
    """

    values = get_commodities()

    if not values:
        raise HTTPException(
            status_code=503,
            detail="Commodity dataset is not loaded.",
        )

    return {
        "success": True,
        "commodities": values,
        "count": len(values),
    }


@router.get("/model-status")
def get_model_status():
    return model_status()


@router.post("/predict")
def predict(data: PackagingInput):
    """
    Return raw ML packaging requirement predictions.
    """

    try:
        payload = data.model_dump()

        return {
            "success": True,
            "input": payload,
            "prediction": predict_requirements(payload),
        }

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/recommend")
def recommend(data: PackagingInput):
    """
    Return the final packaging recommendation.
    """

    try:
        payload = data.model_dump()

        recommendation = get_recommendation(payload)

        return {
            "success": True,
            "input": payload,
            **recommendation,
        }

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
