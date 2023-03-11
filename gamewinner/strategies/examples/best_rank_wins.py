from gamewinner.strategies.istrategy import IStrategy
from gamewinner.team import Team


class BestRankWins(IStrategy):
    """
    The team with the lowest regional rank wins.  In case of a tie, whoever
    has a lower national rank wins.
    """

    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        if team1.rank == team2.rank:
            if team1.win_rate == team2.win_rate:
                if team1.wins == team2.wins:
                    # when in doubt pick the first team
                    return team1, team2
                else:
                    if team1.wins > team2.wins:
                        return team1, team2
                    else:
                        return team2, team1
            else:
                if team1.win_rate > team2.win_rate:
                    return team1, team2
                else:
                    return team2, team1
        else:
            if team1.rank < team2.rank:
                return team1, team2
            else:
                return team2, team1

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 81, 67
