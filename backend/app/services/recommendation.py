from pathlib import Path

import joblib
import pandas as pd


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "food" / "models"
DATASET_PATH = BASE_DIR / "food" / "data" / "packaging_training_data.csv"


# =========================================================
# MODEL FILES
# =========================================================

MODEL_PATHS = {
    "recommended_material": (
        MODEL_DIR / "recommended_material_model.joblib"
    ),

    "film_thickness": (
        MODEL_DIR / "film_thickness_model.joblib"
    ),

    "OTR_requirement": (
        MODEL_DIR / "OTR_requirement_model.joblib"
    ),

    "WVTR_requirement": (
        MODEL_DIR / "WVTR_requirement_model.joblib"
    ),

    "sealability": (
        MODEL_DIR / "sealability_model.joblib"
    ),

    "MAP_suitability": (
        MODEL_DIR / "MAP_suitability_model.joblib"
    ),

    "mechanical_strength": (
        MODEL_DIR / "mechanical_strength_model.joblib"
    ),
}


# =========================================================
# RUNTIME STATE
# =========================================================

MODELS: dict[str, object] = {}

COMMODITIES: list[str] = []


# =========================================================
# MODEL FEATURES
# =========================================================
#
# These MUST match the features used by 14_train_model.py.
# =========================================================

NUMERIC_FEATURES = [
    "moisture",
    "fat",
    "ash",
    "sodium",
    "pH",
    "water_activity",
    "respiration_rate",
    "ethylene_rate",
    "temperature",
    "relative_humidity",
    "desired_shelf_life",
]

CATEGORICAL_FEATURES = [
    "commodity",
    "storage_type",
    "transportation_condition",
]

FEATURES = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
)


# =========================================================
# COMMODITY DATASET
# =========================================================

def load_commodities() -> bool:
    """
    Load the canonical commodity list from the packaging
    training dataset.
    """

    global COMMODITIES

    if not DATASET_PATH.exists():
        COMMODITIES = []
        return False

    df = pd.read_csv(
        DATASET_PATH,
        encoding="latin1",
        low_memory=False,
    )

    if "commodity" not in df.columns:
        raise ValueError(
            "Dataset must contain a 'commodity' column. "
            f"Found: {list(df.columns)}"
        )

    COMMODITIES = (
        df["commodity"]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda s: s != ""]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return True


def get_commodities() -> list[str]:
    """
    Return all valid commodities known by the training dataset.
    """

    return COMMODITIES.copy()


def validate_commodity(commodity: str) -> str:
    """
    Validate that the supplied commodity exists in the dataset.
    """

    if not isinstance(commodity, str):
        raise ValueError(
            "Commodity must be a string."
        )

    commodity = commodity.strip().lower()

    if not commodity:
        raise ValueError(
            "Commodity is required."
        )

    if not COMMODITIES:
        raise RuntimeError(
            "Commodity dataset is not loaded."
        )

    if commodity not in COMMODITIES:
        raise ValueError(
            f"Unknown commodity '{commodity}'. "
            f"Choose a commodity from "
            f"/api/packaging/commodities."
        )

    return commodity


# =========================================================
# MODEL LOADING
# =========================================================

def load_model() -> bool:
    """
    Load all seven trained ML models.
    """

    global MODELS

    MODELS = {}

    missing_models = []

    for name, path in MODEL_PATHS.items():

        if not path.exists():
            missing_models.append(
                str(path)
            )
            continue

        MODELS[name] = joblib.load(path)

    if missing_models:

        MODELS = {}

        return False

    return True


def get_model(name: str):
    """
    Return a loaded model by name.
    """

    if name not in MODELS:

        raise RuntimeError(
            f"ML model '{name}' is not loaded."
        )

    return MODELS[name]


def model_status() -> dict:
    """
    Return ML model status for health/debug endpoints.
    """

    loaded_models = {
        name: name in MODELS
        for name in MODEL_PATHS
    }

    return {
        "loaded": len(MODELS) == len(MODEL_PATHS),
        "type": "Random Forest",
        "model_count": len(MODELS),
        "expected_model_count": len(MODEL_PATHS),
        "models": loaded_models,
        "directory": str(MODEL_DIR),
    }


def dataset_status() -> dict:
    """
    Return commodity dataset status.
    """

    return {
        "loaded": bool(COMMODITIES),
        "commodity_count": len(COMMODITIES),
        "path": str(DATASET_PATH),
    }


# =========================================================
# FEATURE PREPARATION
# =========================================================

def _features(data: dict) -> pd.DataFrame:
    """
    Convert request data into the exact feature schema used
    during model training.
    """

    row = {
        # USDA features
        "moisture": float(data["moisture"]),
        "fat": float(data["fat"]),
        "ash": (
            float(data["ash"])
            if data.get("ash") is not None
            else None
        ),

        "sodium": (
            float(data["sodium"])
            if data.get("sodium") is not None
            else None
        ),

        # Food physiology
        "pH": float(data["pH"]),
        "water_activity": float(
            data["water_activity"]
        ),
        "respiration_rate": float(
            data["respiration_rate"]
        ),
        "ethylene_rate": float(
            data["ethylene_rate"]
        ),

        # Storage conditions
        "temperature": float(
            data["temperature"]
        ),
        "relative_humidity": float(
            data["relative_humidity"]
        ),
        "desired_shelf_life": float(
            data["desired_shelf_life"]
        ),

        # Categorical features
        "commodity": data["commodity"],
        "storage_type": data["storage_type"],
        "transportation_condition": (
            data["transportation_condition"]
        ),
    }

    return pd.DataFrame(
        [row],
        columns=FEATURES,
    )


# =========================================================
# NUMERIC CLEANUP
# =========================================================

def _number(value) -> float:
    """
    Convert a model output into a normal Python float.
    """

    return float(value)


# =========================================================
# MODEL PREDICTION
# =========================================================

def predict_requirements(data: dict) -> dict:
    """
    Run all seven trained Random Forest models.
    """

    features = _features(data)

    # -----------------------------------------------------
    # Classification
    # -----------------------------------------------------

    material_model = get_model(
        "recommended_material"
    )

    sealability_model = get_model(
        "sealability"
    )

    map_model = get_model(
        "MAP_suitability"
    )

    mechanical_model = get_model(
        "mechanical_strength"
    )

    recommended_material = material_model.predict(
        features
    )[0]

    sealability = sealability_model.predict(
        features
    )[0]

    map_suitability = map_model.predict(
        features
    )[0]

    mechanical_strength = mechanical_model.predict(
        features
    )[0]

    # -----------------------------------------------------
    # Regression
    # -----------------------------------------------------

    thickness_model = get_model(
        "film_thickness"
    )

    otr_model = get_model(
        "OTR_requirement"
    )

    wvtr_model = get_model(
        "WVTR_requirement"
    )

    film_thickness = thickness_model.predict(
        features
    )[0]

    otr = otr_model.predict(
        features
    )[0]

    wvtr = wvtr_model.predict(
        features
    )[0]

    return {
        "recommended_material": str(
            recommended_material
        ),

        "film_thickness": _number(
            film_thickness
        ),

        "OTR_requirement": _number(
            otr
        ),

        "WVTR_requirement": _number(
            wvtr
        ),

        "sealability": str(
            sealability
        ),

        "MAP_suitability": str(
            map_suitability
        ),

        "mechanical_strength": str(
            mechanical_strength
        ),
    }


# =========================================================
# FINAL RECOMMENDATION
# =========================================================

def get_recommendation(data: dict) -> dict:
    """
    Validate the commodity, run all ML models, and return
    the packaging recommendation.
    """

    data = dict(data)

    data["commodity"] = validate_commodity(
        data.get("commodity", "")
    )

    prediction = predict_requirements(
        data
    )

    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------

    map_value = prediction[
        "MAP_suitability"
    ]

    map_suitable = (
        str(map_value).lower()
        in {
            "high",
            "medium",
            "yes",
            "suitable",
        }
    )

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return {
        "prototype": True,

        "model": "Random Forest",

        "recommendation": {

            "material": prediction[
                "recommended_material"
            ],

            "material_code": (
                prediction[
                    "recommended_material"
                ]
                .upper()
                .replace(" ", "-")
                .replace("/", "-")
            ),

            "thickness": {
                "value": round(
                    prediction[
                        "film_thickness"
                    ],
                    2,
                ),
                "unit": "µm",
                "status": "model estimate",
            },

            "otr": {
                "requirement_score": round(
                    prediction[
                        "OTR_requirement"
                    ],
                    2,
                ),
                "unit": "normalized requirement score",
            },

            "wvtr": {
                "requirement_score": round(
                    prediction[
                        "WVTR_requirement"
                    ],
                    2,
                ),
                "unit": "normalized requirement score",
            },

            "sealability": prediction[
                "sealability"
            ],

            "map": {
                "suitable": map_suitable,
                "classification": prediction[
                    "MAP_suitability"
                ],
            },

            "mechanical_strength": {
                "classification": prediction[
                    "mechanical_strength"
                ],
            },
        },

        "reason": (
            "The recommendation was generated by the "
            "trained Random Forest packaging models using "
            "food properties, physiological properties, "
            "storage conditions, transportation conditions, "
            "and desired shelf life."
        ),

        "warning": (
            "Prototype estimate. The current training "
            "labels are synthetic and packaging performance "
            "must be validated with laboratory testing "
            "before production use."
        ),
    }
