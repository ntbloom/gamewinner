from gamewinner.bracket.parsers import SeedParser
from gamewinner.teams.team import Team


class TestParser:
    def test_seed_parser(self, test_year: int) -> None:
        parser = SeedParser(test_year)
        assert parser.west_plays
        assert parser.year == test_year
        for region in (parser.east, parser.west, parser.south, parser.midwest):
            assert len(region) == 16
            assert sum(region.keys()) == 136
            assert len(set(region.values())) == 16
        assert len(set(parser.teams)) == 64
        for team in parser.teams:
            assert isinstance(team, Team)
