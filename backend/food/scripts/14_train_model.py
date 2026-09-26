from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


# =========================================================
# FILES
# =========================================================

INPUT_FILE = Path("data/packaging_training_data.csv")
MODEL_DIR = Path("models")

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# LOAD DATA
# =========================================================

print("Loading packaging training data...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")


# =========================================================
# INPUT FEATURES
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
# TARGETS
# =========================================================

CLASSIFICATION_TARGETS = [
    "recommended_material",
    "sealability",
    "MAP_suitability",
    "mechanical_strength",
]

REGRESSION_TARGETS = [
    "film_thickness",
    "OTR_requirement",
    "WVTR_requirement",
]


# =========================================================
# CHECK COLUMNS
# =========================================================

required_columns = (
    FEATURES
    + CLASSIFICATION_TARGETS
    + REGRESSION_TARGETS
    + ["sample_group"]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        "Missing columns:\n"
        + "\n".join(
            f"  - {column}"
            for column in missing_columns
        )
    )


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================
#
# IMPORTANT:
# We split by sample_group rather than individual rows.
#
# This prevents different storage/transport scenarios
# generated from the SAME USDA sample from appearing in
# both training and testing sets.
# =========================================================

print()
print("=" * 80)
print("CREATING GROUPED TRAIN / TEST SPLIT")
print("=" * 80)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42,
)

train_indices, test_indices = next(
    splitter.split(
        df,
        groups=df["sample_group"],
    )
)

train_df = df.iloc[train_indices].copy()
test_df = df.iloc[test_indices].copy()

print(f"Training rows: {len(train_df):,}")
print(f"Testing rows:  {len(test_df):,}")

print(
    f"Training samples: "
    f"{train_df['sample_group'].nunique():,}"
)

print(
    f"Testing samples:  "
    f"{test_df['sample_group'].nunique():,}"
)


# =========================================================
# PREPROCESSING
# =========================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="median",
            ),
        ),
    ]
)


categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent",
            ),
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
            ),
        ),
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            NUMERIC_FEATURES,
        ),
        (
            "categorical",
            categorical_pipeline,
            CATEGORICAL_FEATURES,
        ),
    ]
)


# =========================================================
# MODEL CONFIGURATION
# =========================================================

def create_classifier():
    return Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=200,
                    random_state=42,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )


def create_regressor():
    return Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=200,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


# =========================================================
# TRAIN CLASSIFICATION MODELS
# =========================================================

classification_results = {}


for target in CLASSIFICATION_TARGETS:

    print()
    print("=" * 80)
    print(f"TRAINING CLASSIFIER: {target}")
    print("=" * 80)

    X_train = train_df[FEATURES]
    X_test = test_df[FEATURES]

    y_train = train_df[target]
    y_test = test_df[target]

    model = create_classifier()

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    classification_results[target] = {
        "accuracy": float(accuracy),
    }

    print(
        f"Accuracy: "
        f"{accuracy:.4f}"
    )

    output_file = (
        MODEL_DIR
        / f"{target}_model.joblib"
    )

    joblib.dump(
        model,
        output_file,
    )

    print(
        f"Saved: {output_file}"
    )


# =========================================================
# TRAIN REGRESSION MODELS
# =========================================================

regression_results = {}


for target in REGRESSION_TARGETS:

    print()
    print("=" * 80)
    print(f"TRAINING REGRESSOR: {target}")
    print("=" * 80)

    X_train = train_df[FEATURES]
    X_test = test_df[FEATURES]

    y_train = train_df[target]
    y_test = test_df[target]

    model = create_regressor()

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    regression_results[target] = {
        "mae": float(mae),
    }

    print(
        f"Mean Absolute Error: "
        f"{mae:.4f}"
    )

    output_file = (
        MODEL_DIR
        / f"{target}_model.joblib"
    )

    joblib.dump(
        model,
        output_file,
    )

    print(
        f"Saved: {output_file}"
    )


# =========================================================
# SAVE MODEL METADATA
# =========================================================

metadata = {
    "features": FEATURES,
    "numeric_features": NUMERIC_FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "classification_targets": CLASSIFICATION_TARGETS,
    "regression_targets": REGRESSION_TARGETS,
    "classification_results": classification_results,
    "regression_results": regression_results,
    "train_rows": len(train_df),
    "test_rows": len(test_df),
    "random_state": 42,
}


metadata_file = (
    MODEL_DIR / "model_metadata.json"
)

with open(
    metadata_file,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        metadata,
        f,
        indent=2,
    )


# =========================================================
# FINAL SUMMARY
# =========================================================

print()
print("=" * 80)
print("MODEL TRAINING COMPLETE")
print("=" * 80)

print()
print("Classification models:")

for target, result in classification_results.items():

    print(
        f"  {target:25s} "
        f"accuracy = "
        f"{result['accuracy']:.4f}"
    )


print()
print("Regression models:")

for target, result in regression_results.items():

    print(
        f"  {target:25s} "
        f"MAE = "
        f"{result['mae']:.4f}"
    )


print()
print(f"Models saved in: {MODEL_DIR}")
print(f"Metadata saved to: {metadata_file}")
print()
print("Done.")
