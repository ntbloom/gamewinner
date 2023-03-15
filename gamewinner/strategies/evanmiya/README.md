# Evan Miya Strategy

This strategy adds Evan Miya data (from the "Team Ratings" section of [evanmiya.com](https://evanmiya.com/)) for use in `pick()` methods. Details on the available data, along with attribute names, is below under "Data Definitions".

# Defining a strategy

This library defines an `IEvanMiyaStrategy` class, which your strategy will inherit from. This class loads the data for use, and defines a default `pick()` method, which runs both teams through a `_team_metric()` method and picks the team with the highest resulting score. 

## Helper methods

### `_team_metric()`

The simplest path to designing a new strategy is to implement a custom `_team_metric()` algorithm and inherit the defaults for everything else. **See example strategies below** for syntax and inspiration.

### `_rank_to_percentile()`
Much of the Evan Miya data is in the form of ranks, with the best team for the relevant category having a rank of 1 and worst being ranked 335(?). However, ranks can be obnoxious to do math with. The [`_rank_to_percentile()`](https://github.com/ntbloom/gamewinner/blob/a26d1f2/gamewinner/strategies/evanmiya/ievanmiya.py#L115-L119) method translates these ranks to percentiles: rank 1 becomes `1.0`, rank 2 becomes `0.998...`, etc. and all ranks below 250 become `0.0`. You can also use the `reverse` argument, for example if you want team with a _lower_ `evanmiyaHomeRank` to get a bonus. Several of the examples below use this method.

## Example strategies

* [VanillaMiya](https://github.com/ntbloom/gamewinner/blob/main/gamewinner/strategies/evanmiya/vanilla_miya.py) is the simplest option. The team with the highest `evanmiyaRank` always wins.
* [SlothfireSteady](https://github.com/ntbloom/gamewinner/blob/main/gamewinner/strategies/evanmiya/slothfire_steady.py) uses `evanmiyaDefRank` and `evanmiyaTempoRank` to give preference to teams that control the tempo and flow of the game.
* [TheCuts23](https://github.com/ntbloom/gamewinner/blob/main/gamewinner/strategies/evanmiya/the_cuts.py) prioritizes `evanmiyaBPR`, with some extra points for resume and being good on the road.
* [MrFreeze](https://github.com/ntbloom/gamewinner/blob/main/gamewinner/strategies/evanmiya/mr_freeze.py) is a somewhat abstract strategy, inspired by the films of Mr Arnold S.

# Data Definitions

- `evanmiyaRank` - Evan Miya Rank: Overal rank, based on Evan Miya statistics
- `evanmiyaOBPR` - OBPR: Team Offensive Bayesian Performance Rating reflects a
  team's expected offensive efficiency. This is interpreted as the points per
  100 possessions better than average expected when playing against an average
  D1 team. A higher rating is better.
- `evanmiyaDBPR` - DBPR: Team Defensive Bayesian Performance Rating reflects a
  team's expected defensive efficiency. This is interpreted as the defensive
  points per 100 possessions better (lower) than average when playing against an
  average D1 team. A higher rating is better.
- `evanmiyaBPR` - BPR: Bayesian Performance Rating is the sum of a team's OBPR
  and DBPR. This rating is the ultimate measure of a team's expected overall
  strength. This is interpreted as the number of points the team is expected to
  outscore an average D1 team by in an 100 possession game. A higher rating is
  better.
- `evanmiyaOffRank` - Off Rank: A team's rank in OBPR.
- `evanmiyaDefRank` - Def Rank: A team's rank in DBPR.
- `evanmiyaTrueTempo` - True Tempo: A measure of a team's true game pace. This
  number reflects the estimated number of possessions played in a game against
  an average paced D1 opponent.
- `evanmiyaTempoRank` - Tempo Rank: A team's rank in True Tempo
- `evanmiyaInjuryRank` - Injury Rank: A team's overall ranking after accounting
  for the absence of all currently injured players.
- `evanmiyaRosterRank` - Roster Rank: A crude ranking of each team's strength of
  roster. This is largely based on the individual BPR values of all players on
  the roster.
- `evanmiyaKillShotsPerGame` - Kill Shots Per Game: The number of double digit
  scoring runs per game (10 points or more scored in a row without the opposing
  team scoring).
- `evanmiyaKillShotsAllowedPerGame` - Kill Shots Allowed Per Game: The number of
  double digit scoring runs conceded per game (10 points or more scored in a row
  by the opponent without the team scoring).
- `evanmiyaTotalKillShots` - Total Kill Shots: The total number of double digit
  scoring runs in the season.
- `evanmiyaTotalKillShotsAllowed` - Total Kill Shots Allowed: The total number
  of double digit scoring runs conceded in the season.
- `evanmiyaResumeRank` - Resume Rank: A ranking of each team's in-season resume,
  treating all teams as equal at the start of the season. Think of it as a
  better version of the NET.
- `evanmiyaHomeRank` - Home Rank: A team's rank in how much better they perform
  at home versus road games. A team ranked higher will play much better at home
  than on the road.

**BPR Interpretation Example:**

> If Kansas had an Offensive BPR of 18, a Defensive BPR of 12, and a BPR of 30,
> this would mean the following: If Kansas was facing an average D1 team, they
> would be expected score 18 more points per 100 possessions than an average
> team would (the average points per 100 in the past has been around 104), and
> they would be expected to allow 12 less points per 100 possessions than an
> average team would. Overall, they would be expected to outscore a D1 average
> team by 30 points in a 100 possession game (games are often roughly around 70
> possessions).
