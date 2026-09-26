from pathlib import Path
import pandas as pd


INPUT_FILE = Path("data/usda_target_foods.csv")
OUTPUT_FILE = Path("data/ml_food_features.csv")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

print("Loading target food dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
    low_memory=False,
)

print(f"Input rows: {len(df):,}")


# ---------------------------------------------------------
# USDA FEATURES WE WANT
# ---------------------------------------------------------

FEATURE_MAP = {
    "Water": "moisture",
    "Total lipid (fat)": "fat",
    "Protein": "protein",
    "Carbohydrate, by difference": "carbohydrate",
    "Fiber, total dietary": "fiber",
    "Ash": "ash",
    "Sugars, total including NLEA": "sugars",
    "Sodium, Na": "sodium",
}


# ---------------------------------------------------------
# BUILD COMPACT DATASET
# ---------------------------------------------------------

base_columns = [
    "commodity",
    "sample_group",
    "sample_fdc_id",
    "sample_description",
]

missing_base = [
    column
    for column in base_columns
    if column not in df.columns
]

if missing_base:
    raise ValueError(
        f"Missing required columns: {missing_base}"
    )


features = df[base_columns].copy()


print()
print("=" * 80)
print("USDA FEATURE AVAILABILITY")
print("=" * 80)


for source_column, output_column in FEATURE_MAP.items():

    if source_column in df.columns:

        features[output_column] = pd.to_numeric(
            df[source_column],
            errors="coerce",
        )

        available = features[output_column].notna().sum()
        missing = features[output_column].isna().sum()

        print(
            f"{output_column:15s} "
            f"available: {available:4d} "
            f"missing: {missing:4d}"
        )

    else:

        features[output_column] = pd.NA

        print(
            f"{output_column:15s} "
            f"NOT FOUND in USDA dataset"
        )


# ---------------------------------------------------------
# SORT
# ---------------------------------------------------------

features = features.sort_values(
    [
        "commodity",
        "sample_description",
        "sample_group",
    ]
).reset_index(drop=True)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

features.to_csv(
    OUTPUT_FILE,
    index=False,
)


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()
print("=" * 80)
print("ML FOOD FEATURE DATASET CREATED")
print("=" * 80)

print(f"Output: {OUTPUT_FILE}")
print(f"Rows:   {len(features):,}")
print(f"Cols:   {len(features.columns):,}")


print()
print("=" * 80)
print("SAMPLES BY COMMODITY")
print("=" * 80)

print(
    features["commodity"]
    .value_counts()
    .sort_index()
    .to_string()
)


print()
print("=" * 80)
print("FEATURE PREVIEW")
print("=" * 80)

preview_columns = [
    "commodity",
    "sample_description",
    "moisture",
    "fat",
    "protein",
    "carbohydrate",
    "fiber",
    "ash",
    "sugars",
    "sodium",
]

available_preview = [
    column
    for column in preview_columns
    if column in features.columns
]

print(
    features[available_preview]
    .head(15)
    .to_string(index=False)
)


print()
print("=" * 80)
print("MISSING VALUE PERCENTAGES")
print("=" * 80)

for column in FEATURE_MAP.values():

    missing_percent = (
        features[column].isna().mean() * 100
    )

    print(
        f"{column:15s}: "
        f"{missing_percent:6.2f}% missing"
    )


print()
print("Done.")
