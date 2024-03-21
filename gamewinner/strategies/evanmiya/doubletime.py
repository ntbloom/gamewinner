import random
from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import EvanMiyaStrategy
from gamewinner.strategies.evanmiya.ievanmiya import ESPNStrategy
from gamewinner.team import Team


class Doubletime(IStrategy):
    """
    
    """

    @property
    def name(self) -> str:
        return "Doubletime"

    def prepare(self, teams: dict[str, Team]) -> None:
        self.em_props = EvanMiyaStrategy.load_data(teams)
        self.espn_props = ESPNStrategy.load_data(teams)

        self.data = pd.join(
            EvanMiyaStrategy.load_data(teams),
            ESPNStrategy.load_data(teams),
            by = "team"
        )




    #def get_props(self, team: Team) -> EMProps:
    #
    #    self.em = self.em_props.get(team.name, None)
    #    self.espn = self.espn_props.get(team.name, None)

    @no_type_check
    def _team_metric(self, team: Team) -> float:

        em_props = self.em_props.get(team.name, None)
        espn_props = self.espn_props.get(team.name, None)

        assert em_props and espn_props


        #overall_score = (
        #    self._rank_to_percentile(em_props.rank)
        #    + 0.5 * self._rank_to_percentile(em_props.TempoRank, reverse=True)
        #    + 0.3 * self._rank_to_percentile(espn_props.some_stat)
        #)


        overall_score = (
            helper.percentile(em_props.BPR) + 
            helper.rank(espn_props.FTP)
        )

        # upset factor
        overall_score = overall_score + random.random() * (
            self._rank_to_percentile(team.evanmiyaResumeRank)
            + min(self._rank_to_percentile(team.evanmiyaHomeRank, reverse=True), 0.5)
        )

        return overall_score



    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        """
        By default, this picks the team with the higher self._team_metric() score
        """
        team1_overall = self._team_metric(team1)
        team2_overall = self._team_metric(team2)

        if team1_overall > team2_overall:
            return team1, team2
        else:
            return team2, team1