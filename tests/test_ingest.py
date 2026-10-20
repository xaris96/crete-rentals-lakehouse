from crete_rentals.ingest import snapshot_url


def test_snapshot_url():
    assert (
        snapshot_url("2026-09-25", "listings.csv.gz")
        == "https://data.insideairbnb.com/greece/crete/crete/2026-09-25/data/listings.csv.gz"
    )
