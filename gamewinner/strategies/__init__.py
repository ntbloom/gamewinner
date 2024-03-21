from gamewinner.strategies.examples.best_rank_wins import BestRankWins
from gamewinner.strategies.examples.worst_rank_wins import WorstRankWins
from gamewinner.strategies.istrategy import Strategy  # noqa
from gamewinner.strategies.mathstats.derived.chillz import Chillz, KillerChillz
from gamewinner.strategies.mathstats.derived.doctor_lizard import DoctorLizard
from gamewinner.strategies.mathstats.derived.firewater import FireWaterFireWater
from gamewinner.strategies.mathstats.derived.mr_freeze import MrFreeze
from gamewinner.strategies.mathstats.derived.slothfire_steady import (
    SlothfireSteadiest,
    SlothfireSteady,
    SlothfireSteadyBayz,
)
from gamewinner.strategies.mathstats.derived.the_cuts import (
    TheCuts23,
    TheCuts23DumBayz,
    TheCuts23Frozen,
)
from gamewinner.strategies.mathstats.derived.the_white_whale import TheWhiteWhale
from gamewinner.strategies.mathstats.derived.theowl import TheOwl
from gamewinner.strategies.mathstats.derived.vanilla import Vanilla

available_strategies = (
    BestRankWins(),
    Chillz(),
    DoctorLizard(),
    FireWaterFireWater(),
    KillerChillz(),
    MrFreeze(),
    TheOwl(),
    TheWhiteWhale(),
    Vanilla(),
    WorstRankWins(),
    SlothfireSteady(),
    SlothfireSteadiest(),
    SlothfireSteadyBayz(),
    TheCuts23(),
    TheCuts23Frozen(),
    TheCuts23DumBayz(),
)
