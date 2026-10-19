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
