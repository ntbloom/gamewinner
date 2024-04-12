from __future__ import annotations

from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy
from gamewinner.teams.team import Team


class Rocky(IMathStatsStrategy):
    @property
    def name(self) -> str:
        return "Rocky"

    def pick(self, team1: Team, team2: Team) -> Team:

        props1 = self.get_props(team1)
        props2 = self.get_props(team2)
        score1 = props1.raw_overall
        score2 = props2.raw_overall

        # can you make it 15 rounds?
        injury_weight = 10
        if props1.rank_injury < props2.rank_injury:
            score1 += injury_weight
        else:
            score2 += injury_weight

        # how big is your heart?
        roster_weight = 25
        if props1.rank_roster > props2.rank_roster:
            score1 += roster_weight
        else:
            score2 += roster_weight

        # can you beat Carl Weathers in a footrace?
        tempo_weight = 25
        if props1.raw_tempo > props2.raw_tempo:
            score1 += tempo_weight
        else:
            score2 += tempo_weight

        # only a knockout counts
        kill_weight = 100
        if props1.obj_kills_per_game > props2.obj_kills_per_game:
            score1 += kill_weight
        else:
            score2 += kill_weight

        if score1 > score2:
            return team1
        else:
            return team2
