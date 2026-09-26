from pathlib import Path
import pandas as pd
import re


INPUT_FILE = Path("data/usda_samples.csv")


SEARCH_TERMS = {
    "apple": [
        "apple",
        "apples",
    ],
    "banana": [
        "banana",
        "bananas",
    ],
    "potato": [
        "potato",
        "potatoes",
    ],
    "tomato": [
        "tomato",
        "tomatoes",
    ],
    "rice": [
        "rice",
    ],
    "wheat": [
        "wheat",
    ],
    "nuts": [
        "almond",
        "walnut",
        "pecan",
        "cashew",
        "pistachio",
        "hazelnut",
        "peanut",
        "macadamia",
        "nut",
        "nuts",
    ],
    "chips": [
        "chip",
        "chips",
    ],
    "cheese": [
        "cheese",
    ],
    "bread": [
        "bread",
    ],
}


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


for category, terms in SEARCH_TERMS.items():

    print()
    print("=" * 100)
    print(f"CATEGORY: {category.upper()}")
    print("=" * 100)

    masks = []

    for term in terms:

        pattern = rf"\b{re.escape(term)}\b"

        masks.append(
            df["sample_description"].str.contains(
                pattern,
                case=False,
                regex=True,
                na=False,
            )
        )

    combined_mask = masks[0]

    for mask in masks[1:]:
        combined_mask = combined_mask | mask

    matches = df[combined_mask].copy()

    descriptions = (
        matches["sample_description"]
        .value_counts()
        .sort_index()
    )

    print(
        f"Matching samples: {len(matches):,}"
    )

    print(
        f"Unique descriptions: {len(descriptions):,}"
    )

    print()

    if len(descriptions) == 0:
        print("No matches found.")
        continue

    for description, count in descriptions.items():

        print(
            f"{count:4d} samples | {description}"
        )
