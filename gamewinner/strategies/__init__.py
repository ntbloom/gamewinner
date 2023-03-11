from gamewinner.strategies.evanmiya.slothfire_steady import SlothfireSteady  # noqa
from gamewinner.strategies.evanmiya.the_cuts import TheCuts23  # noqa
from gamewinner.strategies.evanmiya.vanilla_miya import VanillaMiya  # noqa
from gamewinner.strategies.examples.best_rank_wins import BestRankWins  # noqa
from gamewinner.strategies.examples.worst_rank_wins import WorstRankWins  # noqa
from gamewinner.strategies.istrategy import Strategy  # noqa

available_strategies = (
    BestRankWins(),
    SlothfireSteady(),
    TheCuts23(),
    VanillaMiya(),
    WorstRankWins(),
)
