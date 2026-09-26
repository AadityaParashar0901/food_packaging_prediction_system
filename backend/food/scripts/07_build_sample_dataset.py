from pathlib import Path
import pandas as pd


INPUT_FILE = Path("data/usda_combined.csv")
OUTPUT_FILE = Path("data/usda_samples.csv")


print("Loading USDA combined dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
    low_memory=False,
)

df = df.reset_index(drop=True)


# ---------------------------------------------------------
# 1. Create sample groups
#
# Every sample_food starts a new sample.
# Everything until the next sample_food belongs
# to that sample.
# ---------------------------------------------------------

df["sample_group"] = (
    df["data_type"]
    .eq("sample_food")
    .cumsum()
)


# ---------------------------------------------------------
# 2. Extract sample metadata
#
# The sample_food row contains the actual sample-level
# description and FDC ID.
# ---------------------------------------------------------

sample_metadata = df[
    df["data_type"] == "sample_food"
][
    [
        "sample_group",
        "fdc_id",
        "description",
        "publication_date",
    ]
].copy()


sample_metadata = sample_metadata.rename(
    columns={
        "fdc_id": "sample_fdc_id",
        "description": "sample_description",
    }
)


# ---------------------------------------------------------
# 3. Keep nutrient records
# ---------------------------------------------------------

nutrients = df[
    df["data_type"] == "sub_sample_food"
].copy()


nutrients = nutrients[
    nutrients["name"].notna()
].copy()


# ---------------------------------------------------------
# 4. Keep useful nutrient fields
# ---------------------------------------------------------

nutrients = nutrients[
    [
        "sample_group",
        "nutrient_id",
        "name",
        "unit_name",
        "amount",
    ]
].copy()


# ---------------------------------------------------------
# 5. Clean nutrient names
# ---------------------------------------------------------

nutrients["name"] = (
    nutrients["name"]
    .astype(str)
    .str.strip()
)


nutrients["unit_name"] = (
    nutrients["unit_name"]
    .astype(str)
    .str.strip()
)


# ---------------------------------------------------------
# 6. Convert nutrient amounts to numeric
# ---------------------------------------------------------

nutrients["amount"] = pd.to_numeric(
    nutrients["amount"],
    errors="coerce",
)


nutrients = nutrients[
    nutrients["amount"].notna()
].copy()


# ---------------------------------------------------------
# 7. Show basic nutrient statistics
# ---------------------------------------------------------

print()
print("=" * 80)
print("NUTRIENT RECORDS")
print("=" * 80)

print(
    f"Records: {len(nutrients):,}"
)

print(
    f"Unique samples: "
    f"{nutrients['sample_group'].nunique():,}"
)

print(
    f"Unique nutrients: "
    f"{nutrients['name'].nunique():,}"
)


# ---------------------------------------------------------
# 8. Pivot nutrients
#
# IMPORTANT:
# Do NOT include fdc_id here.
#
# Multiple sub_sample_food FDC IDs can belong to the
# same sample.
# ---------------------------------------------------------

print()
print("=" * 80)
print("PIVOTING NUTRIENTS")
print("=" * 80)


sample_nutrients = nutrients.pivot_table(
    index="sample_group",
    columns="name",
    values="amount",
    aggfunc="mean",
).reset_index()


sample_nutrients.columns.name = None


# ---------------------------------------------------------
# 9. Combine nutrient columns with sample metadata
# ---------------------------------------------------------

sample_data = sample_metadata.merge(
    sample_nutrients,
    on="sample_group",
    how="inner",
)


# ---------------------------------------------------------
# 10. Save
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)


sample_data.to_csv(
    OUTPUT_FILE,
    index=False,
)


# ---------------------------------------------------------
# 11. Summary
# ---------------------------------------------------------

print()
print("=" * 80)
print("SAMPLE DATASET CREATED")
print("=" * 80)

print(f"Output: {OUTPUT_FILE}")
print(f"Rows:   {len(sample_data):,}")
print(f"Cols:   {len(sample_data.columns):,}")


print()
print("=" * 80)
print("FIRST 10 SAMPLES")
print("=" * 80)

print(
    sample_data[
        [
            "sample_group",
            "sample_fdc_id",
            "sample_description",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


print()
print("=" * 80)
print("NUTRIENT PREVIEW")
print("=" * 80)

preview_columns = [
    "sample_group",
    "sample_description",
    "Water",
    "Total lipid (fat)",
    "Fiber, total dietary",
    "Potassium, K",
    "Calcium, Ca",
    "Sodium, Na",
]

available_columns = [
    column
    for column in preview_columns
    if column in sample_data.columns
]

print(
    sample_data[available_columns]
    .head(10)
    .to_string(index=False)
)
