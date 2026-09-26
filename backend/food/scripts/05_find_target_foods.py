from pathlib import Path
import re

import pandas as pd
from rapidfuzz import fuzz


INPUT_FILE = Path("data/usda_combined.csv")
OUTPUT_FILE = Path("data/target_food_candidates.csv")


TARGETS = [
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


# Extra words that are valid representations of a target.
ALIASES = {
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
        "nut",
        "nuts",
    ],

    "chips": [
        "chip",
        "chips",
    ],

    "cheese": [
        "cheese",
        "cheeses",
    ],

    "bread": [
        "bread",
        "breads",
    ],
}


# Words that indicate the USDA food is probably
# a processed/product form of another target.
#
# These are target-specific.
EXCLUDE_WORDS = {

    "apple": [
        "juice",
        "sauce",
        "pie",
        "cider",
        "butter",
        "jam",
        "jelly",
    ],

    "banana": [
        "bread",
        "muffin",
        "pudding",
        "smoothie",
        "cake",
        "chips",
    ],

    "potato": [
        "chips",
        "french",
        "fries",
        "mashed",
        "fried",
        "flakes",
        "starch",
    ],

    "tomato": [
        "sauce",
        "paste",
        "juice",
        "ketchup",
        "puree",
    ],

    "rice": [
        "milk",
        "flour",
        "cracker",
        "noodle",
        "cake",
    ],

    "wheat": [
        "bread",
        "pasta",
        "cracker",
        "cereal",
        "flour",
    ],

    "nuts": [
        "butter",
        "flour",
        "milk",
        "oil",
    ],

    "chips": [
        "chocolate",
    ],

    "cheese": [
        "sauce",
        "pizza",
        "flavored",
    ],

    "bread": [
        "banana",
        "garlic",
        "breaded",
        "crumb",
    ],
}


def normalize(text):
    """
    Normalize USDA descriptions.

    Examples:

        'APPLES'
            -> 'apples'

        'Apples, Gala'
            -> 'apples gala'

        'Potatoes - Russet'
            -> 'potatoes russet'
    """

    text = str(text).lower()

    # Replace punctuation with spaces.
    text = re.sub(r"[^a-z0-9]+", " ", text)

    # Remove repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def singularize(word):
    """
    Very small/simple singularization helper.

    We deliberately do NOT use a full NLP stemmer here.
    Food names often have irregular forms such as:

        potato -> potatoes
        tomato -> tomatoes

    Those are handled through ALIASES.
    """

    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"

    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]

    return word


def contains_alias(description, aliases):
    """
    Check whether any alias occurs as a complete word
    or as a normalized singular/plural form.
    """

    words = description.split()

    normalized_words = {
        singularize(word)
        for word in words
    }

    normalized_aliases = {
        singularize(alias)
        for alias in aliases
    }

    return bool(normalized_words & normalized_aliases)


def exclusion_found(description, exclusions):
    """
    Check whether an exclusion word occurs as a complete word.
    """

    words = set(description.split())

    for word in exclusions:
        if word in words:
            return True

    return False


def calculate_score(target, description):
    """
    Calculate a relevance score.

    Higher score = more likely to be a useful
    representation of the target commodity.
    """

    aliases = ALIASES[target]

    words = description.split()

    score = 0

    # -------------------------------------------------
    # Exact alias match
    # -------------------------------------------------

    if description in aliases:
        score += 100

    # -------------------------------------------------
    # Alias appears as a complete word
    # -------------------------------------------------

    if contains_alias(description, aliases):
        score += 50

    # -------------------------------------------------
    # Description starts with an alias
    #
    # Examples:
    #
    #   apples
    #   apples gala
    #   potato russet
    # -------------------------------------------------

    for alias in aliases:

        if description.startswith(alias):
            score += 30

            break

    # -------------------------------------------------
    # Fuzzy similarity
    # -------------------------------------------------

    fuzzy_scores = [
        fuzz.token_set_ratio(alias, description)
        for alias in aliases
    ]

    if fuzzy_scores:
        score += max(fuzzy_scores) * 0.25

    # -------------------------------------------------
    # Short/simple descriptions are usually better
    # representatives of the commodity.
    # -------------------------------------------------

    if len(words) == 1:
        score += 30

    elif len(words) == 2:
        score += 15

    return score


print("Loading combined USDA dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
    low_memory=False,
)


# We only need one row per food for candidate discovery.
foods = df[
    [
        "fdc_id",
        "description",
        "data_type",
        "food_category_id",
    ]
].drop_duplicates("fdc_id")


foods["normalized_description"] = (
    foods["description"]
    .fillna("")
    .map(normalize)
)


print(f"Unique USDA foods: {len(foods):,}")
print()


all_candidates = []


for target in TARGETS:

    print("=" * 80)
    print(f"TARGET: {target}")
    print("=" * 80)

    candidates = []

    aliases = ALIASES[target]
    exclusions = EXCLUDE_WORDS.get(target, [])

    for _, row in foods.iterrows():

        description = row["normalized_description"]

        if not description:
            continue

        # ---------------------------------------------
        # First filter:
        # Does this description contain an alias?
        # ---------------------------------------------

        if not contains_alias(description, aliases):
            continue

        # ---------------------------------------------
        # Second filter:
        # Remove misleading processed foods.
        # ---------------------------------------------

        if exclusion_found(description, exclusions):
            continue

        # ---------------------------------------------
        # Calculate relevance.
        # ---------------------------------------------

        score = calculate_score(
            target,
            description
        )

        candidates.append({
            "commodity": target,
            "fdc_id": row["fdc_id"],
            "description": row["description"],
            "data_type": row["data_type"],
            "food_category_id": row["food_category_id"],
            "score": round(score, 2),
        })

    candidates_df = pd.DataFrame(candidates)

    if candidates_df.empty:

        print("No candidates found.")
        print()

        continue

    candidates_df = candidates_df.sort_values(
        "score",
        ascending=False
    )

    # Keep the best 30 candidates for manual inspection.
    candidates_df = candidates_df.head(30)

    all_candidates.append(candidates_df)

    print(f"Candidates found: {len(candidates_df)}")
    print()

    for _, row in candidates_df.head(15).iterrows():

        print(
            f"{row['score']:7.2f} | "
            f"{row['fdc_id']} | "
            f"{row['description']}"
        )

    print()


if not all_candidates:

    raise RuntimeError(
        "No target food candidates were found."
    )


result = pd.concat(
    all_candidates,
    ignore_index=True
)


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


result.to_csv(
    OUTPUT_FILE,
    index=False
)


print("=" * 80)
print("TARGET FOOD SEARCH COMPLETE")
print("=" * 80)

print(f"Output: {OUTPUT_FILE}")
print(f"Candidate rows: {len(result):,}")

print()
print("Review target_food_candidates.csv before")
print("creating the final commodity -> FDC ID mapping.")
