from crete_rentals import ingest
from crete_rentals.ingest import download_file, snapshot_url, upload_snapshot


def test_snapshot_url():
    assert (
        snapshot_url("2026-09-25", "listings.csv.gz")
        == "https://data.insideairbnb.com/greece/crete/crete/2026-09-25/data/listings.csv.gz"
    )


def test_download_file_skips_existing_file(tmp_path, monkeypatch):
    existing = tmp_path / "2026-09-25" / "listings.csv.gz"
    existing.parent.mkdir()
    existing.write_bytes(b"already here")

    def fail_if_called(url, path):
        raise AssertionError("should not download a file that already exists")

    monkeypatch.setattr(ingest, "urlretrieve", fail_if_called)

    assert download_file("2026-09-25", "listings.csv.gz", tmp_path) == existing


class FakeFiles:
    """Stands in for client.files, recording calls instead of talking to Databricks."""

    def __init__(self):
        self.directories = []
        self.uploads = {}

    def create_directory(self, directory_path):
        self.directories.append(directory_path)

    def upload(self, file_path, contents, overwrite):
        self.uploads[file_path] = contents.read()


class FakeClient:
    def __init__(self):
        self.files = FakeFiles()


def test_upload_snapshot_puts_every_file_in_the_snapshot_folder(tmp_path):
    snapshot_dir = tmp_path / "2026-09-25"
    snapshot_dir.mkdir()
    for file_name in ingest.FILES:
        (snapshot_dir / file_name).write_bytes(file_name.encode())
    client = FakeClient()

    uploaded = upload_snapshot(client, "2026-09-25", tmp_path, volume_dir="/Volumes/c/s/v")

    assert client.files.directories == ["/Volumes/c/s/v/2026-09-25"]
    assert uploaded == [f"/Volumes/c/s/v/2026-09-25/{name}" for name in ingest.FILES]
    assert client.files.uploads["/Volumes/c/s/v/2026-09-25/reviews.csv.gz"] == b"reviews.csv.gz"
