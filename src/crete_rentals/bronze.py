"""Bronze layer: raw snapshots as Delta tables with snapshot_date and ingested_at.

Ingestion is idempotent: re-running a snapshot must not duplicate rows.
"""
