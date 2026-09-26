from pathlib import Path
import pandas as pd
import re


INPUT_FILE = Path("data/usda_samples.csv")


COMMODITIES = [
    "apple",
    "banana",
    "potato",
    "tomato",
    "rice",
    "wheat",
    "nuts",
    "chips",
    "cheese",
    "bread",
]


df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
    low_memory=False,
)


df["sample_description"] = (
    df["sample_description"]
    .astype(str)
    .str.strip()
)


# ---------------------------------------------------------
# Search helper
# ---------------------------------------------------------

def search_descriptions(keyword):
    pattern = rf"\b{re.escape(keyword)}\b"

    mask = df["sample_description"].str.contains(
        pattern,
        case=False,
        regex=True,
        na=False,
    )

    return df.loc[mask]


# ---------------------------------------------------------
# Find candidate foods
# ---------------------------------------------------------

for commodity in COMMODITIES:

    matches = search_descriptions(commodity)

    descriptions = (
        matches["sample_description"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    print()
    print("=" * 100)
    print(f"TARGET: {commodity.upper()}")
    print("=" * 100)

    print(
        f"Matching samples: {len(matches):,}"
    )

    print(
        f"Unique descriptions: {len(descriptions):,}"
    )

    print()

    if not descriptions:
        print("No direct matches found.")
        continue

    for description in descriptions:
        count = (
            matches["sample_description"]
            == description
        ).sum()

        print(
            f"{count:4d} samples | {description}"
        )
