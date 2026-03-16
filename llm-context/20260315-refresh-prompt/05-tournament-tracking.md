# Step 05: Tournament Tracking and Standings

## Objective

During the tournament, track actual game results and score each strategy's bracket against reality. Produce standings like those in GitHub issue #19. Optionally compare against human brackets from ESPN/Yahoo.

## How the system works today

When you run a strategy, the `Bracket` object records every predicted game as a `Game(team1, team2, predicted_winner, stage)`. The full bracket of predictions is the output.

To score a bracket, we need to compare these predictions against actual results. The existing codebase has **no** results-tracking infrastructure — this is entirely new.

## Design: Keep it simple

The core need is:
1. A way to record actual tournament results
2. A scorer that compares predictions vs. results
3. A script to produce standings

### Actual results: a simple data file

**File**: `data/results/2026.yaml` (or `.json`)

A manually-maintained (or script-updated) file recording game outcomes:

```yaml
# data/results/2026.yaml
year: 2026
games:
  # First Round
  - round: FirstRound
    winner: Connecticut
    loser: Stetson
  - round: FirstRound
    winner: Iowa State
    loser: South Dakota State
  # ... as games are played
  
  # Second Round
  - round: SecondRound
    winner: Connecticut
    loser: Northwestern
  # ...
```

Team names must be canonical (same as everywhere else). The `round` field should use `Stage` enum values: `FirstRound`, `SecondRound`, `SweetSixteen`, `EliteEight`, `FinalFour`, `Finals`.

This file gets updated each day as games are completed. It can be updated manually (simplest) or via script (nicer).

### Scoring a bracket

**File**: `gamewinner/scoring.py` (or `scripts/score_brackets.py`)

Standard bracket scoring:

| Round | Points per correct pick |
|-------|------------------------|
| First Round | 10 |
| Second Round | 20 |
| Sweet Sixteen | 40 |
| Elite Eight | 80 |
| Final Four | 160 |
| Championship | 320 |

(These are the ESPN standard point values. Adjust as desired.)

The scorer:
1. Runs each strategy to generate its bracket predictions (deterministic strategies are stable; random ones can be run with a fixed seed or multiple times)
2. Loads the results file
3. For each actual game result, checks if the strategy predicted that winner advancing in that round
4. Tallies points

**Key detail**: A bracket prediction isn't just "who wins each game" — it's "who reaches each round." If Strategy X picks Duke to reach the Elite Eight, but Duke loses in the Sweet Sixteen, the strategy gets no points for the Elite Eight game (even if the team that beat Duke is also someone the strategy picked elsewhere). This is standard bracket scoring: you only get points for a correct pick in the specific game slot.

The simplest implementation:
- For each completed game in results, identify the corresponding game in the bracket tree (same round, same matchup slot)
- Check if the strategy's predicted winner matches the actual winner
- Award points based on round

Since the bracket is a binary tree, each game slot is deterministic. The `Bracket` object already organizes games by round.

### Standings output

```markdown
# 2026 Tournament Standings — Through Sweet Sixteen

| Rank | Strategy | Score | Correct | Max Possible | Champion Pick |
|------|----------|-------|---------|--------------|---------------|
| 1 | SlothfireSteadiest | 290 | 24/48 | 770 | Houston ✅ |
| 2 | TheCuts23Frozen | 270 | 22/48 | 690 | Duke ❌ |
| 3 | Vanilla | 260 | 23/48 | 610 | Connecticut ✅ |
| ... | ... | ... | ... | ... | ... |
```

### Handling randomness

Strategies with randomness produce different brackets each run. Options:
- **Lock brackets before tournament starts**: Run each strategy once, save the bracket (as JSON/YAML), and score against those locked picks. This is the fairest approach.
- **Use deterministic variants**: `SlothfireSteadiest` instead of `SlothfireSteady`, `TheCuts23Frozen` instead of `TheCuts23`, etc.
- **Run multiple times, take consensus**: More complex, probably not worth it.

Recommend: Before the tournament starts, run each strategy (including random ones) and save the brackets to `generated/brackets/2026/`. Score against those saved brackets.

### Fetching results automatically (optional)

The ESPN scoreboard API is undocumented but well-known:
```
https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?dates=20260319&groups=100
```

(`groups=100` filters to tournament games.)

A script could fetch completed games and update the results YAML. This is nice-to-have but the results file can also be updated manually.

### CI automation (optional)

A GitHub Actions workflow that:
1. Runs daily during the tournament (`schedule: cron: '0 13 * 3 *'`)
2. Fetches latest results (or expects a manually-pushed results file)
3. Runs the scoring script
4. Commits updated standings to the repo (or creates/updates an issue)

## Comparing against external brackets

For ESPN/Yahoo group comparison:
- The simplest approach: manually enter scores from the ESPN/Yahoo group leaderboard into a CSV
- A fancier approach: scrape the ESPN bracket group standings

ESPN and Yahoo bracket scoring varies by pool settings, so ensure you're comparing with the same point values.

This is a nice-to-have and can be as simple as adding a row to the standings table.

## Files to create

| File | Purpose |
|------|---------|
| `data/results/2026.yaml` | Actual game results (updated throughout tournament) |
| `scripts/score_brackets.py` | Score each strategy's bracket against results |
| `scripts/lock_brackets.py` | Run all strategies and save bracket predictions |
| `scripts/fetch_results.py` | Optional: fetch results from ESPN API |
| `.github/workflows/tournament_tracking.yml` | Optional: daily CI job |

## Next Step
After implementing tournament tracking, proceed to **06-strategy-builder-yaml.md**.