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

## Snapshot 2026-09-25 at a glance

| File | Rows | Notes |
|---|---|---|
| `listings.csv.gz` | 27,381 | 90 columns |
| `calendar.csv.gz` | 9,994,065 | 27,381 listings × exactly 365 days |
| `reviews.csv.gz` | 672,725 | 23,237 listings have at least one review |

- The folder date (2026-09-25, also in `scrape_id`) is not the day the data was collected:
  `last_scraped` is 2026-09-28 or 2026-09-29.
- Each listing's calendar starts on its own scrape day, so `calendar.date` spans
  2026-09-28 to 2027-09-28 (366 dates) even though every listing has 365 rows.
- `calendar.available` is the text `t` / `f`, not a boolean.
- `reviews.date` goes from 2010-10-15 to 2026-09-29.
- About 4,100 listings have no reviews at all.
- Every `reviews.listing_id` exists in `listings.id` (a `left_anti` join returns 0 rows).
- Read without `inferSchema`, every column is a string, including ids, dates and numbers.

## Known data issues

- `listings.csv.gz` has free-text fields (e.g. `host_about`, `description`) with line breaks
  and doubled quotes inside them. Read with `multiLine=True` and `escape='"'`, otherwise
  Spark splits them into fake rows (52,956 rows instead of 27,381 for 2026-09-25).
- `description` contains HTML tags such as `<b>` and `<br />`.
- `reviews.comments` also contains HTML (`<br/>`) and is written in many languages.
- `calendar.csv.gz` is a single gzip file, which Spark cannot split, so one task reads all
  ~10M rows. Every action on a DataFrame read straight from it re-reads the whole file.
