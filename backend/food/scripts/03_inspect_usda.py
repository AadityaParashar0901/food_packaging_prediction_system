from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/usda")

csv_files = list(DATA_DIR.rglob("*.csv"))

print(f"Found {len(csv_files)} CSV files:\n")

for file in csv_files:
    print(file)

print("\n=== PREVIEWING CSV FILES ===\n")

for file in csv_files:
    try:
        df = pd.read_csv(
            file,
            encoding="latin1",
            nrows=5,
        )

        print("=" * 70)
        print(file)
        print("=" * 70)

        print("Rows previewed:", len(df))
        print("Columns:")

        for column in df.columns:
            print(f"  {column}")

        print()

    except Exception as e:
        print(f"Could not read {file}: {e}")
