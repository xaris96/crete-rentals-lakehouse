"""Download Inside Airbnb snapshot files for Crete into a Unity Catalog volume."""

from pathlib import Path
from urllib.request import urlretrieve

BASE_URL = "https://data.insideairbnb.com/greece/crete/crete/"
FILES = ["listings.csv.gz", "calendar.csv.gz", "reviews.csv.gz"]


def snapshot_url(snapshot_date, file_name):
    return f"{BASE_URL}{snapshot_date}/data/{file_name}"


def download_file(snapshot_date, file_name, dest_dir):
    folder = Path(dest_dir) / snapshot_date
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / file_name
    url = snapshot_url(snapshot_date, file_name)
    urlretrieve(url, file_path)

    return file_path


def download_snapshot(snapshot_date, dest_dir):
    results = []
    for file_name in FILES:
        file_path = download_file(snapshot_date, file_name, dest_dir)
        results.append(file_path)
    return results
