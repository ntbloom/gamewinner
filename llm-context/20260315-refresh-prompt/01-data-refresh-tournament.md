# Step 01: Tournament Data Refresh for 2026

## Objective

Create `data/2026.yaml` and `data/csv/2026.csv` with the 2026 NCAA tournament bracket, matching the exact format of the 2024 files. Optionally build a script to semi-automate this for future years.

## Exact Format Requirements

### `data/2026.yaml`

Reference: `data/2024.yaml`. Must match this structure exactly:

```yaml
Year: 2026
WestPlays: East   # which two regions meet in the Final Four (the other two also meet)

East:
  1: TeamName
  2: TeamName
  # ... seeds 1-16

Midwest:
  1: TeamName
  # ... seeds 1-16

South:
  1: TeamName
  # ... seeds 1-16

West:
  1: TeamName
  # ... seeds 1-16
```

**Important notes:**
- The `WestPlays` field determines Final Four matchups. Check the official bracket for which regions are paired.
- Team names must be the **canonical names** from `gamewinner/teams/alternate_names.py`. Use `get_definitive_name()` or look up the canonical form manually.
- The template at `data/_template.yaml` shows the skeleton.
- The 2024 regions were East, Midwest, South, West. The 2026 regions may differ — check the official bracket. If the region names change, the `GeographicRegion` enum in `gamewinner/bracket/geographic_region.py` may need updating.

### `data/csv/2026.csv`

Reference: `data/csv/2024.csv`. Exact format:

```csv
Team Name,Region,Regional Rank,Wins,Losses
Connecticut,East,1,31,3
Stetson,East,16,22,12
...
```

**Important notes:**
- Team names must exactly match the YAML file (canonical names).
- `Region` is the region name from the YAML, with `-Playoff` suffix for First Four teams (e.g., `West-Playoff`).
- First Four: two teams share the same `Regional Rank` with a `-Playoff` region. Both appear in the CSV.
- `Wins` and `Losses` are the regular-season record at time of selection.
- The 2024 CSV has 64 teams (no First Four entries visible). The 2022 CSV does have First Four entries. Check if 2026 has play-in games and include them.

### Team name resolution

Every team name in both files must pass through `get_definitive_name()` successfully. This means:
1. Check `gamewinner/teams/alternate_names.py` for existing entries.
2. For any new tournament team not already in the dictionary, **add it** with reasonable aliases.
3. Use the canonical spelling exactly (case-sensitive after normalization).

## Data Sources

- **ESPN bracket page**: `https://www.espn.com/mens-college-basketball/tournament/bracket`
- **CBS Sports**: `https://www.cbssports.com/college-basketball/bracketology/`
- **NCAA.com**: Official tournament bracket
- **ESPN API** (undocumented but functional): `https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard` — can filter by date and groups to get tournament games

The LLM performing this step should use its web access tools (fetch_url, etc.) to pull the actual bracket data from one of these sources.

## Implementation Approach

### Option A: Manual data entry (fastest, simplest)
Just look at the official bracket and type the YAML and CSV by hand. This is how 2023 and 2024 were done. It takes ~30 minutes.

### Option B: Script-assisted (better for future years)
Create `scripts/fetch_tournament_data.py` that:
1. Fetches the bracket from ESPN or CBS
2. Parses team names, seeds, regions, and records
3. Resolves names through `get_definitive_name()` (importing from the codebase)
4. Outputs `data/YYYY.yaml` and `data/csv/YYYY.csv`

Either approach is fine. If building a script, keep it simple — a single Python file using `requests` and `beautifulsoup4` (both already available or easily added). Don't over-engineer.

## Validation

After creating the files, verify:
- [ ] `poetry run play --strategy BestRankWins --year 2026` runs without error
- [ ] All team names resolve (no `ValueError` from `get_definitive_name()`)
- [ ] The YAML has 4 regions with 16 teams each
- [ ] Team names match between YAML and CSV
- [ ] Win/loss records are reasonable

Note: Mathstats strategies will fail at this point because `gamewinner/strategies/mathstats/data/2026.csv` doesn't exist yet. That's expected — handled in Step 02. Use `BestRankWins` or `WorstRankWins` for testing since they don't need Evan Miya data.

## Files to create or modify

| File | Action |
|------|--------|
| `data/2026.yaml` | Create |
| `data/csv/2026.csv` | Create |
| `gamewinner/teams/alternate_names.py` | Modify — add any new teams/aliases |
| `scripts/fetch_tournament_data.py` | Create (optional, for automation) |

## Next Step
After completing tournament data refresh, proceed to **02-data-refresh-evan-miya.md**.