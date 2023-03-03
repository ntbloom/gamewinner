import pytest

from gamewinner import GeographicRegion, Region, Strategy, Team

nat_rank_counter = 1


def _make_region(region_name: str, strategy: Strategy) -> Region:
    region = GeographicRegion(region_name)
    teams: list[Team] = []
    for i in range(1, 17):
        name = f"{region_name}{i}"
        regional_rank = i
        # change this value later if we want?
        global nat_rank_counter
        national_rank = nat_rank_counter
        nat_rank_counter += 1
        teams.append(Team(name, region, regional_rank, national_rank))
    wildcards = [Team(f"{region_name}-wildcard{i}", region, i, i) for i in (17, 18)]
    return Region(teams, wildcards, strategy)


@pytest.fixture(scope="module")
def strategy() -> Strategy:
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

    return HighestWins()
