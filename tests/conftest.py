from gamewinner import GeographicRegion, Region, Strategy, Team

nat_rank_counter = 1


def _make_region(region_name: str, strategy: Strategy) -> Region:
    region = GeographicRegion(region_name)
    teams: list[Team] = []
    for i in range(1, 17):
        name = f"{region_name}{i}"
        regional_rank = i
        # change this value later if we want?
        global nat_rank_counter
        national_rank = nat_rank_counter
        nat_rank_counter += 1
        teams.append(Team(name, region, regional_rank, national_rank))
    wildcards = [Team(f"{region_name}-wildcard{i}", region, i, i) for i in (17, 18)]
    return Region(teams, wildcards, strategy)
