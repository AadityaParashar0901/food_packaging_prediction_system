from pathlib import Path
import pandas as pd
import random


INPUT_FILE = Path("data/ml_food_features.csv")
OUTPUT_FILE = Path("data/packaging_training_data.csv")

random.seed(42)


# =========================================================
# LOAD FOOD FEATURES
# =========================================================

print("Loading food features...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
)

print(f"Food samples: {len(df):,}")


# =========================================================
# PACKAGING PROFILES
# =========================================================
#
# IMPORTANT:
# These are prototype training labels.
# They are NOT claimed to be USDA measurements.
#
# Later, these can be replaced with experimentally/literature
# validated packaging data.
# =========================================================

PROFILES = {

    "apple": {
        "pH": 3.8,
        "water_activity": 0.98,
        "respiration_rate": 25,
        "ethylene_rate": 10,

        "material": "Breathable PE film",
        "thickness": 40,
        "OTR": 5000,
        "WVTR": 15,
        "sealability": "Good",
        "MAP_suitability": "High",
        "mechanical_strength": "Medium",
    },

    "banana": {
        "pH": 5.0,
        "water_activity": 0.97,
        "respiration_rate": 35,
        "ethylene_rate": 15,

        "material": "Perforated PE film",
        "thickness": 50,
        "OTR": 7000,
        "WVTR": 18,
        "sealability": "Good",
        "MAP_suitability": "Medium",
        "mechanical_strength": "Medium",
    },

    "tomato": {
        "pH": 4.3,
        "water_activity": 0.97,
        "respiration_rate": 30,
        "ethylene_rate": 8,

        "material": "Micro-perforated PE film",
        "thickness": 50,
        "OTR": 6000,
        "WVTR": 16,
        "sealability": "Good",
        "MAP_suitability": "High",
        "mechanical_strength": "Medium",
    },

    "bread": {
        "pH": 5.5,
        "water_activity": 0.94,
        "respiration_rate": 5,
        "ethylene_rate": 0,

        "material": "LDPE film",
        "thickness": 40,
        "OTR": 2000,
        "WVTR": 8,
        "sealability": "Excellent",
        "MAP_suitability": "Medium",
        "mechanical_strength": "Medium",
    },

    "cheese": {
        "pH": 5.2,
        "water_activity": 0.90,
        "respiration_rate": 0,
        "ethylene_rate": 0,

        "material": "PET/PE laminate",
        "thickness": 80,
        "OTR": 100,
        "WVTR": 3,
        "sealability": "Excellent",
        "MAP_suitability": "High",
        "mechanical_strength": "High",
    },
}


# =========================================================
# STORAGE / TRANSPORT OPTIONS
# =========================================================

STORAGE_OPTIONS = {
    "ambient": {
        "temperature": 25,
        "relative_humidity": 60,
    },

    "chilled": {
        "temperature": 5,
        "relative_humidity": 85,
    },

    "frozen": {
        "temperature": -18,
        "relative_humidity": 90,
    },
}


TRANSPORT_OPTIONS = [
    "normal",
    "refrigerated",
    "frozen",
]


# =========================================================
# GENERATE TRAINING ROWS
# =========================================================

rows = []


for _, food in df.iterrows():

    commodity = str(
        food["commodity"]
    ).lower().strip()

    if commodity not in PROFILES:
        continue

    profile = PROFILES[commodity]

    # Generate several storage/transport scenarios
    for storage_type, storage in STORAGE_OPTIONS.items():

        for transportation_condition in TRANSPORT_OPTIONS:

            # Shelf life is intentionally varied.
            if storage_type == "ambient":
                shelf_life = random.choice(
                    [3, 5, 7, 10, 14]
                )

            elif storage_type == "chilled":
                shelf_life = random.choice(
                    [7, 10, 14, 21, 30]
                )

            else:
                shelf_life = random.choice(
                    [30, 60, 90, 180]
                )

            row = {

                # -----------------------------------------
                # FOOD / USDA FEATURES
                # -----------------------------------------

                "commodity": commodity,

                "sample_group": food["sample_group"],

                "sample_fdc_id": food["sample_fdc_id"],

                "moisture": food["moisture"],

                "fat": food["fat"],

                "ash": food["ash"],

                "sodium": food["sodium"],


                # -----------------------------------------
                # FOOD PHYSIOLOGY
                # -----------------------------------------

                "pH": profile["pH"],

                "water_activity": profile[
                    "water_activity"
                ],

                "respiration_rate": profile[
                    "respiration_rate"
                ],

                "ethylene_rate": profile[
                    "ethylene_rate"
                ],


                # -----------------------------------------
                # STORAGE / TRANSPORT
                # -----------------------------------------

                "temperature": storage[
                    "temperature"
                ],

                "relative_humidity": storage[
                    "relative_humidity"
                ],

                "desired_shelf_life": shelf_life,

                "storage_type": storage_type,

                "transportation_condition":
                    transportation_condition,


                # -----------------------------------------
                # PACKAGING TARGETS
                # -----------------------------------------

                "recommended_material":
                    profile["material"],

                "film_thickness":
                    profile["thickness"],

                "OTR_requirement":
                    profile["OTR"],

                "WVTR_requirement":
                    profile["WVTR"],

                "sealability":
                    profile["sealability"],

                "MAP_suitability":
                    profile["MAP_suitability"],

                "mechanical_strength":
                    profile["mechanical_strength"],
            }

            rows.append(row)


# =========================================================
# CREATE DATAFRAME
# =========================================================

training_df = pd.DataFrame(rows)


# =========================================================
# SAVE
# =========================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

training_df.to_csv(
    OUTPUT_FILE,
    index=False,
)


# =========================================================
# SUMMARY
# =========================================================

print()
print("=" * 80)
print("PACKAGING TRAINING DATASET CREATED")
print("=" * 80)

print(f"Output: {OUTPUT_FILE}")
print(f"Rows:   {len(training_df):,}")
print(f"Cols:   {len(training_df.columns):,}")


print()
print("=" * 80)
print("ROWS BY COMMODITY")
print("=" * 80)

print(
    training_df["commodity"]
    .value_counts()
    .sort_index()
    .to_string()
)


print()
print("=" * 80)
print("PACKAGING MATERIALS")
print("=" * 80)

print(
    training_df["recommended_material"]
    .value_counts()
    .to_string()
)


print()
print("=" * 80)
print("PREVIEW")
print("=" * 80)

preview_columns = [
    "commodity",
    "moisture",
    "fat",
    "pH",
    "water_activity",
    "temperature",
    "desired_shelf_life",
    "storage_type",
    "recommended_material",
    "film_thickness",
    "OTR_requirement",
    "WVTR_requirement",
]

print(
    training_df[
        preview_columns
    ].head(20).to_string(index=False)
)


print()
print("Done.")
