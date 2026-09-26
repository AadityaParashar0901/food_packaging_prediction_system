import requests
from pathlib import Path

# USDA Foundation Foods download
URL = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_csv_2026-04-30.zip"

DATA_DIR = Path("data")
ZIP_FILE = DATA_DIR / "usda_foundation_foods.zip"

DATA_DIR.mkdir(parents=True, exist_ok=True)

print("Downloading USDA Foundation Foods...")

response = requests.get(URL, stream=True, timeout=60)
response.raise_for_status()

total = int(response.headers.get("content-length", 0))
downloaded = 0

with open(ZIP_FILE, "wb") as f:
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            f.write(chunk)
            downloaded += len(chunk)

            if total:
                percent = downloaded / total * 100
                print(
                    f"\rProgress: {percent:6.2f}%",
                    end="",
                )

print("\n")
print(f"Downloaded to: {ZIP_FILE}")
print(f"Size: {ZIP_FILE.stat().st_size / 1024 / 1024:.2f} MB")
