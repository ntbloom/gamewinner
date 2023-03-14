from gamewinner.strategies.evanmiya.mr_freeze import MrFreeze
from gamewinner.strategies.evanmiya.slothfire_steady import SlothfireSteady  # noqa
from gamewinner.strategies.evanmiya.the_cuts import TheCuts23  # noqa
from gamewinner.strategies.evanmiya.the_cuts import TheCuts23DumBayz  # noqa
from gamewinner.strategies.evanmiya.vanilla_miya import VanillaMiya  # noqa
from gamewinner.strategies.examples.best_rank_wins import BestRankWins  # noqa
from gamewinner.strategies.examples.worst_rank_wins import WorstRankWins  # noqa
from gamewinner.strategies.istrategy import Strategy  # noqa

available_strategies = (
    BestRankWins(),
    MrFreeze(),
    SlothfireSteady(),
    TheCuts23(),
    TheCuts23DumBayz(),
    VanillaMiya(),
    WorstRankWins(),
)
