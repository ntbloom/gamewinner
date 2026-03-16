# Step 02: Evan Miya Statistics Data Refresh for 2026

## Objective

Create `gamewinner/strategies/mathstats/data/2026.csv` with advanced team statistics from Evan Miya, matching the column structure and order of the 2024 file so that existing strategies work.
## Critical: The Exact 2024 Column Format
The existing code in `imathstats.py` parses this CSV **positionally** (not by header name). The `prepare()` method does:
```python
for row in reader:
    (
        rank_overall,      # col 0
        name,              # col 1
        raw_offense,       # col 2  (obpr)
        raw_defense,       # col 3  (dbpr)
        raw_overall,       # col 4  (bpr)
        adjust_opponent,   # col 5
        adjust_pace,       # col 6
        rank_offense,      # col 7
        rank_defense,      # col 8
        raw_tempo,         # col 9
        rank_tempo,        # col 10
        rank_injury,       # col 11
        rank_home,         # col 12
        rank_roster,       # col 13
        obj_kills_per_game,            # col 14
        obj_kills_concede_per_game,    # col 15
        obj_kills_total,               # col 16
        obj_kills_conceded_total,      # col 17
        obj_wins,          # col 18
        obj_losses,        # col 19
    ) = row
```
The 2024 CSV header is:
```
rank,team,obpr,dbpr,bpr,opponent_adjust,pace_adjust,off_rank,def_rank,tempo,tempo_rank,rank_inj,home_rank,roster_rank,runs_per_game,runs_conceded_per_game,runs_total,runs_conceded_total,wins,losses
```

**The output CSV for 2026 must have exactly these 20 columns in exactly this order.** The header row names don't matter to the parser (it's skipped), but should match for human readability.
## What the 2024 columns mean (Evan Miya terminology)
| CSV col | MSProps field | Evan Miya concept |
|---------|---------------|-------------------|
| rank | rank_overall | Overall BPR rank |
| team | (name) | Team name |
| obpr | raw_offense | Offensive BPR rating |
| dbpr | raw_defense | Defensive BPR rating |
| bpr | raw_overall | Combined BPR rating |
| opponent_adjust | adjust_opponent | Strength of schedule adjustment |
| pace_adjust | adjust_pace | Pace/tempo adjustment factor |
| off_rank | rank_offense | Offensive efficiency rank |
| def_rank | rank_defense | Defensive efficiency rank |
| tempo | raw_tempo | Actual tempo (possessions/game) |
| tempo_rank | rank_tempo | Tempo rank |
| rank_inj | rank_injury | Injury impact rank |
| home_rank | rank_home | Home court advantage rank |
| roster_rank | rank_roster | Roster talent rank |
| runs_per_game | obj_kills_per_game | "Kill shots" (runs) per game |
| runs_conceded_per_game | obj_kills_concede_per_game | Kill shots conceded per game |
| runs_total | obj_kills_total | Total kill shots in season |
| runs_conceded_total | obj_kills_conceded_total | Total kill shots conceded |
| wins | obj_wins | Wins |
| losses | obj_losses | Losses |

## Which fields are actually used by strategies?

Scanning `gamewinner/strategies/mathstats/derived/*.py`, these `MSProps` fields are referenced:

| Field | Used by |
|-------|---------|
| `rank_overall` | Vanilla, SlothfireSteady* |
| `rank_offense` | SlothfireSteady* |
| `rank_defense` | SlothfireSteady*, Chillz*, MrFreeze, DoctorLizard |
| `rank_tempo` | SlothfireSteady*, FireWater |
| `rank_roster` | SlothfireSteady*, TheCuts*, TheOwl |
| `rank_home` | SlothfireSteady*, TheCuts* |
| `raw_overall` (bpr) | TheCuts*, TheWhiteWhale |
| `raw_offense` (obpr) | Rocky |
| `raw_defense` (dbpr) | Rocky |
| `obj_kills_concede_per_game` | SlothfireSteady* |

The `adjust_opponent`, `adjust_pace`, `rank_injury`, `obj_kills_per_game`, `obj_kills_total`, `obj_kills_conceded_total` fields are loaded but not used by any current strategy. They should still be present for completeness.

## Data Source: Evan Miya

- **URL**: `https://evanmiya.com/?team_ratings`
- **Status**: May require a paid subscription. Check current access.
- **Historical pattern**: The site provides BPR (Bayesian Performance Rating) along with various rankings and game stats.

### Expected 2026 changes
The 2023→2024 transition already saw significant changes:
- Column headers were renamed (e.g., `Rank` → `rank`, `OBPR` → `obpr`)
- `ResumeRank` was removed
- `opponent_adjust`, `pace_adjust`, `wins`, `losses` were added
- Kill shot stats were renamed (e.g., `KillShotsPerGame` → `runs_per_game`)
For 2026, expect similar potential changes. The key task is mapping whatever Evan Miya provides into the 20-column format.

## Implementation Approach

### Step 1: Access the data

Visit `https://evanmiya.com/?team_ratings` and determine:
- Is data freely accessible, or is a subscription needed?
- What columns/stats are currently available?
- Is there an API endpoint or export feature?
- Can the table be scraped from the page HTML?

If a subscription is needed, flag this and obtain access before proceeding.
### Step 2: Map columns

Once you can see the 2026 data, create a mapping from the current Evan Miya columns to the 20-column format. For each column:
- **Direct match**: Same stat, maybe different name → just rename
- **Close equivalent**: Similar concept → use it with a note
- **Missing**: Not available → decide on a fallback (calculate from other data, use a placeholder, or set to 0/-1)
Document every mapping decision.

### Step 3: Build the CSV
Create `gamewinner/strategies/mathstats/data/2026.csv` with:
- All ~362 Division I teams (the file should include ALL teams, not just tournament teams)
- Exactly 20 columns in the correct order
- Team names that pass `get_definitive_name()` resolution

**Important**: The Evan Miya file includes ALL D1 teams (the 2024 file has 362 rows). This is because strategies use rank-based percentile calculations (`_rank_to_percentile`) that need the full ranking context. However, only tournament teams need to match exactly.

### Step 4: Resolve team names
Evan Miya uses its own team naming convention. For each team:
1. Try `get_definitive_name(evan_miya_name)` 
2. If it fails, check `alternate_names.py` for the canonical form
3. Add new aliases to `alternate_names.py` as needed
Pay special attention to teams like:
- "UConn" → "Connecticut"
- "McNeese" → "McNeese State" 
- "Miami (FL)" → "Miami (Fla.)"
- "Charleston" → "College of Charleston"

### Step 5: Validate

Run a quick smoke test:
```bash
poetry run play --strategy Vanilla --year 2026
poetry run play --strategy SlothfireSteady --year 2026
```
If any strategy crashes with a `KeyError` on a team name, it means that team is in the tournament bracket but not matched in the Evan Miya CSV. Fix the name mapping.

## Script (optional, for automation)

If building a fetch script (`scripts/fetch_evan_miya_data.py`), it should:
1. Fetch or load the raw Evan Miya data
2. Map columns to the 20-column format
3. Resolve team names
4. Output the CSV
5. Print a report of any unmapped columns or unresolved team names

Keep it simple. The 2023→2024 transition was done manually with good results.

## Fallback: Alternative Data Sources
If Evan Miya is inaccessible or too expensive:
- **KenPom** (`kenpom.com`) — similar advanced stats, may also require subscription
- **Bart Torvik** (`barttorvik.com`) — free alternative with comparable metrics
- **Manually approximate** — some stats (like BPR) may not have exact equivalents, but offensive/defensive efficiency ranks, tempo, and roster rankings can be sourced from multiple places

The strategies are fairly robust to the exact values — they mostly use **rank-based percentiles**, so as long as the relative ordering is reasonable, the strategies will produce sensible brackets.

## Files to create or modify

| File | Action |
|------|--------|
| `gamewinner/strategies/mathstats/data/2026.csv` | Create |
| `gamewinner/teams/alternate_names.py` | Modify — add new aliases |
| `gamewinner/strategies/mathstats/imathstats.py` | Possibly modify — only if column count/order changes (see Step 03) |
| `scripts/fetch_evan_miya_data.py` | Create (optional) |
## Next Step

After completing Evan Miya data refresh, proceed to **03-strategy-updates.md**.