from gamewinner.strategies.evanmiya.chillz import Chillz  # noqa
from gamewinner.strategies.evanmiya.chillz import KillerChillz  # noqa
from gamewinner.strategies.evanmiya.doctor_lizard import DoctorLizard  # noqa
from gamewinner.strategies.evanmiya.firewater import FireWaterFireWater  # noqa
from gamewinner.strategies.evanmiya.mr_freeze import MrFreeze
from gamewinner.strategies.evanmiya.slothfire_steady import SlothfireSteadiest  # noqa
from gamewinner.strategies.evanmiya.slothfire_steady import SlothfireSteady  # noqa
from gamewinner.strategies.evanmiya.slothfire_steady import SlothfireSteadyBayz  # noqa
from gamewinner.strategies.evanmiya.the_cuts import TheCuts23  # noqa
from gamewinner.strategies.evanmiya.the_cuts import TheCuts23DumBayz  # noqa
from gamewinner.strategies.evanmiya.the_cuts import TheCuts23Frozen  # noqa
from gamewinner.strategies.evanmiya.the_white_whale import TheWhiteWhale
from gamewinner.strategies.evanmiya.vanilla_miya import VanillaMiya  # noqa
from gamewinner.strategies.examples.best_rank_wins import BestRankWins  # noqa
from gamewinner.strategies.examples.worst_rank_wins import WorstRankWins  # noqa
from gamewinner.strategies.istrategy import Strategy  # noqa

available_strategies = (
    BestRankWins(),
    MrFreeze(),
    SlothfireSteady(),
    SlothfireSteadiest(),
    SlothfireSteadyBayz(),
    TheCuts23(),
    TheCuts23Frozen(),
    TheCuts23DumBayz(),
    TheWhiteWhale(),
    Chillz(),
    KillerChillz(),
    VanillaMiya(),
    DoctorLizard(),
    FireWaterFireWater(),
    WorstRankWins(),
)
