from datetime import datetime

from gamewinner.bracket import this_year


def test_this_year() -> None:
    assert this_year == datetime.now().year
