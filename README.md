# gamewinner

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

March madness predictor. Bring your own game winning prediction algorithm and
hope for the best library and get a bracket printed out with the winners, along
with a score for the final game.

## How it works

### Data Model

Only data included in the official NCAA bracket will be provided. The following
data points are included:

- team name
- region
- bracket rank
- wins
- losses

Additional data such as national rankings or seasonal statistics are not
included as part of the main library, but should be implemented as part of a
concrete strategy.

Teams in the first four have their region marked as `<REGION>-Playoff` along
with the regional rank they're competing for.

For example, this is a sample of the 2022 bracket data used as test data:

```csv
Team Name,Region,Regional Rank,Wins,Losses
Rutgers,West-Playoff,11,18,13
Notre Dame,West-Playoff,11,22,10
Texas Southern,Midwest-Playoff,16,18,12
Texas A&M CC,Midwest-Playoff,16,23,11
Wright St.,South-Playoff,16,21,13
Bryant,South-Playoff,16,22,9
Wyoming,East-Playoff,12,25,8
Indiana,East-Playoff,12,20,13
Gonzaga,West,1,26,3
Georgia St.,West,16,18,10
Boise St.,West,8,27,7
Memphis,West,9,21,10
Uconn,West,5,23,9
New Mexico St.,West,12,26,6
Arkansas,West,4,25,8
Vermont,West,13,28,5
Alabama,West,6,19,3
Texas Tech,West,3,25,9
...
```

### Define a Strategy

Implement a class that inherits from the `IStrategy` interface defined in
[istrategy.py](https://github.com/ntbloom/gamewinner/blob/main/gamewinner/strategies/istrategy.py).
Example strategies can be found in
[gamewinner/strategies/](https://github.com/ntbloom/gamewinner/blob/main/gamewinner/strategies/)
(i.e. the classic
[BestRankWins](https://github.com/ntbloom/gamewinner/blob/main/gamewinner/strategies/best_rank_wins.py)).

The class has 4 main methods:

### `prepare(teams: dict[str,Team]) -> None`

- gets called after the teams are loaded into the bracket but before any games
  (including first four) are played
- used to do any external data fetching, rank teams, etc.
- defaults to no-op if you don't override the method

### `adjust(teams: dict[str,Team]) -> None`

- gets called before each round, including the first four
- adjust your strategy to accomodate "Cinderella factor" or how to recover after
  an upset
- defaults to no-op if you don't override the method

### `pick(team1: Team, team2: Team) -> tuple[Team, Team]`

- pick a winner using whatever method you think will make you the gamewinner
- the whole point of the library

### `predict_score(winner: Team, loser: Team) -> tuple[int, int]`

- predict the score of a game, generally reserved for the final game

## Run the model

Once you've got your strategy figured out, printing a sample bracket is trivial.

### Python

Dependencies:
* python 3.10 or later
* poetry

```shell
$ python -m pip install poetry
$ poetry install
```

From there, invoke the cli:

```shell
poetry run play --help
#                                                                                                                              
# Usage: play [OPTIONS]                                                                                                      
#                                                                                                                              
#╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
#│ *  --strategy        TEXT     strategy you want to use [default: None] [required]                                          │
#│    --year            INTEGER  year you want to use [default: 2023]                                                         │
#│    --printer         TEXT     printer to use [default: colortext]                                                          │
#│    --help                     Show this message and exit.                                                                  │
#╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
#
```

### Docker

Dependencies:
* make
* docker with compose plugin

No python toolchain is needed here. Simply run `make docker` and generate 
brackets for every strategy.  Files will be created in the `generated/`
directory.

```shell
$ make docker
# ...
$ ls generated/
# BestRankWins-2024-basic.txt        Rocky-2024-basic.txt                TheCuts23Frozen-2024-basic.txt
# Chillz-2024-basic.txt              SlothfireSteadiest-2024-basic.txt   TheOwl-2024-basic.txt
# DoctorLizard-2024-basic.txt        SlothfireSteady-2024-basic.txt      TheWhiteWhale-2024-basic.txt
# FireWaterFireWater-2024-basic.txt  SlothfireSteadyBayz-2024-basic.txt  Vanilla-2024-basic.txt
# KillerChillz-2024-basic.txt        TheCuts23-2024-basic.txt            WorstRankWins-2024-basic.txt
# MrFreeze-2024-basic.txt            TheCuts23DumBayz-2024-basic.txt

```

That's it. Good luck!

Special thanks to [Vulfpeck](https://youtu.be/j3rwKl267gEh) for the name
inspiration.
