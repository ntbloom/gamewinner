from gamewinner.strategies.istrategy import IStrategy
from gamewinner.teams.team import Team


class BestRankWins(IStrategy):
    """
    The team with the lowest regional rank wins.  In case of a tie, go with alphabetical
    """

    @property
    def name(self) -> str:
        return "BestRankWins"

    def pick(self, team1: Team, team2: Team) -> Team:
        if team1.rank != team2.rank:
            return team1 if team1.rank < team2.rank else team2

        teams = [team1, team2]
        teams.sort(key=str)
        return teams[0]

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 81, 67
