# Step 06: YAML-Based Strategy Builder

## Objective

Create a system where a user defines a strategy in YAML, and a tool generates the corresponding Python file (an `IMathStatsStrategy` subclass). This makes it easy for non-programmers to build bracket strategies by declaring weights on statistical components.

## What existing strategies actually look like

Every mathstats strategy follows the same pattern:

```python
class MyStrategy(IMathStatsStrategy):
    @property
    def name(self) -> str:
        return "MyStrategy"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)  # returns MSProps NamedTuple
        score = <some weighted combination of props fields>
        score += <optional randomness factor>
        return score
```

The `_team_metric()` function returns a float. Higher = better team. The base class `pick()` method calls this for both teams and picks the higher one.

### Available MSProps fields

These are the fields strategies can use (all from Evan Miya data):
- `rank_overall`, `rank_offense`, `rank_defense`, `rank_tempo`, `rank_injury`, `rank_home`, `rank_roster` — integer ranks (1 = best)
- `raw_overall`, `raw_offense`, `raw_defense`, `raw_tempo` — float ratings
- `adjust_opponent`, `adjust_pace` — float adjustments
- `obj_kills_per_game`, `obj_kills_concede_per_game` — float
- `obj_kills_total`, `obj_kills_conceded_total` — int
- `obj_wins`, `obj_losses` — int

### Common patterns

1. **Rank-to-percentile conversion**: `self._rank_to_percentile(rank)` converts rank to 0–1 (1 = rank #1). `reverse=True` flips it.
2. **Weighted sum**: Most strategies are `w1 * percentile(stat1) + w2 * percentile(stat2) + ...`
3. **Random upset factor**: `random.random() * some_component` adds variability
4. **DumBayz**: `self._dumbayz(lambda: <expr>, numdraws=N)` runs expression N times and takes median

## YAML format design

Keep it close to how existing strategies actually work. Here's a proposed format:

```yaml
name: DefenseSloth
description: "Defense-heavy sloth strategy with upset factor"

# Main scoring formula: weighted sum of percentile-converted ranks
# score = sum of (weight * percentile(stat, reverse?))
components:
  - stat: rank_defense
    weight: 1.0
  - stat: rank_tempo
    weight: 0.5
    reverse: true        # lower tempo = higher score
  - stat: rank_offense
    weight: 0.3
  - stat: rank_overall
    weight: 0.3

# Raw stat adjustments (added/subtracted directly, not percentile-converted)
adjustments:
  - stat: obj_kills_concede_per_game
    operation: subtract   # score -= value

# Upset/randomness factor: random.random() * sum of (weight * percentile(stat))
# Set to null or omit to disable
upset_factor:
  components:
    - stat: rank_roster
      weight: 1.0
    - stat: rank_home
      weight: 1.0
      reverse: true
      cap: 0.5            # min(percentile_value, cap)

# Optional: fixed score prediction for championship game
score_prediction:
  winner: 76
  loser: 67

# Optional: use DumBayz (median of N random runs) instead of single random run
# If set, the upset_factor uses dumbayz instead of a single random.random()
# dumbayz_draws: 100
```

This maps directly to the code patterns:

```python
def _team_metric(self, team):
    props = self.get_props(team)
    score = (
        1.0 * self._rank_to_percentile(props.rank_defense)
        + 0.5 * self._rank_to_percentile(props.rank_tempo, reverse=True)
        + 0.3 * self._rank_to_percentile(props.rank_offense)
        + 0.3 * self._rank_to_percentile(props.rank_overall)
        - props.obj_kills_concede_per_game
    )
    score += random.random() * (
        1.0 * self._rank_to_percentile(props.rank_roster)
        + min(1.0 * self._rank_to_percentile(props.rank_home, reverse=True), 0.5)
    )
    return score
```

## Implementation

### Code generator: `scripts/build_strategy.py`

A simple Python script that:
1. Reads a YAML file
2. Validates all `stat` fields are valid `MSProps` fields
3. Generates a `.py` file with the strategy class
4. Optionally registers it in `gamewinner/strategies/__init__.py`

The generated Python code should be **readable and editable** — someone should be able to tweak it by hand afterward. Don't use complex metaprogramming. Just emit straightforward Python.

**Usage**:
```bash
python scripts/build_strategy.py strategies/my_strategy.yaml
# → generates gamewinner/strategies/mathstats/derived/defense_sloth.py
# → optionally adds import + registration to __init__.py
```

### Validation

The builder should check:
- All `stat` values are valid `MSProps` field names
- `weight` values are numbers
- `operation` is one of `add`, `subtract`
- If `cap` is set, it's a number
- `name` is a valid Python class name

### Registration

To register a new strategy, the builder needs to:
1. Add an import line to `gamewinner/strategies/__init__.py`
2. Add the class to the `available_strategies` tuple

This can be done with simple string manipulation of `__init__.py`. The existing file follows a very regular pattern.

## Example: recreating SlothfireSteady from YAML

As a sanity check, this YAML should generate code equivalent to the existing `SlothfireSteady`:

```yaml
name: SlothfireSteadyYAML
description: "YAML-generated version of SlothfireSteady"

components:
  - stat: rank_defense
    weight: 1.0
  - stat: rank_tempo
    weight: 0.5
    reverse: true
  - stat: rank_offense
    weight: 0.3
  - stat: rank_overall
    weight: 0.3

adjustments:
  - stat: obj_kills_concede_per_game
    operation: subtract

upset_factor:
  components:
    - stat: rank_roster
      weight: 1.0
    - stat: rank_home
      weight: 1.0
      reverse: true
      cap: 0.5
```

## Scope control

- **Do**: Simple weighted-sum strategies with optional randomness
- **Don't**: Conditional logic ("if team is from East region..."), opponent-aware picks, ML models
- **Don't**: Jinja2 or complex templating — use Python string formatting or `textwrap.dedent`
- **Don't**: Need a web framework, database, or new dependencies

The goal is a single-file script that reads YAML and writes Python. Keep it under 200 lines.

## Files to create

| File | Purpose |
|------|---------|
| `scripts/build_strategy.py` | YAML → Python strategy generator |
| `strategies/*.yaml` | Directory for YAML strategy definitions |
| Example YAML files | 2–3 examples to demonstrate the format |

## Next Step
After implementing the YAML strategy builder, proceed to **07-strategy-builder-interactive.md**.