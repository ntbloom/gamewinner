from __future__ import annotations

from gamewinner.bracket.team import Team
from gamewinner.strategies.evanmiya.ievanmiya import EMProps, IEvanMiyaStrategy


class TheWhiteWhale(IEvanMiyaStrategy):
    """
    Witness the white bear of the poles, and the white shark of the tropics;
    what but their smooth, flaky whiteness makes them the transcendent horrors
    they are?
    """

    @property
    def name(self) -> str:
        return "TheWhiteWhale"

    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        props1 = self.get_props(team1)
        props2 = self.get_props(team2)

        fave: EMProps
        underdog: EMProps
        fave, underdog = (
            (props1, props2) if props1.rank < props2.rank else (props2, props1)
        )
        upset = False

        # can an underdog with good defense stifle a better team?
        tempo_winner, tempo_loser = (
            (fave, underdog)
            if fave.tempo_rank < underdog.tempo_rank
            else (underdog, fave)
        )
        defense_holds = True if (tempo_winner.obpr < tempo_loser.dbpr) else False
        if defense_holds and tempo_winner == self:
            upset = True

        if upset:
            result = underdog == props1
        else:
            result = fave == props1
        return (team1, team2) if result else (team2, team1)
