from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")

food_file = next(DATA_DIR.rglob("usda_combined.csv"))

print(f"Reading: {food_file}")
print()

food = pd.read_csv(
    food_file,
    encoding="latin1",
    low_memory=False,
)


print("=" * 80)
print("FOOD TABLE COLUMNS")
print("=" * 80)

for i, column in enumerate(food.columns):
    print(f"{i:2d}: {column}")


print()
print("=" * 80)
print("APPLES, GALA RECORDS")
print("=" * 80)

apple_rows = food[
    food["description"]
    .astype(str)
    .str.contains(
        "APPLES, GALA",
        case=False,
        na=False,
    )
]


print(
    f"Found {len(apple_rows)} rows"
)

print()


# Display all columns because we need to find
# the relationship between sample_food,
# market_acquisition and sub_sample_food.

print(
    apple_rows.to_string(
        index=False
    )
)
