"""Download Inside Airbnb snapshot files for Crete into a Unity Catalog volume.

Free Edition compute cannot reach insideairbnb.com, so this runs on a local machine:
it downloads a snapshot into a local folder, then uploads it to the landing volume.

Usage:
    python -m crete_rentals.ingest 2026-09-25
"""

import argparse
from pathlib import Path
from urllib.request import urlretrieve

from databricks.sdk import WorkspaceClient

BASE_URL = "https://data.insideairbnb.com/greece/crete/crete/"
FILES = ["listings.csv.gz", "calendar.csv.gz", "reviews.csv.gz"]
VOLUME_DIR = "/Volumes/crete_rentals/raw/landing"


def snapshot_url(snapshot_date, file_name):
    return f"{BASE_URL}{snapshot_date}/data/{file_name}"


def download_file(snapshot_date, file_name, dest_dir):
    folder = Path(dest_dir) / snapshot_date
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / file_name
    if file_path.exists():
        return file_path
    url = snapshot_url(snapshot_date, file_name)
    # Download to a .part file and rename when done, so an interrupted download
    # never leaves a half file that the exists() check above would trust.
    part_path = file_path.with_name(file_name + ".part")
    urlretrieve(url, part_path)
    part_path.replace(file_path)

    return file_path


def download_snapshot(snapshot_date, dest_dir):
    results = []
    for file_name in FILES:
        file_path = download_file(snapshot_date, file_name, dest_dir)
        results.append(file_path)
    return results


def upload_snapshot(client, snapshot_date, local_dir, volume_dir=VOLUME_DIR):
    target_dir = f"{volume_dir}/{snapshot_date}"
    client.files.create_directory(target_dir)
    results = []
    for file_name in FILES:
        target_path = f"{target_dir}/{file_name}"
        with open(Path(local_dir) / snapshot_date / file_name, "rb") as f:
            client.files.upload(target_path, f, overwrite=True)
        results.append(target_path)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Download an Inside Airbnb Crete snapshot and upload it to the landing volume."
    )
    parser.add_argument("snapshot_date", help="snapshot date as YYYY-MM-DD, e.g. 2026-09-25")
    parser.add_argument("--local-dir", default="data", help="local download folder")
    parser.add_argument("--profile", default=None, help="Databricks CLI profile to use")
    args = parser.parse_args()

    for file_path in download_snapshot(args.snapshot_date, args.local_dir):
        print(f"Downloaded {file_path}")

    client = WorkspaceClient(profile=args.profile)
    for target_path in upload_snapshot(client, args.snapshot_date, args.local_dir):
        print(f"Uploaded   {target_path}")


if __name__ == "__main__":
    main()
