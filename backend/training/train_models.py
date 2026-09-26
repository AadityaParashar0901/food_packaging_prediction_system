from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

OTR_FILE = DATA_DIR / "packaging_otr_candidates.csv"
WVTR_FILE = DATA_DIR / "packaging_wvtr_candidates.csv"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Features
# ============================================================

CATEGORICAL_FEATURES = [
    "Base Material",
    "Type",
    "Secondary Material",
    "Composition",
    "Plasticizer",
]

NUMERIC_FEATURES = [
    "thickness_Updated_Num",
    "temperature_Updated_Num",
    "RH_Updated_Num",
]

FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


# ============================================================
# Model configuration
# ============================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20

MODEL_PARAMS = {
    "n_estimators": 300,
    "max_depth": 12,
    "min_samples_leaf": 2,
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
}


# ============================================================
# Metrics
# ============================================================

def regression_metrics(y_true_log, y_pred_log):
    """
    Calculate metrics in log10 space and original target space.
    """

    # Log-space
    log_mae = mean_absolute_error(
        y_true_log,
        y_pred_log
    )

    log_rmse = np.sqrt(
        mean_squared_error(
            y_true_log,
            y_pred_log
        )
    )

    log_r2 = r2_score(
        y_true_log,
        y_pred_log
    )

    # Convert back to original units
    y_true = np.power(10, y_true_log)
    y_pred = np.power(10, y_pred_log)

    real_mae = mean_absolute_error(
        y_true,
        y_pred
    )

    real_rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    real_r2 = r2_score(
        y_true,
        y_pred
    )

    return {
        "log_mae": log_mae,
        "log_rmse": log_rmse,
        "log_r2": log_r2,
        "real_mae": real_mae,
        "real_rmse": real_rmse,
        "real_r2": real_r2,
    }


# ============================================================
# Train one model
# ============================================================

def train_model(
    data_file,
    target_column,
    log_target_column,
    model_name,
):
    print()
    print("=" * 70)
    print(f"TRAINING {model_name}")
    print("=" * 70)

    if not data_file.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{data_file}"
        )

    df = pd.read_csv(data_file)

    # --------------------------------------------------------
    # Validate columns
    # --------------------------------------------------------

    required = FEATURES + [
        "Doc",
        target_column,
        log_target_column,
    ]

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns:\n"
            + "\n".join(
                f"  - {column}"
                for column in missing
            )
        )

    # --------------------------------------------------------
    # Remove rows with invalid target
    # --------------------------------------------------------

    df = df[
        df[target_column].notna()
        & df[log_target_column].notna()
        & (df[target_column] > 0)
    ].copy()

    print(f"Rows available: {len(df)}")
    print(
        f"Unique source documents: "
        f"{df['Doc'].nunique()}"
    )

    # --------------------------------------------------------
    # X / y / groups
    # --------------------------------------------------------

    X = df[FEATURES].copy()

    y = df[log_target_column].astype(float)

    groups = df["Doc"].astype(str)

    # --------------------------------------------------------
    # Grouped train/test split
    # --------------------------------------------------------

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    train_idx, test_idx = next(
        splitter.split(
            X,
            y,
            groups=groups,
        )
    )

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    train_groups = groups.iloc[train_idx]
    test_groups = groups.iloc[test_idx]

    print()
    print("Train/test split:")
    print(f"  Training rows: {len(X_train)}")
    print(f"  Test rows    : {len(X_test)}")
    print(
        f"  Training docs: "
        f"{train_groups.nunique()}"
    )
    print(
        f"  Test docs    : "
        f"{test_groups.nunique()}"
    )

    overlap = (
        set(train_groups.unique())
        & set(test_groups.unique())
    )

    if overlap:
        raise RuntimeError(
            "Source-document leakage detected!"
        )

    # --------------------------------------------------------
    # Preprocessing
    # --------------------------------------------------------

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
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

    # --------------------------------------------------------
    # Random Forest
    # --------------------------------------------------------

    model = RandomForestRegressor(
        **MODEL_PARAMS
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    print()
    print("Training model...")

    pipeline.fit(
        X_train,
        y_train,
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    y_pred = pipeline.predict(
        X_test
    )

    metrics = regression_metrics(
        y_test.to_numpy(),
        y_pred,
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("LOG10 TARGET METRICS")
    print("-" * 70)

    print(
        f"MAE : {metrics['log_mae']:.4f}"
    )

    print(
        f"RMSE: {metrics['log_rmse']:.4f}"
    )

    print(
        f"R²  : {metrics['log_r2']:.4f}"
    )

    print()
    print("-" * 70)
    print("ORIGINAL TARGET UNITS")
    print("-" * 70)

    print(
        f"MAE : {metrics['real_mae']:.6g}"
    )

    print(
        f"RMSE: {metrics['real_rmse']:.6g}"
    )

    print(
        f"R²  : {metrics['real_r2']:.4f}"
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    model_path = MODEL_DIR / model_name

    artifact = {
        "pipeline": pipeline,
        "features": FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "target": target_column,
        "target_transform": "log10",
        "metrics": metrics,
        "training_rows": len(X_train),
        "test_rows": len(X_test),
        "training_documents": sorted(
            train_groups.unique()
        ),
        "test_documents": sorted(
            test_groups.unique()
        ),
    }

    joblib.dump(
        artifact,
        model_path,
    )

    print()
    print(f"Model saved:")
    print(model_path)

    return metrics


# ============================================================
# Main
# ============================================================

def main():

    otr_metrics = train_model(
        data_file=OTR_FILE,
        target_column="OTR_Updated_Num",
        log_target_column="OTR_log10",
        model_name="otr_model.joblib",
    )

    wvtr_metrics = train_model(
        data_file=WVTR_FILE,
        target_column="WVTR_Updated_Num",
        log_target_column="WVTR_log10",
        model_name="wvtr_model.joblib",
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)

    print()
    print("OTR model:")
    print(
        f"  Log R² : {otr_metrics['log_r2']:.4f}"
    )
    print(
        f"  Real R²: {otr_metrics['real_r2']:.4f}"
    )

    print()
    print("WVTR model:")
    print(
        f"  Log R² : {wvtr_metrics['log_r2']:.4f}"
    )
    print(
        f"  Real R²: {wvtr_metrics['real_r2']:.4f}"
    )

    print()
    print("Models:")
    print(
        MODEL_DIR / "otr_model.joblib"
    )
    print(
        MODEL_DIR / "wvtr_model.joblib"
    )

    print()
    print(
        "IMPORTANT: These are baseline models. "
        "Do not interpret the metrics as proof of "
        "engineering-grade prediction accuracy."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()
