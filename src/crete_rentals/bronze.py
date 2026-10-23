"""Bronze layer: raw snapshots as Delta tables with snapshot_date and ingested_at.

Ingestion is idempotent: re-running a snapshot must not duplicate rows.
"""

from pyspark.sql import functions as F

LANDING_DIR = "/Volumes/crete_rentals/raw/landing"
BRONZE_SCHEMA = "crete_rentals.bronze"
TABLES = ["listings", "calendar", "reviews"]


def read_raw_csv(spark, path):
    # Text fields contain line breaks and doubled quotes, see docs/data-notes.md.
    return spark.read.csv(path, header=True, multiLine=True, escape='"')


def add_metadata(df, snapshot_date):
    # lit() marks snapshot_date as a value; a bare string would be read as a column name.
    return df.withColumn("snapshot_date", F.to_date(F.lit(snapshot_date))).withColumn(
        "ingested_at", F.current_timestamp()
    )


def write_bronze(df, table, snapshot_date):
    # replaceWhere swaps only this snapshot's rows, so a re-run replaces them instead of
    # appending a second copy. mergeSchema lets a later snapshot add new columns.
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", f"snapshot_date = '{snapshot_date}'")
        .option("mergeSchema", "true")
        .saveAsTable(table)
    )


def load_snapshot(spark, snapshot_date, landing_dir=LANDING_DIR, schema=BRONZE_SCHEMA):
    results = []
    for name in TABLES:
        df = read_raw_csv(spark, f"{landing_dir}/{snapshot_date}/{name}.csv.gz")
        table = f"{schema}.{name}"
        write_bronze(add_metadata(df, snapshot_date), table, snapshot_date)
        results.append(table)
    return results
