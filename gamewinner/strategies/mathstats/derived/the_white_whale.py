from __future__ import annotations

from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy, MSProps
from gamewinner.teams.team import Team


class TheWhiteWhale(IMathStatsStrategy):
    """
    Witness the white bear of the poles, and the white shark of the tropics;
    what but their smooth, flaky whiteness makes them the transcendent horrors
    they are?
    """

    @property
    def name(self) -> str:
        return "TheWhiteWhale"

    def pick(self, team1: Team, team2: Team) -> Team:
        props1 = self.get_props(team1)
        props2 = self.get_props(team2)

        fave: MSProps
        underdog: MSProps
        fave, underdog = (
            (props1, props2)
            if props1.rank_overall < props2.rank_overall
            else (props2, props1)
        )
        upset = False

        # can an underdog with good defense stifle a better team?
        tempo_winner, tempo_loser = (
            (fave, underdog)
            if fave.rank_tempo < underdog.rank_tempo
            else (underdog, fave)
        )
        defense_holds = (
            True if (tempo_winner.raw_offense < tempo_loser.raw_defense) else False
        )
        if defense_holds and tempo_winner == self:
            upset = True

        if upset:
            result = underdog == props1
        else:
            result = fave == props1
        return team1 if result else team2
