import pytest

from gamewinner.bracket.exceptions import MatchupError
from gamewinner.bracket.game import Game
from gamewinner.bracket.geographic_region import GeographicRegion
from gamewinner.bracket.stage import Stage
from gamewinner.teams.team import Team

east1 = Team("Duke", GeographicRegion.EAST, 1)
east2 = Team("Virginia", GeographicRegion.EAST, 2)
west3 = Team("NC State", GeographicRegion.WEST, 3)
west4 = Team("James Madison", GeographicRegion.WEST, 4)


class TestGame:
    @pytest.mark.parametrize(
        "one,two",
        [
            (east1, east2),
            (east2, east1),
            (west3, west4),
            (west4, west3),
        ],
    )
    def test_game_good(self, one: Team, two: Team) -> None:
        assert Game(team1=one, team2=two, stage=Stage.FirstRound, predicted_winner=one)

    @pytest.mark.parametrize("one,two", [(east1, east2), (west3, west4)])
    def test_game_order_doesnt_matter(self, one: Team, two: Team) -> None:
        first = Stage.FirstRound
        assert Game(team1=one, team2=two, stage=first, predicted_winner=one) == Game(
            team1=two, team2=one, stage=first, predicted_winner=one
        )

    @pytest.mark.parametrize("one,two", [(east1, east2), (west3, west4)])
    def test_game_round_matters(self, one: Team, two: Team) -> None:
        assert Game(
            team1=one, team2=two, stage=Stage.FirstRound, predicted_winner=one
        ) != Game(team1=one, team2=two, stage=Stage.SecondRound, predicted_winner=one)

    def test_game_bad_same_team(self) -> None:
        with pytest.raises(MatchupError):
            Game(
                team1=east1, team2=east1, stage=Stage.FirstRound, predicted_winner=east1
            )

    @pytest.mark.parametrize("late_round", [Stage.FinalFour, Stage.Finals])
    def test_game_bad_same_region_final_four(self, late_round: Stage) -> None:
        with pytest.raises(MatchupError):
            Game(team1=east1, team2=east2, stage=late_round, predicted_winner=east1)

    @pytest.mark.parametrize(
        "early_round",
        [Stage.FirstRound, Stage.SecondRound, Stage.EliteEight, Stage.SweetSixteen],
    )
    def test_game_bad_different_region_early(self, early_round: Stage) -> None:
        with pytest.raises(MatchupError):
            Game(team1=east1, team2=west3, stage=early_round, predicted_winner=east1)

    def test_same_game_with_different_winner_is_equal(self) -> None:
        t1 = east1
        t2 = east2
        stage = Stage.FirstRound
        assert Game(team1=t1, team2=t2, stage=stage, predicted_winner=t1) == Game(
            team1=t1, team2=t2, stage=stage, predicted_winner=t2
        )
