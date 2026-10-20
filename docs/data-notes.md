# Data notes

What I learn about the Inside Airbnb Crete data while exploring it.

## Source

- Inside Airbnb, Crete: https://insideairbnb.com/get-the-data/
- License: CC BY 4.0 (attribution required)

## Files per snapshot

| File | Grain |
|---|---|
| `listings.csv.gz` | one row per listing |
| `calendar.csv.gz` | one row per listing per day, for the next 365 days |
| `reviews.csv.gz` | one row per review |

## Snapshot dates used

- 2026-09-25

## Known data issues

- `listings.csv.gz` has free-text fields (e.g. `host_about`, `description`) with line breaks
  and doubled quotes inside them. Read with `multiLine=True` and `escape='"'`, otherwise
  Spark splits them into fake rows (52,956 rows instead of 27,381 for 2026-09-25).
- `description` contains HTML tags such as `<b>` and `<br />`.
