# GameWinner March 2026 Refresh — Overall Plan

## Project Overview

GameWinner is a March Madness bracket predictor. You define a strategy (a Python class that picks winners), run it against a tournament bracket, and get a printed bracket with results.

The system has these layers:

1. **Tournament data** — `data/YYYY.yaml` (bracket structure + seeding) and `data/csv/YYYY.csv` (team name, region, seed, W/L record). Currently has 2023 and 2024.
2. **Advanced stats data** — `gamewinner/strategies/mathstats/data/YYYY.csv` — Evan Miya team ratings used by "mathstats" strategies. Currently has 2023 and 2024.
3. **Strategy framework** — `IStrategy` (base) and `IMathStatsStrategy` (loads Evan Miya CSV and provides `MSProps` per team). Concrete strategies live in `gamewinner/strategies/mathstats/derived/`.
4. **CLI** — `cli.py` uses Typer. `poetry run play --strategy SlothfireSteady --year 2024`.
5. **Printers** — output formatters (currently `BasicFilePrinter` and a color text printer).

## Critical Architectural Details

### CSV parsing is positional, not header-based
`IMathStatsStrategy.prepare()` in `imathstats.py` reads the Evan Miya CSV using **positional tuple unpacking** — it skips the header row and destructures each row into 20 named variables. It does NOT use `csv.DictReader` or pandas. This means:
- Column **order** matters, not column names in the header.
- Adding/removing/reordering columns requires updating the unpacking code in `prepare()`.
- The `MSProps` NamedTuple defines the canonical field names that all strategies use.

### MSProps fields (from 2024 format, 20 columns)
```
rank_overall, raw_offense, raw_defense, raw_overall,
adjust_opponent, adjust_pace, rank_offense, rank_defense,
raw_tempo, rank_tempo, rank_injury, rank_home, rank_roster,
obj_kills_per_game, obj_kills_concede_per_game,
obj_kills_total, obj_kills_conceded_total, obj_wins, obj_losses
```
Plus `resume_rank` as a deprecated field with default `-1` (it was in 2023 but dropped in 2024).

### 2023 → 2024 column changes already happened
The 2023 CSV had 16 columns (no `opponent_adjust`, `pace_adjust`, `wins`, `losses`, and it had `ResumeRank`). The 2024 CSV has 20 columns with those additions and `ResumeRank` removed. The code was updated to match.

### Team name resolution
`gamewinner/teams/alternate_names.py` has a comprehensive dictionary mapping canonical names to aliases. `get_definitive_name()` normalizes names from any data source. New teams or name variants must be added here.

### Available years are discovered from `data/`
`gamewinner/bracket/__init__.py` likely scans for YAML files to build `available_years`. Adding `data/2026.yaml` should make 2026 available.

## Implementation Plan — Step Order

| Step | File | Summary |
|------|------|---------|
| 01 | `01-data-refresh-tournament.md` | Create `data/2026.yaml` and `data/csv/2026.csv` from public bracket data |
| 02 | `02-data-refresh-evan-miya.md` | Create `gamewinner/strategies/mathstats/data/2026.csv` from Evan Miya |
| 03 | `03-strategy-updates.md` | Update `imathstats.py` if columns changed; update `alternate_names.py` for new teams |
| 04 | `04-strategy-rendering.md` | Make it easy to run strategies and generate readable reports |
| 05 | `05-tournament-tracking.md` | Track live results, score brackets, produce standings |
| 06 | `06-strategy-builder-yaml.md` | YAML-based strategy definition + code generation |
| 07 | `07-strategy-builder-interactive.md` | Optional: TUI or web UI for building strategies interactively |

Steps 01–03 are the highest priority and must happen before the tournament starts. Steps 04–05 are needed during the tournament. Steps 06–07 are nice-to-haves.

## Key Risks

1. **Evan Miya format change** — The biggest risk. The 2026 site may have different columns, renamed stats, or require a paid subscription. The 2023→2024 transition already required changes. Expect the same.
2. **Team name mismatches** — Different data sources use different names ("UConn" vs "Connecticut", "McNeese" vs "McNeese State"). The `alternate_names.py` system handles this, but new teams and new aliases will need to be added.
3. **First Four teams** — These use the `<Region>-Playoff` convention and need special handling.
4. **Time pressure** — The tournament bracket is typically announced on Selection Sunday and games start 4 days later.

## Non-Goals (for now)
- Rewriting the core bracket engine
- Changing the CSV parsing to pandas/DictReader (tempting but risky mid-season)
- Adding new strategy base classes beyond `IMathStatsStrategy`