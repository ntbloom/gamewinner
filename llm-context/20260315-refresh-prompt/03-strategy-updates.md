# Step 03: Strategy and Parser Updates for 2026 Data

## Objective

Make all existing strategies work with the 2026 data created in Steps 01 and 02. This may involve:
1. Updating `imathstats.py` if the Evan Miya column count/order changed
2. Adding new team name aliases
3. Fixing any other breakage

**If Steps 01 and 02 produced data files that exactly match the 2024 format, this step may require zero code changes.** The goal of Step 02 was to produce a 20-column CSV matching the 2024 layout. If that succeeded, all strategies should already work.

## When changes ARE needed

### Scenario A: Evan Miya changed columns

If the 2026 Evan Miya data has different columns (new stats added, old stats removed, or reordered), then `imathstats.py` needs updating.

The key code to modify is the `prepare()` method's tuple unpacking:

```python
# In gamewinner/strategies/mathstats/imathstats.py, inside prepare():
for row in reader:
    (
        rank_overall,
        name,
        raw_offense,
        raw_defense,
        raw_overall,
        adjust_opponent,
        adjust_pace,
        rank_offense,
        rank_defense,
        raw_tempo,
        rank_tempo,
        rank_injury,
        rank_home,
        rank_roster,
        obj_kills_per_game,
        obj_kills_concede_per_game,
        obj_kills_total,
        obj_kills_conceded_total,
        obj_wins,
        obj_losses,
    ) = row
```

If columns were added/removed:
1. Update the tuple unpacking to match the new column order
2. Update the `MSProps` NamedTuple if fields are added or removed
3. If a field used by strategies was removed, you must either:
   - Calculate it from other available data
   - Set a reasonable default value
   - Update the strategies that use it

**If a field was added** that you want to expose to strategies:
1. Add it to `MSProps`
2. Include it in the `MSProps(...)` constructor call
3. Existing strategies won't break — they just won't use the new field

**If a field was removed** that strategies depend on:
- Check which strategies use it (see the table in `02-data-refresh-evan-miya.md`)
- Decide: can it be approximated? Should the strategy be updated? Or use a dummy value?
- Fields with `resume_rank` precedent: the field was kept in `MSProps` with `default=-1` when it was removed in 2024

### Scenario B: Backward compatibility with 2023/2024

The current `prepare()` method loads `{year}.csv` based on the `year` argument. **There is only one parser, so any changes must also work with 2023 and 2024 data.**

Options if column count changed:
1. **Best option**: Make the 2026 CSV match the 2024 format (20 columns, same order). Then no parser changes needed.
2. **If unavoidable**: Add a version check:
   ```python
   if year >= 2026:
       # new unpacking
   else:
       # existing unpacking
   ```
   Or better yet, detect column count from the header row.
3. **Consider**: Switching to `csv.DictReader` so column order doesn't matter. This is a larger refactor but would make future years easier. Weigh the risk vs. benefit.

### Scenario C: New team names

If any team in the 2026 tournament is not in `alternate_names.py`, the system will crash with:
```
ValueError: Can't find definitive name for `some team`
```

Fix: Add the team to `alternate_names.py` with its canonical name and any aliases.

Likely candidates for 2026:
- New programs that joined D1 recently
- Teams that changed names or conferences
- Teams with non-standard name formatting

Also check Evan Miya's naming — if it uses names not in the alias list, add those aliases.

## Verification

Run every strategy against 2026:

```bash
# Quick test with non-random strategies
poetry run play --strategy Vanilla --year 2026
poetry run play --strategy SlothfireSteadiest --year 2026
poetry run play --strategy TheCuts23Frozen --year 2026
poetry run play --strategy BestRankWins --year 2026

# Full test with all strategies
for strategy in BestRankWins Chillz DoctorLizard FireWaterFireWater KillerChillz MrFreeze Rocky SlothfireSteady SlothfireSteadiest SlothfireSteadyBayz TheCuts23 TheCuts23DumBayz TheCuts23Frozen TheOwl TheWhiteWhale Vanilla WorstRankWins; do
    echo "Testing $strategy..."
    poetry run play --strategy "$strategy" --year 2026
done
```

Also verify backward compatibility:
```bash
poetry run play --strategy Vanilla --year 2024
poetry run play --strategy Vanilla --year 2023
```

## Files potentially modified

| File | When |
|------|------|
| `gamewinner/strategies/mathstats/imathstats.py` | Only if column format changed |
| `gamewinner/teams/alternate_names.py` | If new teams or Evan Miya uses new name variants |
| `gamewinner/strategies/mathstats/derived/*.py` | Only if MSProps fields were removed that strategies use |
| `gamewinner/bracket/geographic_region.py` | Only if 2026 uses different region names |

## Next Step
After verifying all strategies work, proceed to **04-strategy-rendering.md**.