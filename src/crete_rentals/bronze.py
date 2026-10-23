"""Bronze layer: raw snapshots as Delta tables with snapshot_date and ingested_at.

Ingestion is idempotent: re-running a snapshot must not duplicate rows.
"""


def read_raw_csv(spark, path):
    return spark.read.csv(path, header=True, multiLine=True, escape='"')
