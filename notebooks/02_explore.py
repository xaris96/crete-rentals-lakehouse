# Databricks notebook source
path = "/Volumes/crete_rentals/raw/landing/2026-09-25/listings.csv.gz"

df = (
    spark.read
    .option("header", True)
    .option("multiLine", True)
    .option("escape", '"')
    .csv(path)
)

display(df)


# COMMAND ----------

print(df.count(), len(df.columns))


# COMMAND ----------

base = "/Volumes/crete_rentals/raw/landing/2026-09-25"

calendar = spark.read.csv(f"{base}/calendar.csv.gz", header=True, multiLine=True, escape='"')
reviews = spark.read.csv(f"{base}/reviews.csv.gz", header=True, multiLine=True, escape='"')

calendar.printSchema()
reviews.printSchema()


# COMMAND ----------

from pyspark.sql import functions as F

print("γραμμές:", calendar.count())
print("listings:", calendar.select("listing_id").distinct().count())

display(calendar.agg(F.min("date"), F.max("date")))
display(calendar.groupBy("available").count())
display(calendar.limit(10))


# COMMAND ----------

print("γραμμές:", reviews.count())
print("listings με review:", reviews.select("listing_id").distinct().count())

display(reviews.agg(F.min("date"), F.max("date")))
display(reviews.limit(10))


# COMMAND ----------

listings = spark.read.csv(f"{base}/listings.csv.gz", header=True, multiLine=True, escape='"')

orphans = reviews.join(listings, reviews.listing_id == listings.id, "left_anti")
print("ορφανά reviews:", orphans.count())
