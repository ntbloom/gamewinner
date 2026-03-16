# Step 07: Interactive Strategy Builder (Optional)

## Objective

Provide an interactive way for users to build strategies without editing YAML or Python files directly. This is a nice-to-have stretch goal.

## Context

Step 06 created a YAML-based strategy definition format and a script to generate Python code from it. This step adds an interactive layer on top.

## Recommended approach: TUI with `textual`

The `textual` library (from the same author as `rich`, which is already a dependency) provides a terminal-based UI framework. This fits the project's CLI-oriented workflow better than a web app.

### What the TUI would do

1. **Prompt for strategy metadata**: name, description
2. **Show available MSProps fields** with descriptions
3. **Let user add scoring components**: pick a stat, set weight, toggle reverse
4. **Let user add adjustments**: pick a stat, choose add/subtract
5. **Configure upset factor**: enable/disable, add components with weights
6. **Preview**: show the generated YAML and Python code
7. **Save**: write the YAML and/or Python file, optionally register the strategy

### Why TUI over Web

- No new server infrastructure
- No JavaScript/HTML/CSS to maintain
- Works over SSH
- Consistent with the existing `poetry run play` workflow
- `textual` is a single pip install with no system dependencies

### Simpler alternative: guided CLI prompts

If a full TUI is too much, a simple interactive script using `typer.prompt()` or `questionary` would work:

```bash
$ python scripts/build_strategy_interactive.py

Strategy name: MyNewStrategy
Description: A balanced approach to bracket picking

Available stats: rank_overall, rank_offense, rank_defense, rank_tempo, ...

Add scoring component? [y/n]: y
  Stat: rank_defense
  Weight [1.0]: 1.0
  Reverse percentile? [y/n]: n

Add scoring component? [y/n]: y
  Stat: rank_offense
  Weight [1.0]: 0.5
  Reverse percentile? [y/n]: n

Add scoring component? [y/n]: n

Add raw stat adjustment? [y/n]: n

Enable upset factor? [y/n]: y
  Add upset component:
    Stat: rank_roster
    Weight [1.0]: 1.0
  Add another? [y/n]: n

Fixed score prediction? [y/n]: y
  Winner score: 74
  Loser score: 66

--- Preview ---
[shows generated YAML]
[shows generated Python]

Save? [y/n]: y
Register in __init__.py? [y/n]: y

Done! Run with: poetry run play --strategy MyNewStrategy --year 2026
```

This is probably the right level of effort for the project's needs.

## Implementation

- Depends on Step 06 being complete (the YAML format and code generator)
- The interactive layer is just a UI that collects inputs and calls the same generator
- Keep it as a single script file

## Files to create

| File | Purpose |
|------|---------|
| `scripts/build_strategy_interactive.py` | Interactive strategy builder |

## Dependencies

- `questionary` or just `typer.prompt()` (already available) for the simple version
- `textual` for the TUI version (optional)

## This step is truly optional

The YAML format from Step 06 is already human-friendly enough. Most users comfortable with a bracket prediction system can edit YAML. The interactive builder is a convenience, not a necessity.
