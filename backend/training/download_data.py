from pathlib import Path
import subprocess
import requests
import zipfile
import shutil


ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

USDA_URL = (
    "https://fdc.nal.usda.gov/"
    "fdc-datasets/FoodData_Central_foundation_food_csv_2026-04-30.zip"
)

ZENODO_URL = (
    "https://zenodo.org/records/6353580/files/"
    "Packaging-performances-PBSA-LDH_v01_TER_WP6_D6-2%20%284%29.zip"
    "?download=1"
)

GITHUB_REPO = "https://github.com/whps0620/Food-Pack-Mapper.git"


def download(url: str, destination: Path):
    if destination.exists():
        print(f"[skip] {destination}")
        return

    print(f"[download] {url}")

    response = requests.get(
        url,
        stream=True,
        timeout=60,
        headers={"User-Agent": "food-packaging-project/1.0"},
    )

    response.raise_for_status()

    with destination.open("wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    print(f"[saved] {destination}")


def clone_repo():
    destination = RAW / "Food-Pack-Mapper"

    if destination.exists():
        print(f"[skip] {destination}")
        return

    print("[git] cloning Food-Pack-Mapper")

    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            GITHUB_REPO,
            str(destination),
        ],
        check=True,
    )


def extract_zip(zip_path: Path, destination: Path):
    if destination.exists() and any(destination.iterdir()):
        print(f"[skip] already extracted: {destination}")
        return

    destination.mkdir(parents=True, exist_ok=True)

    print(f"[extract] {zip_path}")

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(destination)


def main():
    print("\n=== Food Packaging Dataset Downloader ===\n")

    # USDA Foundation Foods
    usda_zip = RAW / "usda_foundation_foods.zip"

    download(
        USDA_URL,
        usda_zip,
    )

    extract_zip(
        usda_zip,
        RAW / "usda_foundation",
    )

    # Zenodo experimental packaging data
    zenodo_zip = RAW / "zenodo_packaging.zip"

    download(
        ZENODO_URL,
        zenodo_zip,
    )

    extract_zip(
        zenodo_zip,
        RAW / "zenodo_packaging",
    )

    # 2026 Food-Pack-Mapper processed dataset/code
    clone_repo()

    print("\nDone.")
    print(f"Raw data is in: {RAW}")


if __name__ == "__main__":
    main()
