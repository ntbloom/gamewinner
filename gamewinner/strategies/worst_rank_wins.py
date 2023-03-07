from gamewinner.strategies.istrategy import IStrategy
from gamewinner.team import Team


class WorstRankWins(IStrategy):
    """
    The team with the highest regional rank wins.  In case of a tie, whoever
    has a higher national rank wins.
    """

    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        assert team1.rank_nat != team2.rank_nat
        if team1.rank_reg == team2.rank_reg:
            if team1.rank_nat > team2.rank_nat:
                return team1, team2
            else:
                return team2, team1

        if team1.rank_reg > team2.rank_reg:
            return team1, team2
        else:
            return team2, team1

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 81, 67
