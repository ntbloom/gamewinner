import subprocess

import pytest

from gamewinner import play
from gamewinner.strategies import Strategy, available_strategies


class TestCli:
    @pytest.mark.parametrize("cli_strategy", available_strategies)
    def test_invoke_strategy(self, cli_strategy: Strategy) -> None:
        subprocess.run(
            f"make play strategy={cli_strategy.name}", shell=True
        ).check_returncode()

    def test_gamewinner_main_with_only_strategy(self) -> None:
        play(strategy=available_strategies[0])
