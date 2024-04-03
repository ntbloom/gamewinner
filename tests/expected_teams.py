from gamewinner.teams.team import get_definitive_name

matchup = set[str]


def make_set(matchups: list[matchup]) -> list[matchup]:
    return [
        {get_definitive_name(game.pop()), get_definitive_name(game.pop())}
        for game in matchups
    ]


class ExpectedTeamData:
    def __init__(
        self,
        winner: str,
        finals: matchup,
        final_four: list[matchup],
        elite_eight: list[matchup],
        sweet_sixteen: list[matchup],
        second_round: list[matchup],
        first_round: list[matchup],
    ):
        self.winner = get_definitive_name(winner)
        self.finals = {get_definitive_name(game) for game in finals}
        self.final_four = make_set(final_four)
        self.elite_eight = make_set(elite_eight)
        self.sweet_sixteen = make_set(sweet_sixteen)
        self.second_round = make_set(second_round)
        self.first_round = make_set(first_round)

        assert self.winner
        assert len(final_four) == 2
        assert len(elite_eight) == 4
        assert len(sweet_sixteen) == 8
        assert len(second_round) == 16
        assert len(first_round) == 32


Expected2024 = ExpectedTeamData(
    winner="UConn",
    finals={"Houston", "UConn"},
    final_four=[
        {"UNC", "UConn"},
        {"Houston", "Purdue"},
    ],
    elite_eight=[
        {"UConn", "Iowa State"},
        {"UNC", "Arizona"},
        {"Purdue", "Tennessee"},
        {"Houston", "Marquette"},
    ],
    sweet_sixteen=[
        {"UNC", "Alabama"},
        {"Baylor", "Arizona"},
        {"Purdue", "Kansas"},
        {"Creighton", "Tennessee"},
        {"UConn", "Auburn"},
        {"Illinois", "Iowa State"},
        {"Houston", "Duke"},
        {"Marquette", "Kentucky"},
    ],
    second_round=[
        {"UConn", "FAU"},
        {"San Diego State", "Auburn"},
        {"BYU", "Illinois"},
        {"Washington State", "Iowa State"},
        {"UNC", "Mississippi State"},
        {"Saint Mary's", "Alabama"},
        {"Clemson", "Baylor"},
        {"Dayton", "Arizona"},
        {"Purdue", "Utah State"},
        {"Gonzaga", "Kansas"},
        {"South Carolina", "Creighton"},
        {"Texas", "Tennessee"},
        {"Houston", "Nebraska"},
        {"Wisconsin", "Duke"},
        {"Texas Tech", "Kentucky"},
        {"Florida", "Marquette"},
    ],
    first_round=[
        {"UNC", "Wagner"},
        {"Mississippi State", "Michigan State"},
        {"Saint Mary's", "Grand Canyon"},
        {"Alabama", "Charleston"},
        {"Clemson", "New Mexico"},
        {"Baylor", "Colgate"},
        {"Dayton", "Nevada"},
        {"Arizona", "Long Beach State"},
        {"Purdue", "Grambling"},
        {"Utah State", "TCU"},
        {"Gonzaga", "McNeese"},
        {"Kansas", "Samford"},
        {"South Carolina", "Oregon"},
        {"Creighton", "Akron"},
        {"Texas", "Colorado State"},
        {"Tennessee", "Saint Peter's"},
        {"UConn", "Stetson"},
        {"FAU", "Northwestern"},
        {"San Diego State", "UAB"},
        {"Auburn", "Yale"},
        {"BYU", "Duquesne"},
        {"Illinois", "Morehead State"},
        {"Washington State", "Drake"},
        {"Iowa State", "South Dakota State"},
        {"Houston", "Longwood"},
        {"Nebraska", "Texas A&M"},
        {"Wisconsin", "James Madison"},
        {"Duke", "Vermont"},
        {"Texas Tech", "NC State"},
        {"Kentucky", "Oakland"},
        {"Florida", "Colorado"},
        {"Marquette", "Western Kentucky"},
    ],
)
