from pathlib import Path
import pandas as pd


INPUT_FILE = Path("data/usda_combined.csv")


print("Loading USDA combined dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
    low_memory=False,
)


print()
print("=" * 80)
print("DATASET OVERVIEW")
print("=" * 80)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


print()
print("=" * 80)
print("DATA TYPES")
print("=" * 80)

print(
    df["data_type"]
    .value_counts(dropna=False)
)


print()
print("=" * 80)
print("APPLES, GALA DATA TYPES")
print("=" * 80)

apple = df[
    df["description"]
    .astype(str)
    .str.contains(
        "APPLES, GALA",
        case=False,
        na=False,
    )
].copy()

print(
    apple["data_type"]
    .value_counts(dropna=False)
)


print()
print("=" * 80)
print("APPLES, GALA FDC ID / DATA TYPE SEQUENCE")
print("=" * 80)

sequence = (
    apple[
        [
            "fdc_id",
            "data_type",
            "description",
        ]
    ]
    .drop_duplicates()
)

print(
    sequence.to_string(
        index=False
    )
)


print()
print("=" * 80)
print("SAMPLE FOOD RECORDS")
print("=" * 80)

sample_foods = apple[
    apple["data_type"] == "sample_food"
][
    [
        "fdc_id",
        "description",
    ]
].drop_duplicates()

print(
    sample_foods.to_string(
        index=False
    )
)

print()
print(
    f"Number of sample_food records: "
    f"{len(sample_foods)}"
)


print()
print("=" * 80)
print("FOUNDATION FOOD RECORDS")
print("=" * 80)

foundation = apple[
    apple["data_type"] == "foundation_food"
][
    [
        "fdc_id",
        "description",
    ]
].drop_duplicates()

print(
    foundation.to_string(
        index=False
    )
)

print()
print(
    f"Number of foundation_food records: "
    f"{len(foundation)}"
)
