# Step 01 Completion Summary — Tournament Data Refresh

## Objective — Complete

> Create `data/2026.yaml` and `data/csv/2026.csv` with the 2026 NCAA tournament bracket, matching the exact format of the 2024 files. Optionally build a script to semi-automate this for future years.

All three parts delivered: the YAML, the CSV, and helper scripts for automation.

## Format Requirements

| Requirement | Status |
|---|---|
| `data/2026.yaml` matches 2024 structure exactly | Done. Same structure: `Year`, `WestPlays`, four regions with seeds 1–16 |
| `WestPlays` set correctly from official bracket | Done. `WestPlays: Midwest` (East plays South, West plays Midwest in the Final Four) |
| Team names are canonical names from `alternate_names.py` | Done. All 68 teams resolve through `get_definitive_name()` |
| Region names match `GeographicRegion` enum | Done. Same four regions as 2024 (East, Midwest, South, West) — no enum change needed |
| `data/csv/2026.csv` matches 2024 CSV format | Done. Same header, same column order |
| First Four teams use `-Playoff` region suffix in CSV | Done. 8 First Four teams across 4 matchups included with `-Playoff` suffixes |
| All 68 teams in CSV with W-L records | Done. Records fetched from ESPN team API |

## Team Name Resolution — Complete

7 new aliases were added to `alternate_names.py` for ESPN name variants that didn't previously resolve:

| Alias | Canonical |
|---|---|
| `Hawai'i` | Hawaii |
| `Long Island University`, `LIU` | Long Island |
| `Miami (OH)` | Miami (Ohio) |
| `Pennsylvania` | Penn |
| `Prairie View A&M` | Prairie View |
| `Queens University` | Queens |
| `St. John's` | Saint John's |

No brand-new teams needed to be added — all 68 tournament teams already existed in the dictionary.

## Data Sources — Used ESPN API (Option B from the plan)

Three scripts were created under `scripts/`:

- **`fetch_bracket_2026.py`** — pulls all first-round + First Four games from ESPN's scoreboard API across 4 tournament dates, extracts team names, seeds, and regions from the game event notes
- **`fetch_records_2026.py`** — backfills W-L records by hitting the ESPN team API for each team
- **`check_names.py`** — validates that all canonical names and ESPN aliases resolve correctly

These aren't yet a single polished `scripts/fetch_tournament_data.py` that auto-generates YAML and CSV output files (as the plan's Option B envisions). They were used as building blocks to extract and verify the data, which was then used to hand-craft the final files. A future improvement would be to unify them into one script that writes the files directly.

## Validation Checklist

| Check | Status |
|---|---|
| `poetry run play --strategy BestRankWins --year 2026` runs without error | Done (tested via `poetry run python` — CLI has a pre-existing typer/click version bug unrelated to our changes) |
| All team names resolve | Done. Verified by `check_names.py` and by the tests |
| YAML has 4 regions with 16 teams each | Done. Parser loads 64 teams |
| Team names match between YAML and CSV | Done. Same canonical names used |
| Win/loss records are reasonable | Done. Fetched from ESPN |
| Full test suite passes | Done. 81 passed, 60 skipped (mathstats skipped for 2023 and 2026 as expected), 0 failures |

## Additional Work Done (beyond the plan)

- **`gamewinner/bracket/__init__.py`** — updated `this_year = 2026` and added `2026` to `available_years`
- **`tests/conftest.py`** — added `2026` to testable years, added skip for mathstats strategies on 2026 (no Evan Miya data yet)

## Files Created or Modified

| File | Action |
|---|---|
| `data/2026.yaml` | Created |
| `data/csv/2026.csv` | Created |
| `gamewinner/teams/alternate_names.py` | Modified — added 7 aliases |
| `gamewinner/bracket/__init__.py` | Modified — added 2026 to available years, set as current year |
| `tests/conftest.py` | Modified — added 2026 to testable years, skip mathstats for 2026 |
| `scripts/fetch_bracket_2026.py` | Created |
| `scripts/fetch_records_2026.py` | Created |
| `scripts/check_names.py` | Created |

## First Four Caveat

The YAML currently has placeholder picks for the 4 First Four slots (the favored team from each matchup). These should be updated after the First Four games are played on 3/17–3/18, before filling out actual strategy brackets. The matchups are documented in YAML comments:

- **South 16**: Lehigh vs Prairie View (Lehigh in YAML)
- **Midwest 16**: UMBC vs Howard (UMBC in YAML)
- **Midwest 11**: Miami (Ohio) vs SMU (Miami (Ohio) in YAML)
- **West 11**: NC State vs Texas (NC State in YAML)

## Pre-existing Issue: CLI typer/click Incompatibility

The `poetry run play` CLI crashes on `--help` due to a `TypeError: Parameter.make_metavar() missing 1 required positional argument: 'ctx'`. This is a version incompatibility between `typer ^0.12.3` and the installed version of `click`. This is pre-existing and unrelated to the 2026 data refresh. The bracket engine itself works correctly when invoked via `poetry run python` directly.

## What's Next

**Step 02 (`02-data-refresh-evan-miya.md`)** — create `gamewinner/strategies/mathstats/data/2026.csv` with Evan Miya team ratings so the mathstats strategies can run on 2026 data.
