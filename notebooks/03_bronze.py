# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze
# MAGIC Loads one snapshot from the landing volume into the `crete_rentals.bronze` Delta tables.
# MAGIC Safe to re-run: the snapshot's rows are replaced, not duplicated.

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

import sys

sys.path.append("../src")

from crete_rentals.bronze import load_snapshot

# COMMAND ----------

dbutils.widgets.text("snapshot_date", "2026-09-25")
snapshot_date = dbutils.widgets.get("snapshot_date")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS crete_rentals.bronze

# COMMAND ----------

for table in load_snapshot(spark, snapshot_date):
    print(f"Loaded {table}")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'listings' AS table_name, snapshot_date, count(*) AS row_count
# MAGIC FROM crete_rentals.bronze.listings GROUP BY snapshot_date
# MAGIC UNION ALL
# MAGIC SELECT 'calendar', snapshot_date, count(*)
# MAGIC FROM crete_rentals.bronze.calendar GROUP BY snapshot_date
# MAGIC UNION ALL
# MAGIC SELECT 'reviews', snapshot_date, count(*)
# MAGIC FROM crete_rentals.bronze.reviews GROUP BY snapshot_date
