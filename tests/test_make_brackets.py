import pytest

from gamewinner.games.bracket import Bracket
from gamewinner.games.region import Region
from gamewinner.strategies import BestRankWins, WorstRankWins
from gamewinner.strategies.istrategy import IStrategy
from gamewinner.team import GeographicRegion, Team

nat_rank_counter = 1


def _make_region(
    region_name: str, strategy: IStrategy, simulate: bool = True
) -> Region:
    region = GeographicRegion(region_name)
    teams: list[Team] = []
    for i in range(1, 17):
        name = f"{region_name}{i}"
        regional_rank = i
        global nat_rank_counter
        national_rank = nat_rank_counter
        nat_rank_counter += 1
        teams.append(Team(name, region, regional_rank, national_rank))
    reg = Region(region, teams, strategy)
    if simulate:
        reg.first_round()
        reg.second_round()
        reg.sweet_sixteen()
        reg.elite_eight()
    return reg


@pytest.fixture(autouse=True, scope="function")
def reset_national_counter() -> None:
    """Reset the global counter after each test to not let global state bleed"""
    global nat_rank_counter
    nat_rank_counter = 1


class TestGenerateRegionalBrackets:
    """
    These tests use naive tests of highest/lowest to make sure that we built the trees
    correctly
    """

    @pytest.mark.parametrize("geographic_region", GeographicRegion)
    def test_regional_winners_of_best_rank(
        self, geographic_region: GeographicRegion
    ) -> None:
        region = _make_region(geographic_region.value, BestRankWins())
        # round 1
        assert region.w1.rank_reg == 1
        assert region.w2.rank_reg == 8
        assert region.w3.rank_reg == 5
        assert region.w4.rank_reg == 4
        assert region.w5.rank_reg == 6
        assert region.w6.rank_reg == 3
        assert region.w7.rank_reg == 7
        assert region.w8.rank_reg == 2

        # round 2
        assert region.w9.rank_reg == 1
        assert region.w10.rank_reg == 4
        assert region.w11.rank_reg == 3
        assert region.w12.rank_reg == 2

        # round 3
        assert region.w13.rank_reg == 1
        assert region.w14.rank_reg == 2

        # winner
        assert region.w15.rank_reg == 1
        assert region.winner.rank_reg == 1

    @pytest.mark.parametrize("geographic_region", GeographicRegion)
    def test_regional_winners_of_worst_rank(
        self, geographic_region: GeographicRegion
    ) -> None:
        region = _make_region(geographic_region.value, WorstRankWins())
        # round 1
        assert region.w1.rank_reg == 16
        assert region.w2.rank_reg == 9
        assert region.w3.rank_reg == 12
        assert region.w4.rank_reg == 13
        assert region.w5.rank_reg == 11
        assert region.w6.rank_reg == 14
        assert region.w7.rank_reg == 10
        assert region.w8.rank_reg == 15

        # round 2
        assert region.w9.rank_reg == 16
        assert region.w10.rank_reg == 13
        assert region.w11.rank_reg == 14
        assert region.w12.rank_reg == 15

        # round 3
        assert region.w13.rank_reg == 16
        assert region.w14.rank_reg == 15

        # winner
        assert region.w15.rank_reg == 16
        assert region.winner.rank_reg == 16

    def test_full_bracket_winners_best_rank(self) -> None:
        strategy = BestRankWins()
        west = _make_region(GeographicRegion.WEST.value, strategy, simulate=False)
        east = _make_region(GeographicRegion.EAST.value, strategy, simulate=False)
        south = _make_region(GeographicRegion.SOUTH.value, strategy, simulate=False)
        midwest = _make_region(GeographicRegion.MIDWEST.value, strategy, simulate=False)

        final_four = Bracket(
            west=west,
            east=east,
            south=south,
            midwest=midwest,
            strategy=strategy,
        )
        final_four.play()

        # west should beat east
        winner = final_four.winner
        assert winner.name == "West1"
        assert winner.rank_reg == 1
        assert winner.rank_nat == 1
        assert winner.region == GeographicRegion.WEST

        # south should beat midwest
        runner_up = final_four.runner_up
        assert runner_up.name == "South1"
        assert runner_up.rank_reg == 1
        assert runner_up.rank_nat == (16 * 2) + 1
        assert runner_up.region == GeographicRegion.SOUTH

    def test_full_bracket_winners_worst_rank(self) -> None:
        strategy = WorstRankWins()
        west = _make_region(GeographicRegion.WEST.value, strategy, simulate=False)
        east = _make_region(GeographicRegion.EAST.value, strategy, simulate=False)
        south = _make_region(GeographicRegion.SOUTH.value, strategy, simulate=False)
        midwest = _make_region(GeographicRegion.MIDWEST.value, strategy, simulate=False)

        final_four = Bracket(
            west=west,
            east=east,
            south=south,
            midwest=midwest,
            strategy=strategy,
        )
        final_four.play()

        # midwest should win as the worst overall
        winner = final_four.winner
        assert winner.name == "Midwest16"
        assert winner.rank_reg == 16
        assert winner.rank_nat == (16 * 4)
        assert winner.region == GeographicRegion.MIDWEST

        # east should beat west and get runner up
        runner_up = final_four.runner_up
        assert runner_up.name == "East16"
        assert runner_up.rank_reg == 16
        assert runner_up.rank_nat == (16 * 2)
        assert runner_up.region == GeographicRegion.EAST

    def test_print_full_bracket(self) -> None:
        """Prints the bracket outcomes, requires manual validation"""
        strategy = BestRankWins()
        final_four = Bracket(
            strategy=strategy,
            **{
                region.value.lower(): _make_region(region.value, strategy)
                for region in GeographicRegion
            },
        )
        final_four.print()
