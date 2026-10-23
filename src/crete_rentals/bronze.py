"""Bronze layer: raw snapshots as Delta tables with snapshot_date and ingested_at.

Ingestion is idempotent: re-running a snapshot must not duplicate rows.
"""

from pyspark.sql import functions as F


def read_raw_csv(spark, path):
    # Text fields contain line breaks and doubled quotes, see docs/data-notes.md.
    return spark.read.csv(path, header=True, multiLine=True, escape='"')


def add_metadata(df, snapshot_date):
    # lit() marks snapshot_date as a value; a bare string would be read as a column name.
    return df.withColumn("snapshot_date", F.to_date(F.lit(snapshot_date))).withColumn(
        "ingested_at", F.current_timestamp()
    )
