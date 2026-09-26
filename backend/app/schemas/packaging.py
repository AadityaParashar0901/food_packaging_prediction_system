from typing import Literal

from pydantic import BaseModel, Field


class PackagingInput(BaseModel):
    commodity: str = Field(
        min_length=1,
        max_length=120,
    )

    moisture: float = Field(
        ge=0,
        le=100,
    )

    fat: float = Field(
        ge=0,
        le=100,
    )

    ash: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    sodium: float | None = Field(
        default=None,
        ge=0,
    )

    pH: float = Field(
        ge=0,
        le=14,
    )

    water_activity: float = Field(
        ge=0,
        le=1,
    )

    respiration_rate: float = Field(
        ge=0,
    )

    ethylene_rate: float = Field(
        ge=0,
    )

    temperature: float = Field(
        ge=-30,
        le=60,
    )

    relative_humidity: float = Field(
        ge=0,
        le=100,
    )

    desired_shelf_life: float = Field(
        gt=0,
    )

    storage_type: Literal[
        "ambient",
        "chilled",
        "frozen",
    ]

    transportation_condition: Literal[
        "normal",
        "refrigerated",
        "frozen",
    ]
