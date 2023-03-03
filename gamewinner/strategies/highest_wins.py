from gamewinner import Strategy, Team


class HighestWins(Strategy):
    def pick(self, team1: Team, team2: Team) -> Team:
        assert team1.rank_nat != team2.rank_nat
        diff = team1.rank_reg - team2.rank_reg
        if diff > 0:
            return team2
        if diff < 0:
            return team1
        if diff == 0:
            if team1.rank_nat > team2.rank_nat:
                return team1
            return team2
        raise ValueError(f"impossible outcome: {team1=}, {team2=}")

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 81, 67
