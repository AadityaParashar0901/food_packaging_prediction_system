from pathlib import Path
import pandas as pd


INPUT_FILE = Path("data/usda_combined.csv")


print("Loading USDA dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
    low_memory=False,
)

df = df.reset_index(drop=True)


# ---------------------------------------------------------
# 1. Add row number so we can see the original sequence
# ---------------------------------------------------------

df["row_number"] = df.index


# ---------------------------------------------------------
# 2. Inspect a few sample_food records
# ---------------------------------------------------------

sample_rows = df[
    df["data_type"] == "sample_food"
].head(5)


print()
print("=" * 100)
print("FIRST 5 SAMPLE_FOOD RECORDS")
print("=" * 100)

print(
    sample_rows[
        [
            "row_number",
            "fdc_id",
            "data_type",
            "description",
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# 3. Print the records surrounding each sample_food
# ---------------------------------------------------------

print()
print("=" * 100)
print("RECORDS AROUND SAMPLE_FOOD")
print("=" * 100)


for _, sample in sample_rows.iterrows():

    row = int(sample["row_number"])

    start = max(0, row - 1)
    end = min(len(df), row + 12)

    nearby = df.iloc[start:end]

    print()
    print("-" * 100)
    print(
        f"SAMPLE STARTING AT ROW {row}"
    )
    print("-" * 100)

    print(
        nearby[
            [
                "row_number",
                "fdc_id",
                "data_type",
                "description",
                "id",
                "nutrient_id",
                "name",
                "unit_name",
                "amount",
            ]
        ].to_string(index=False)
    )


# ---------------------------------------------------------
# 4. Inspect APPLES, GALA specifically
# ---------------------------------------------------------

print()
print("=" * 100)
print("APPLES, GALA RELATIONSHIP")
print("=" * 100)


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
    apple[
        [
            "row_number",
            "fdc_id",
            "data_type",
            "description",
            "id",
            "nutrient_id",
            "name",
            "unit_name",
            "amount",
        ]
    ].head(100).to_string(index=False)
)


# ---------------------------------------------------------
# 5. Show all IDs by data type for APPLES, GALA
# ---------------------------------------------------------

print()
print("=" * 100)
print("APPLES, GALA FDC IDs BY DATA TYPE")
print("=" * 100)


for data_type, group in apple.groupby(
    "data_type",
    dropna=False,
):

    print()
    print(f"DATA TYPE: {data_type}")

    print(
        group[
            [
                "fdc_id",
                "description",
            ]
        ]
        .drop_duplicates()
        .to_string(index=False)
    )


# ---------------------------------------------------------
# 6. Check whether fdc_id maps to one data_type
# ---------------------------------------------------------

print()
print("=" * 100)
print("FDC_ID DATA TYPE CONSISTENCY")
print("=" * 100)


fdc_types = (
    df.groupby("fdc_id")["data_type"]
    .nunique()
)


print(
    "FDC IDs appearing under multiple data types:",
    (fdc_types > 1).sum()
)

print(
    "FDC IDs appearing under exactly one data type:",
    (fdc_types == 1).sum()
)


# ---------------------------------------------------------
# 7. Check whether an fdc_id has multiple descriptions
# ---------------------------------------------------------

fdc_descriptions = (
    df.groupby("fdc_id")["description"]
    .nunique()
)


print()
print(
    "FDC IDs with multiple descriptions:",
    (fdc_descriptions > 1).sum()
)


# ---------------------------------------------------------
# 8. Final summary
# ---------------------------------------------------------

print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)

print(
    "Total rows:",
    len(df)
)

print(
    "Unique FDC IDs:",
    df["fdc_id"].nunique()
)

print(
    "Unique nutrient IDs:",
    df["nutrient_id"].nunique()
)

print(
    "Unique descriptions:",
    df["description"].nunique()
)
