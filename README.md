# Crete Rentals Lakehouse

[![CI](https://github.com/xaris96/crete-rentals-lakehouse/actions/workflows/ci.yml/badge.svg)](https://github.com/xaris96/crete-rentals-lakehouse/actions/workflows/ci.yml)

A Databricks lakehouse built on public Inside Airbnb snapshots for Crete (listings, calendar, reviews).
Raw files land in a bronze layer, are cleaned and historised (SCD Type 2) in silver, and are modelled as a star schema in gold.
Data quality checks gate every run, and the pipeline is deployed as a Databricks Job with Asset Bundles.

## Local development (Windows, PowerShell)

Requires Python 3.11 and Java 17+ (PySpark runs on the JVM).

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
ruff check .
ruff format --check .
pytest
```

## Loading a snapshot

Free Edition compute has no access to insideairbnb.com, so snapshots are downloaded on a local
machine and uploaded to the `crete_rentals.raw.landing` volume with the Databricks SDK.

One-time setup: install the [Databricks CLI](https://docs.databricks.com/aws/en/dev-tools/cli/install)
and log in to the workspace (opens a browser):

```powershell
winget install Databricks.DatabricksCLI
databricks auth login --host https://<your-workspace>.cloud.databricks.com --profile DEFAULT
```

Then, for each snapshot:

```powershell
python -m crete_rentals.ingest 2026-09-25
```

Files already downloaded are skipped; files in the volume are overwritten, so the command is safe to re-run.
