from typing import Any

from rich.console import Console

from gamewinner.games.bracket import Bracket
from gamewinner.printers.iprinter import IPrinter
from gamewinner.team import Team


class Rich(IPrinter):
    name = "Rich"

    @staticmethod
    def print(bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        # initialize the console for pretty printing
        console = Console()
        winning_team_color = "green"
        losing_team_color = "bright_black"

        print("Not implemented yet but will be soon!")

        def _print_game(winner: Team, loser: Team) -> str:
            start_win = f"[{winning_team_color}]"
            end_win = f"[/{winning_team_color}]"
            start_lose = f"[{losing_team_color}]"
            end_lose = f"[/{losing_team_color}]"
            return f"{start_win}{winner}{end_win}-{start_lose}{loser}{end_lose}"

        def _wip_print(bracket: Bracket, console: Console) -> None:
            assert bracket.played, "Must play bracket before printing!"
            console.print(f"[bold]Final Prediction for {bracket.strategy.name}")
            console.print(_print_game(bracket.winner, bracket.runner_up))
            console.print(
                f"Final score: {bracket.final_score[0]},{bracket.final_score[1]}"
            )

            # first four
            console.print()
            console.print("[bold]First Four:")
            for game in bracket.first_four:
                console.print(_print_game(*game))

            console.print()

            region = "west"
            console.print("[red bold]West Region")
            for i in range(1, 9):
                winner = eval(f"bracket.{region}.w{i}")
                loser = eval(f"bracket.{region}.l{i}")
                console.print(_print_game(winner, loser))

        _wip_print(bracket, console)
