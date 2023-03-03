import pytest

from gamewinner.strategies import HighestWins, LowestWins
from gamewinner.team import GeographicRegion
from tests.conftest import _make_region


class TestGenerateBrackets:
    @pytest.mark.parametrize("geographic_region", GeographicRegion)
    def test_regional_winners_of_lowest_rank(
        self, geographic_region: GeographicRegion
    ) -> None:
        region = _make_region(geographic_region.value, LowestWins())
        # round 1
        assert region.g1.rank_reg == 1
        assert region.g2.rank_reg == 8
        assert region.g3.rank_reg == 5
        assert region.g4.rank_reg == 4
        assert region.g5.rank_reg == 6
        assert region.g6.rank_reg == 3
        assert region.g7.rank_reg == 7
        assert region.g8.rank_reg == 2

        # round 2
        assert region.g9.rank_reg == 1
        assert region.g10.rank_reg == 4
        assert region.g11.rank_reg == 3
        assert region.g12.rank_reg == 2

        # round 3
        assert region.g13.rank_reg == 1
        assert region.g14.rank_reg == 2

        # winner
        assert region.g15.rank_reg == 1
        assert region.winner.rank_reg == 1

    @pytest.mark.parametrize("geographic_region", GeographicRegion)
    def test_regional_winners_of_highest_rank(
        self, geographic_region: GeographicRegion
    ) -> None:
        region = _make_region(geographic_region.value, HighestWins())
        # round 1
        assert region.g1.rank_reg == 16
        assert region.g2.rank_reg == 9
        assert region.g3.rank_reg == 12
        assert region.g4.rank_reg == 13
        assert region.g5.rank_reg == 11
        assert region.g6.rank_reg == 14
        assert region.g7.rank_reg == 10
        assert region.g8.rank_reg == 15

        # round 2
        assert region.g9.rank_reg == 16
        assert region.g10.rank_reg == 13
        assert region.g11.rank_reg == 14
        assert region.g12.rank_reg == 15

        # round 3
        assert region.g13.rank_reg == 16
        assert region.g14.rank_reg == 15

        # winner
        assert region.g15.rank_reg == 16
        assert region.winner.rank_reg == 16
