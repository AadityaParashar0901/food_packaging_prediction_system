from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "raw" / "Food-Pack-Mapper" / "processed.csv"
MODEL_DIR = ROOT / "trained_models"

MODEL_DIR.mkdir(exist_ok=True)


def clean_numeric(series):
    return pd.to_numeric(
        series,
        errors="coerce",
    )


def load_data():
    print(f"Loading:\n{DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    return df


def prepare_data(df):
    # Rename columns to simple Python names
    rename = {
        "Base Material": "base_material",
        "Type": "material_type",
        "Secondary Material": "secondary_material",
        "Composition": "composition",
        "Plasticizer": "plasticizer",

        "WVTR_Updated_Num": "wvtr",
        "OTR_Updated_Num": "otr",

        "thickness_Updated_Num": "thickness",

        "temperature_Updated_Num": "temperature",
        "RH_Updated_Num": "relative_humidity",

        "OTR_temperature_Num": "otr_temperature",
        "OTR_RH_Num": "otr_relative_humidity",
    }

    df = df.rename(columns=rename)

    required = [
        "base_material",
        "material_type",
        "secondary_material",
        "thickness",
        "temperature",
        "relative_humidity",
        "otr",
        "wvtr",
    ]

    for column in required:
        if column not in df.columns:
            df[column] = np.nan

    numeric_columns = [
        "thickness",
        "temperature",
        "relative_humidity",
        "otr",
        "wvtr",
        "otr_temperature",
        "otr_relative_humidity",
    ]

    for column in numeric_columns:
        df[column] = clean_numeric(df[column])

    # Keep observations where at least one actual permeability
    # measurement exists.
    df = df[
        df["otr"].notna() |
        df["wvtr"].notna()
    ].copy()

    # Remove impossible/non-positive measurements.
    df.loc[df["otr"] <= 0, "otr"] = np.nan
    df.loc[df["wvtr"] <= 0, "wvtr"] = np.nan

    return df


def train_target(df, target):
    print("\n" + "=" * 60)
    print(f"Training target: {target}")

    feature_columns = [
        "base_material",
        "material_type",
        "secondary_material",
        "thickness",
        "temperature",
        "relative_humidity",
        "otr_temperature",
        "otr_relative_humidity",
    ]

    data = df[
        feature_columns + [target]
    ].copy()

    data = data.dropna(
        subset=[target]
    )

    if len(data) < 20:
        print(
            f"Not enough rows for {target}: {len(data)}"
        )
        return None

    X = data[feature_columns]
    y = data[target]

    categorical = [
        "base_material",
        "material_type",
        "secondary_material",
    ]

    numerical = [
        "thickness",
        "temperature",
        "relative_humidity",
        "otr_temperature",
        "otr_relative_humidity",
    ]

    categorical_pipeline = Pipeline(
        [
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
            ),
        ]
    )

    numerical_pipeline = Pipeline(
        [
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        [
            (
                "categorical",
                categorical_pipeline,
                categorical,
            ),
            (
                "numerical",
                numerical_pipeline,
                numerical,
            ),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=2,
    )

    pipeline = Pipeline(
        [
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

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    pipeline.fit(
        X_train,
        y_train,
    )

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    r2 = r2_score(
        y_test,
        predictions,
    )

    print(f"Training rows : {len(X_train)}")
    print(f"Testing rows  : {len(X_test)}")
    print(f"MAE           : {mae:.4f}")
    print(f"R²            : {r2:.4f}")

    output = (
        MODEL_DIR /
        f"packaging_{target}_model.joblib"
    )

    joblib.dump(
        pipeline,
        output,
    )

    print(f"Saved: {output}")

    return pipeline


def main():
    df = load_data()

    print("\nPreparing data...")
    df = prepare_data(df)

    print(
        f"Usable permeability rows: {len(df)}"
    )

    print("\nAvailable measurements:")
    print(
        f"OTR  : {df['otr'].notna().sum()}"
    )
    print(
        f"WVTR : {df['wvtr'].notna().sum()}"
    )

    otr_model = train_target(
        df,
        "otr",
    )

    wvtr_model = train_target(
        df,
        "wvtr",
    )

    print("\nTraining complete.")

    if otr_model is None:
        print("WARNING: OTR model was not created.")

    if wvtr_model is None:
        print("WARNING: WVTR model was not created.")


if __name__ == "__main__":
    main()
