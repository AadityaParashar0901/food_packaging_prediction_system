from pathlib import Path
import pandas as pd


DATA_DIR = Path("data/usda")
OUTPUT_FILE = Path("data/usda_combined.csv")


def find_csv(filename):
    """
    Find a USDA CSV recursively.
    """
    matches = list(DATA_DIR.rglob(filename))

    if not matches:
        raise FileNotFoundError(
            f"Could not find {filename} inside {DATA_DIR}"
        )

    if len(matches) > 1:
        print(f"Warning: multiple {filename} files found:")
        for match in matches:
            print(f"  {match}")

    return matches[0]


print("Locating USDA files...")

food_file = find_csv("food.csv")
food_nutrient_file = find_csv("food_nutrient.csv")
nutrient_file = find_csv("nutrient.csv")

print(f"food.csv:          {food_file}")
print(f"food_nutrient.csv: {food_nutrient_file}")
print(f"nutrient.csv:      {nutrient_file}")


print("\nLoading food table...")

food = pd.read_csv(
    food_file,
    encoding="latin1",
    low_memory=False,
)

print(f"Food rows: {len(food):,}")


print("\nLoading food_nutrient table...")

food_nutrient = pd.read_csv(
    food_nutrient_file,
    encoding="latin1",
    low_memory=False,
)

print(f"Food nutrient rows: {len(food_nutrient):,}")


print("\nLoading nutrient table...")

nutrient = pd.read_csv(
    nutrient_file,
    encoding="latin1",
    low_memory=False,
)

print(f"Nutrient rows: {len(nutrient):,}")


# ---------------------------------------------------------
# Validate keys
# ---------------------------------------------------------

required_food_columns = {"fdc_id"}
required_food_nutrient_columns = {"fdc_id", "nutrient_id"}
required_nutrient_columns = {"id"}

if not required_food_columns.issubset(food.columns):
    raise ValueError(
        f"food.csv is missing required columns: "
        f"{required_food_columns - set(food.columns)}"
    )

if not required_food_nutrient_columns.issubset(
    food_nutrient.columns
):
    raise ValueError(
        "food_nutrient.csv is missing required columns: "
        f"{required_food_nutrient_columns - set(food_nutrient.columns)}"
    )

if not required_nutrient_columns.issubset(nutrient.columns):
    raise ValueError(
        "nutrient.csv is missing required columns: "
        f"{required_nutrient_columns - set(nutrient.columns)}"
    )


# ---------------------------------------------------------
# Rename nutrient ID so the relationship is obvious
# ---------------------------------------------------------

nutrient = nutrient.rename(
    columns={
        "id": "nutrient_id"
    }
)


# ---------------------------------------------------------
# Join food -> food_nutrient
# ---------------------------------------------------------

print("\nJoining food -> food_nutrient...")

combined = food.merge(
    food_nutrient,
    on="fdc_id",
    how="left",
    suffixes=("", "_food_nutrient"),
)

print(f"Rows after first join: {len(combined):,}")


# ---------------------------------------------------------
# Join -> nutrient
# ---------------------------------------------------------

print("Joining -> nutrient...")

combined = combined.merge(
    nutrient,
    on="nutrient_id",
    how="left",
    suffixes=("", "_nutrient"),
)

print(f"Rows after second join: {len(combined):,}")


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

combined.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("\n========================================")
print("USDA DATASET COMBINED")
print("========================================")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows:   {len(combined):,}")
print(f"Cols:   {len(combined.columns):,}")


print("\nColumns:")
for column in combined.columns:
    print(f"  {column}")
