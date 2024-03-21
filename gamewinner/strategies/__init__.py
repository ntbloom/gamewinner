from gamewinner.strategies.examples.best_rank_wins import BestRankWins
from gamewinner.strategies.examples.worst_rank_wins import WorstRankWins
from gamewinner.strategies.istrategy import Strategy  # noqa
from gamewinner.strategies.mathstats.derived.chillz import Chillz, KillerChillz
from gamewinner.strategies.mathstats.derived.doctor_lizard import DoctorLizard
from gamewinner.strategies.mathstats.derived.firewater import FireWaterFireWater
from gamewinner.strategies.mathstats.derived.mr_freeze import MrFreeze
from gamewinner.strategies.mathstats.derived.the_white_whale import TheWhiteWhale
from gamewinner.strategies.mathstats.derived.theowl import TheOwl
from gamewinner.strategies.mathstats.derived.vanilla import Vanilla
from gamewinner.strategies.mathstats.derived.slothfire_steady import SlothfireSteady
from gamewinner.strategies.mathstats.derived.slothfire_steady import SlothfireSteadiest
from gamewinner.strategies.mathstats.derived.slothfire_steady import SlothfireSteadyBayz

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
)
