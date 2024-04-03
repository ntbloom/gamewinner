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
        assert Game(one, two, Stage.FirstRound)

    @pytest.mark.parametrize("one,two", [(east1, east2), (west3, west4)])
    def test_game_order_doesnt_matter(self, one: Team, two: Team) -> None:
        first = Stage.FirstRound
        assert Game(one, two, first) == Game(two, one, first)

    @pytest.mark.parametrize("one,two", [(east1, east2), (west3, west4)])
    def test_game_round_matters(self, one: Team, two: Team) -> None:
        assert Game(one, two, Stage.FirstRound) != Game(one, two, Stage.SecondRound)

    def test_game_bad_same_team(self) -> None:
        with pytest.raises(MatchupError):
            Game(east1, east1, Stage.FirstRound)

    @pytest.mark.parametrize("late_round", [Stage.FinalFour, Stage.Finals])
    def test_game_bad_same_region_final_four(self, late_round: Stage) -> None:
        with pytest.raises(MatchupError):
            Game(east1, east2, late_round)

    @pytest.mark.parametrize(
        "early_round",
        [Stage.FirstRound, Stage.SecondRound, Stage.EliteEight, Stage.SweetSixteen],
    )
    def test_game_bad_different_region_early(self, early_round: Stage) -> None:
        with pytest.raises(MatchupError):
            Game(east1, west3, early_round)
