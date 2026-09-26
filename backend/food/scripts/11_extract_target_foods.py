from pathlib import Path
import pandas as pd


INPUT_FILE = Path("data/usda_samples.csv")
OUTPUT_FILE = Path("data/usda_target_foods.csv")


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
# COMMODITY RULES
# ---------------------------------------------------------

RULES = {

    "apple": {
        "include": [
            r"\bAPPLES?,",
        ],
        "exclude": [],
    },

    "banana": {
        "include": [
            r"\bBANANAS?,",
        ],
        "exclude": [],
    },

    "tomato": {
        "include": [
            r"\bTOMATOES?,\s+(GRAPE|ROMA)\b",
        ],
        "exclude": [
            r"\bCANNED\b",
            r"\bPUREE\b",
        ],
    },

    "bread": {
        "include": [
            r"^White bread,",
            r"^Whole wheat bread,",
        ],
        "exclude": [],
    },

    "cheese": {
        "include": [
            r"\bCHEESE\b",
            r"\bCheddar cheese\b",
            r"\bMozzarella cheese\b",
            r"\bParmesan cheese\b",
            r"\bCottage cheese\b",
        ],
        "exclude": [
            r"APPLEBEES",
            r"BURGER KING",
            r"CHICK FIL",
            r"DENNYS",
            r"IHOP",
            r"MCDONALDS",
            r"PANERA",
            r"SUBWAY",
        ],
    },

}


# ---------------------------------------------------------
# EXTRACT
# ---------------------------------------------------------

result_frames = []


for commodity, rules in RULES.items():

    mask = pd.Series(
        False,
        index=df.index,
    )

    # Include rules
    for pattern in rules["include"]:

        mask = mask | df[
            "sample_description"
        ].str.contains(
            pattern,
            case=False,
            regex=True,
            na=False,
        )

    # Exclude rules
    for pattern in rules["exclude"]:

        mask = mask & ~df[
            "sample_description"
        ].str.contains(
            pattern,
            case=False,
            regex=True,
            na=False,
        )

    matches = df[mask].copy()

    matches.insert(
        0,
        "commodity",
        commodity,
    )

    result_frames.append(matches)

    print()
    print("=" * 80)
    print(f"{commodity.upper()}")
    print("=" * 80)
    print(f"Samples: {len(matches):,}")
    print(
        f"Descriptions: "
        f"{matches['sample_description'].nunique():,}"
    )

    for description in (
        matches["sample_description"]
        .drop_duplicates()
        .sort_values()
    ):
        print(f"  {description}")


# ---------------------------------------------------------
# COMBINE
# ---------------------------------------------------------

if result_frames:

    result = pd.concat(
        result_frames,
        ignore_index=True,
    )

else:

    result = pd.DataFrame()


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

result.to_csv(
    OUTPUT_FILE,
    index=False,
)


print()
print("=" * 80)
print("TARGET FOOD DATASET CREATED")
print("=" * 80)

print(f"Output: {OUTPUT_FILE}")
print(f"Rows:   {len(result):,}")
print(f"Cols:   {len(result.columns):,}")

print()
print("Samples by commodity:")

print(
    result["commodity"]
    .value_counts()
    .sort_index()
    .to_string()
)
