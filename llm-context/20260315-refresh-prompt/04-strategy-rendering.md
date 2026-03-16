#  Step 04: Strategy Rendering and Reports

## Objective

Make it easy to:
1. Run a strategy and see a readable output (beyond the current printer)
2. Run all strategies and compare their picks side-by-side
3. Generate a "report" for posting (like the ones in GitHub issues #14, #9)

## Context: What exists today

The current system already works end-to-end:
```bash
poetry run play --strategy SlothfireSteady --year 2024 --printer basic
```

This runs the bracket and prints results via `BasicFilePrinter` (writes a text file to `generated/`). The `Bracket` object after `play()` has all the data we need:
- `bracket.first_round`, `bracket.second_round`, ..., `bracket.final_four`, `bracket.finals` — all sets of `Game` objects
- `bracket.winner` — the champion `Team`
- `bracket.strategy` — strategy name
- Each `Game` has `team1`, `team2`, `predicted_winner`, `stage`

The CLI uses Typer (not Click). The printer system uses an `IPrinter` interface.

## Approach: Work with the existing architecture

Rather than building a separate reporting framework, extend what exists:

### 1. New printer: `MarkdownReportPrinter`

Create a new printer class that generates a markdown report matching the GitHub issue format.

**File**: `gamewinner/printers/markdown_report_printer.py`

This printer would output something like:
```markdown
# SlothfireSteady — 2026 Bracket

## Champion: (1) Houston

## Final
(1) Houston 74, (1) Duke 67

## Final Four
- (1) Houston beats (2) Marquette
- (1) Duke beats (3) Baylor

## Elite Eight
...

## Notable Upsets
- (12) Grand Canyon over (5) San Diego State (Second Round)
- (10) Nevada over (7) Dayton (First Round)

## Seed Summary
- Average Final Four seed: 1.5
- Champion seed: 1
- Biggest upset: 12 over 5
```

The printer has access to the `Bracket` object, which contains all game results organized by round. It can compute upsets (lower seed beating higher seed), Final Four matchups, etc.

Register it in `gamewinner/printers/__init__.py`.

**Usage**: `poetry run play --strategy SlothfireSteady --year 2026 --printer markdown`

### 2. New CLI command or script: `run_all`

Create a way to run all strategies and produce a comparison.

**Option A**: New Typer command in `cli.py`:
```python
@app.command()
def run_all(
    year: int = typer.Option(this_year, help="year"),
    output_dir: str = typer.Option("generated/", help="output directory"),
) -> None:
    for strategy in available_strategies:
        bracket = Bracket(year)
        bracket.play(strategy)
        # collect results...
```

**Option B**: Simple standalone script `scripts/run_all_strategies.py` that imports and runs everything.

Either way, the output should be a comparison table:
```markdown
# 2026 Strategy Comparison

| Strategy | Champion | Final Four | Biggest Upset |
|----------|----------|------------|---------------|
| SlothfireSteady | (1) Houston | Houston, Duke, ... | (12) GCU over (5) SDSU |
| TheCuts23 | (2) Marquette | Marquette, ... | (11) NC State over (6) ... |
| ... | ... | ... | ... |
```

Note: Strategies with randomness will produce different results each run. For the comparison, either:
- Run random strategies multiple times and report the most common picks
- Or just run once and note that results vary
- Or use the `Frozen`/`Steadiest`/`Bayz` variants for stable comparisons

### 3. Report generation script

**File**: `scripts/generate_reports.py`

A script that:
1. Runs each deterministic strategy (or all strategies once)
2. Generates a markdown report for each
3. Generates a comparison summary
4. Saves everything to `generated/reports/2026/`

This is the "report" that can be posted to a GitHub issue.

## Implementation details

### Extracting data from Bracket

The `Bracket` object after `play()` has:
- `bracket.games` — set of all `Game` objects
- `bracket.first_round` through `bracket.finals` — games by round
- Each `Game` has: `team1: Team`, `team2: Team`, `predicted_winner: Team`, `stage: Stage`
- Each `Team` has: `name: str`, `region: GeographicRegion`, `rank: int`

An "upset" is when `predicted_winner.rank > other_team.rank` (higher seed number = lower rank).

### Identifying Final Four teams

The `bracket.final_four` set contains 2 `Game` objects (the two semifinal matchups). Each game's `team1` and `team2` are the regional champions. The `bracket.finals.team1` and `team2` are the finalists.

### Score prediction

The system calls `strategy.predict_score(winner, loser)` only for the championship game. Most strategies return random scores in a range. Some (like `SlothfireSteadiest`) return fixed scores.

## Files to create

| File | Purpose |
|------|---------|
| `gamewinner/printers/markdown_report_printer.py` | Markdown report printer |
| `gamewinner/printers/__init__.py` | Register new printer |
| `scripts/generate_reports.py` | Batch report generation |

## Files to modify

| File | Change |
|------|--------|
| `cli.py` | Optionally add `run-all` command |

## Scope control

Keep this simple. Don't add:
- PDF generation (markdown is fine, can be converted externally)
- HTML templating frameworks
- Chart/visualization libraries
- New dependencies unless truly needed

The existing `rich` library is already a dependency and can do formatted console output. Markdown files can be posted directly to GitHub issues.

## Next Step
After implementing strategy rendering, proceed to **05-tournament-tracking.md**.