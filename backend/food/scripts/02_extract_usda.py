from pathlib import Path
import zipfile

DATA_DIR = Path("data")
ZIP_FILE = DATA_DIR / "usda_foundation_foods.zip"
EXTRACT_DIR = DATA_DIR / "usda"

if not ZIP_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {ZIP_FILE}\n"
        "Run 01_download_usda.py first."
    )

EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

print("Extracting USDA dataset...")

with zipfile.ZipFile(ZIP_FILE, "r") as zip_file:
    zip_file.extractall(EXTRACT_DIR)

print(f"Extracted to: {EXTRACT_DIR}")
