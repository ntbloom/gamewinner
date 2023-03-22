from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class DoctorLizard(IEvanMiyaStrategy):
    """
    Straight from The Doc:

    > My strategy would probably be something like.....
    > if the difference in ranking (using the injuryrank) is greater than 25,
    >   pick higher rank. If not, subtract points allowed (DBPR) from points
    >   scored (OBPR) and select team with greater valueunless difference is
    >   less than 5.
    > If not greater than 5, pick team with more KillShotsPerGame.

    Note: "points allowed" and "points scored" aren't in this data set.
          We are interpretting The Doc to have meant overal point differntial
          which, while also not in the data set, is pretty similar to what's
          being captured by BPR. So that's what we're using.

          If and when The Doc reviews this, we will remove this note and
          adjust as necessary.
    """

    @property
    def name(self) -> str:
        return "DoctorLizard"

    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        """
        The Lizard Sauce
        """

        props1 = self.get_props(team1)
        props2 = self.get_props(team2)
        # "if the difference in ranking (using the injuryrank) is greater than 25..."
        if abs(props1.injury_rank - props2.injury_rank) > 25:
            # "pick higher rank"
            if props1.injury_rank < props2.injury_rank:
                return team1, team2
            else:
                return team2, team1

        # "If not, subtract points allowed from points scored and select team
        #    with greater value..."
        # (Using BPR for this, see note above)
        # "...unless difference is less than 5."
        elif abs(props1.bpr - props2.bpr) >= 5:
            if props1.bpr > props2.bpr:
                return team1, team2
            else:
                return team2, team1

        # "If not greater than 5, pick team with more KillShotsPerGame."
        else:
            if props1.kill_shots_per_game > props2.kill_shots_per_game:
                return team1, team2
            elif props2.kill_shots_per_game > props1.kill_shots_per_game:
                return team2, team1
            # Editorial: it is possible for the above to end in a tie,
            #   which won't work. If we get all the way to the bottom,
            #   we just go back to picking based on InjuryRank.
            else:
                if props1.injury_rank < props2.injury_rank:
                    return team1, team2
                else:
                    return team2, team1

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 75, 67
