from gamewinner.strategies.istrategy import IStrategy
from gamewinner.team import Team


class WorstRankWins(IStrategy):
    """
    The team with the highest regional rank wins.  In case of a tie, whoever
    has a higher national rank wins.
    """

    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        if team1.rank == team2.rank:
            if team1.win_rate == team2.win_rate:
                if team1.wins == team2.wins:
                    if team1.losses == team2.losses:
                        # when in doubt pick the second team
                        return team2, team1
                    else:
                        if team1.losses > team2.losses:
                            return team1, team2
                        else:
                            return team2, team1
                else:
                    if team1.wins < team2.wins:
                        return team1, team2
                    else:
                        return team2, team1
            else:
                if team1.win_rate < team2.win_rate:
                    return team1, team2
                else:
                    return team2, team1
        else:
            if team1.rank > team2.rank:
                return team1, team2
            else:
                return team2, team1

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 81, 67
