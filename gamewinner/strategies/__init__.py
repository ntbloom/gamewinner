# from gamewinner.strategies.evanmiya.chillz import Chillz, KillerChillz
# from gamewinner.strategies.evanmiya.doctor_lizard import DoctorLizard
# from gamewinner.strategies.evanmiya.firewater import FireWaterFireWater
# from gamewinner.strategies.evanmiya.mr_freeze import MrFreeze
# from gamewinner.strategies.evanmiya.slothfire_steady import (
#     SlothfireSteadiest,
#     SlothfireSteady,
#     SlothfireSteadyBayz,
# )
# from gamewinner.strategies.evanmiya.the_cuts import (
#     TheCuts23,
#     TheCuts23DumBayz,
#     TheCuts23Frozen,
# )
# from gamewinner.strategies.evanmiya.the_white_whale import TheWhiteWhale
# from gamewinner.strategies.evanmiya.theowl import TheOwl
# from gamewinner.strategies.evanmiya.vanilla_miya import VanillaMiya

from gamewinner.strategies.examples.best_rank_wins import BestRankWins
from gamewinner.strategies.examples.worst_rank_wins import WorstRankWins
from gamewinner.strategies.istrategy import Strategy  # noqa

available_strategies = (
    BestRankWins(),
    # Chillz(),
    # DoctorLizard(),
    # FireWaterFireWater(),
    # KillerChillz(),
    # MrFreeze(),
    # SlothfireSteady(),
    # SlothfireSteadiest(),
    # SlothfireSteadyBayz(),
    # TheCuts23(),
    # TheCuts23Frozen(),
    # TheCuts23DumBayz(),
    # TheOwl(),
    # TheWhiteWhale(),
    # VanillaMiya(),
    WorstRankWins(),
)
