from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class DoctorLizard(IEvanMiyaStrategy):
    """
    Straight from The Doc:
    
    > My strategy would probably be something like..... 
    > if the difference in ranking (using the injuryrank) is greater than 25, pick higher rank. 
    > If not, subtract points allowed (DBPR) from points scored (OBPR) and select team with greater value 
    >   unless difference is less than 5.
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

        # "if the difference in ranking (using the injuryrank) is greater than 25..."
        if abs(team1.evanmiyaInjuryRank - team2.evanmiyaInjuryRank) > 25:
            # "pick higher rank"
            if team1.evanmiyaInjuryRank < team2.evanmiyaInjuryRank:
                return team1, team2
            else:
                return team2, team1

        # "If not, subtract points allowed from points scored and select team with greater value..."
        # (Using BPR for this, see note above)
        # "...unless difference is less than 5."
        elif abs(team1.evanmiyaBPR - team2.evanmiyaBPR) >= 5:
            if team1.evanmiyaBPR > team2.evanmiyaBPR:
                return team1, team2
            else:
                return team2, team1

        # "If not greater than 5, pick team with more KillShotsPerGame."
        else:
            if team1.evanmiyaKillShotsPerGame > team2.evanmiyaKillShotsPerGame:
                return team1, team2
            elif team2.evanmiyaKillShotsPerGame > team1.evanmiyaKillShotsPerGame:
                return team2, team1
            # Editorial: it is possible for the above to end in a tie,
            #   which won't work. If we get all the way to the bottom,
            #   we just go back to picking based on InjuryRank.
            else:
                if team1.evanmiyaInjuryRank < team2.evanmiyaInjuryRank:
                    return team1, team2
                else:
                    return team2, team1

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 75, 67

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        """
        We're not actually using _team_metric() in this strategy, though
        we made this an @abstractmethod, so it has to be implemented.

        We did this because the default pick() method uses _team_metric().
        However, we may wanna relax this at some point because... of things like this.
        """
        return NotImplemented
