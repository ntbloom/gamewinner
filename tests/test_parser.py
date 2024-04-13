import pytest

from gamewinner.bracket.parsers import ResultsParser, SeedParser
from gamewinner.teams.team import Team, get_definitive_name


@pytest.fixture(scope="function")
def seed_parser(test_year: int) -> SeedParser:
    parser = SeedParser(test_year)
    assert parser.year == test_year
    return parser


@pytest.fixture(scope="function")
def results_parser(test_year: int) -> ResultsParser:
    if test_year == 2023:
        pytest.skip(reason="TODO: write me!")

    parser = ResultsParser(test_year)
    assert parser.year == test_year
    return parser


class TestSeedParser:
    def test_seed_parser_regions(self, seed_parser: SeedParser) -> None:
        assert seed_parser.west_plays
        for region in (
            seed_parser.east,
            seed_parser.west,
            seed_parser.south,
            seed_parser.midwest,
        ):
            assert len(region) == 16
            assert sum(region.keys()) == 136
            assert len(set(region.values())) == 16

    def test_seed_parser_finds_all_teams(self, seed_parser: SeedParser) -> None:
        assert len(set(seed_parser.teams)) == 64
        for team in seed_parser.teams:
            assert isinstance(team, Team)


class TestResultsParser:
    def test_results_parser_has_correct_count(
        self, results_parser: ResultsParser
    ) -> None:
        assert len(results_parser.first_round_winners) == 32
        assert len(results_parser.second_round_winners) == 16
        assert len(results_parser.sweet_sixteen_winners) == 8
        assert len(results_parser.elite_eight_winners) == 4
        assert len(results_parser.final_four_winners) == 2
        assert len(results_parser.winner) == 1

    def test_results_have_valid_team_names(self, results_parser: ResultsParser) -> None:
        for name in results_parser.team_names:
            assert get_definitive_name(name)

    def test_results_parser_teams_play_each_round(
        self, results_parser: ResultsParser
    ) -> None:
        for team in results_parser.winner:
            assert team in results_parser.final_four_winners
            assert team in results_parser.elite_eight_winners
            assert team in results_parser.sweet_sixteen_winners
            assert team in results_parser.second_round_winners
            assert team in results_parser.first_round_winners

        for team in results_parser.final_four_winners:
            assert team in results_parser.elite_eight_winners
            assert team in results_parser.sweet_sixteen_winners
            assert team in results_parser.second_round_winners
            assert team in results_parser.first_round_winners

        for team in results_parser.elite_eight_winners:
            assert team in results_parser.sweet_sixteen_winners
            assert team in results_parser.second_round_winners
            assert team in results_parser.first_round_winners

        for team in results_parser.sweet_sixteen_winners:
            assert team in results_parser.second_round_winners
            assert team in results_parser.first_round_winners

        for team in results_parser.second_round_winners:
            assert team in results_parser.first_round_winners

    def test_final_score(self, results_parser: ResultsParser) -> None:
        score = results_parser.final_score
        assert score and score[0] > score[1]
