from typing import Any

from rich.console import Console

from gamewinner.games.bracket import Bracket
from gamewinner.printers.plain_text import PlainText
from gamewinner.team import Team

console = Console()


class WithColors(PlainText):
    name = "Rich"

    winning_team_color = "green"
    losing_team_color = "bright_black"
    start_win = f"[{winning_team_color}]"
    end_win = f"[/{winning_team_color}]"
    start_lose = f"[{losing_team_color}]"
    end_lose = f"[/{losing_team_color}]"

    @staticmethod
    def print(bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        WithColors._print(bracket)

    @classmethod
    def _print(cls, bracket: Bracket) -> None:
        console.print(
            f"Overall prediction for {bracket.strategy.name}/{bracket.year.year}: "
            f"[bold {WithColors.winning_team_color}]{bracket.winner}"
            f"[/bold {WithColors.winning_team_color}] "
            f"over {bracket.runner_up}: "
            f"{bracket.final_score}"
        )
        cls._first_four(bracket)
        for region in bracket.regions:
            cls._region(region)
        cls._final_four(bracket)
        console.print()
        console.print(f"[magenta]{len(bracket.upsets)} upsets predicted:")
        for upset in bracket.upsets:
            console.print(f"[magenta]\t{upset}")

    @classmethod
    def _print_game(cls, winner: Team, loser: Team, indentation: int = 0) -> None:
        tabs = indentation * "\t"
        console.print(
            f"{tabs}{WithColors.start_win}{winner}{WithColors.end_win} beats {WithColors.start_lose}{loser}{WithColors.end_lose}"  # noqa
        )
