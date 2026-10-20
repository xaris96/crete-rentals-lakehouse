"""Download Inside Airbnb snapshot files for Crete into a Unity Catalog volume."""

BASE_URL = "https://data.insideairbnb.com/greece/crete/crete/"


def snapshot_url(snapshot_date, file_name):
    return f"{BASE_URL}{snapshot_date}/data/{file_name}"
