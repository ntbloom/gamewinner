from gamewinner.strategies.istrategy import IStrategy
from gamewinner.teams.team import Team


class WorstRankWins(IStrategy):
    """
    The team with the highest regional rank wins.  In case of a tie, whoever
    has a higher national rank wins.
    """

    @property
    def name(self) -> str:
        return "WorstRankWins"

    def pick(self, team1: Team, team2: Team) -> Team:
        # pragma: no cover
        if team1.rank != team2.rank:
            return team1 if team1.rank > team2.rank else team2

        # all other things being equal, pick the second team
        return team2

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 81, 67
