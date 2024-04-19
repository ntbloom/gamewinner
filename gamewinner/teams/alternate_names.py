# A simple dictionary where the key is the `definitive name` and the value is a
# list of nicknames.  We can build up this list as we go, including adding new
# teams or nicknames as needed.  We may also need to update definitive names to
# something more clear, though this is for now a terse and simple starting
# point. `alternate_names` is the user-friendly data structure where the team
# names are in alphabetical order, but the `name_map` variable built below should
# be imported in other modules.
alternate_names: dict[str, list[str]] = {
    "Abilene Christian": [],
    "Air Force": [],
    "Akron": [],
    "Alabama": [],
    "Alabama A&M": [],
    "Alabama State": [],
    "Albany": [],
    "Alcorn State": [],
    "American": [],
    "Appalachian State": [],
    "Arizona": [],
    "Arizona State": ["ASU"],
    "Arkansas": [],
    "Arkansas State": [],
    "Arkansas-Little Rock": [],
    "Arkansas-Pine Bluff": [],
    "Army": [],
    "Auburn": [],
    "Austin Peay": [],
    "BYU": [],
    "Ball State": [],
    "Baylor": [],
    "Bellarmine": [],
    "Belmont": [],
    "Bethune-Cookman": [],
    "Binghamton": [],
    "Boise State": [],
    "Boston College": [],
    "Boston University": [],
    "Bowling Green": [],
    "Bradley": [],
    "Brown": [],
    "Bryant": [],
    "Bucknell": [],
    "Buffalo": [],
    "Butler": [],
    "Cal Poly": [],
    "Cal State Bakersfield": [],
    "Cal State Fullerton": [],
    "Cal State Northridge": [],
    "California": [],
    "California Baptist": [],
    "Campbell": [],
    "Canisius": [],
    "Central Arkansas": [],
    "Central Connecticut": [],
    "Central Michigan": [],
    "Charleston Southern": [],
    "Charlotte": [],
    "Chattanooga": [],
    "Chicago State": [],
    "Cincinnati": [],
    "Clemson": [],
    "Cleveland State": [],
    "Coastal Carolina": [],
    "Colgate": [],
    "College of Charleston": ["Charleston"],
    "Colorado": [],
    "Colorado State": [],
    "Columbia": [],
    "Connecticut": ["UConn"],
    "Coppin State": [],
    "Cornell": [],
    "Creighton": [],
    "Dartmouth": [],
    "Davidson": [],
    "Dayton": [],
    "DePaul": [],
    "Delaware": [],
    "Delaware State": [],
    "Denver": [],
    "Detroit": [],
    "Drake": [],
    "Drexel": [],
    "Duke": [],
    "Duquesne": [],
    "East Carolina": [],
    "East Tennessee State": [],
    "Eastern Illinois": [],
    "Eastern Kentucky": [],
    "Eastern Michigan": [],
    "Eastern Washington": [],
    "Elon": [],
    "Evansville": [],
    "Fairfield": [],
    "Fairleigh Dickinson": [],
    "Florida": [],
    "Florida A&M": [],
    "Florida Atlantic": ["FAU"],
    "Florida Gulf Coast": [],
    "Florida International": [],
    "Florida State": [],
    "Fordham": [],
    "Fort Wayne": [],
    "Fresno State": [],
    "Furman": [],
    "Gardner-Webb": [],
    "George Mason": [],
    "George Washington": [],
    "Georgetown": [],
    "Georgia": [],
    "Georgia Southern": [],
    "Georgia State": [],
    "Georgia Tech": [],
    "Gonzaga": [],
    "Grambling": [],
    "Grand Canyon": [],
    "Green Bay": [],
    "Hampton": [],
    "Hartford": [],
    "Harvard": [],
    "Hawaii": [],
    "High Point": [],
    "Hofstra": [],
    "Holy Cross": [],
    "Houston": [],
    "Houston Christian": [],
    "Howard": [],
    "IUPUI": [],
    "Idaho": [],
    "Idaho State": [],
    "Illinois": [],
    "Illinois State": [],
    "Illinois-Chicago": [],
    "Incarnate Word": [],
    "Indiana": [],
    "Indiana State": [],
    "Iona": [],
    "Iowa": [],
    "Iowa State": [],
    "Jackson State": [],
    "Jacksonville": [],
    "Jacksonville State": [],
    "James Madison": [],
    "Kansas": [],
    "Kansas State": [],
    "Kennesaw State": [],
    "Kent State": [],
    "Kentucky": [],
    "LSU": [],
    "La Salle": [],
    "Lafayette": [],
    "Lamar": [],
    "Le Moyne": [],
    "Lehigh": [],
    "Liberty": [],
    "Lindenwood": [],
    "Lipscomb": [],
    "Long Beach State": [],
    "Long Island": [],
    "Longwood": [],
    "Louisiana Tech": [],
    "Louisiana-Lafayette": [],
    "Louisiana-Monroe": [],
    "Louisville": [],
    "Loyola Chicago": [],
    "Loyola Maryland": [],
    "Loyola Marymount": [],
    "Maine": [],
    "Manhattan": [],
    "Marist": [],
    "Marquette": [],
    "Marshall": [],
    "Maryland": [],
    "Maryland-Eastern Shore": [],
    "Massachusetts": [],
    "McNeese State": ["McNeese"],
    "Memphis": [],
    "Mercer": [],
    "Merrimack": [],
    "Miami (Fla.)": ["Miami"],
    "Miami (Ohio)": [],
    "Michigan": [],
    "Michigan State": [],
    "Middle Tennessee": [],
    "Milwaukee": [],
    "Minnesota": [],
    "Mississippi State": [],
    "Mississippi Valley State": [],
    "Missouri": [],
    "Missouri State": [],
    "Missouri-Kansas City": [],
    "Monmouth": [],
    "Montana": [],
    "Montana State": [],
    "Morehead State": [],
    "Morgan State": [],
    "Mount St. Mary's": [],
    "Murray State": [],
    "NC State": [],
    "NJIT": [],
    "Navy": [],
    "Nebraska": [],
    "Nevada": [],
    "New Hampshire": [],
    "New Mexico": [],
    "New Mexico State": [],
    "New Orleans": [],
    "Niagara": [],
    "Nicholls State": [],
    "Norfolk State": [],
    "North Alabama": [],
    "North Carolina": ["UNC"],
    "North Carolina A&T": [],
    "North Carolina Central": [],
    "North Dakota": [],
    "North Dakota State": [],
    "North Florida": [],
    "North Texas": [],
    "Northeastern": [],
    "Northern Arizona": [],
    "Northern Colorado": [],
    "Northern Illinois": [],
    "Northern Iowa": [],
    "Northern Kentucky": [],
    "Northwestern": [],
    "Northwestern State": [],
    "Notre Dame": [],
    "Oakland": [],
    "Ohio": [],
    "Ohio State": [],
    "Oklahoma": [],
    "Oklahoma State": [],
    "Old Dominion": [],
    "Ole Miss": [],
    "Omaha": [],
    "Oral Roberts": [],
    "Oregon": [],
    "Oregon State": [],
    "Pacific": [],
    "Penn": [],
    "Penn State": [],
    "Pepperdine": [],
    "Pittsburgh": ["Pitt"],
    "Portland": [],
    "Portland State": [],
    "Prairie View": [],
    "Presbyterian": [],
    "Princeton": [],
    "Providence": [],
    "Purdue": [],
    "Queens": [],
    "Quinnipiac": [],
    "Radford": [],
    "Rhode Island": [],
    "Rice": [],
    "Richmond": [],
    "Rider": [],
    "Robert Morris": [],
    "Rutgers": [],
    "SIU Edwardsville": [],
    "SMU": [],
    "Sacramento State": [],
    "Sacred Heart": [],
    "Saint Bonaventure": [],
    "Saint Francis (NY)": [],
    "Saint Francis (PA)": [],
    "Saint John's": [],
    "Saint Joseph's": [],
    "Saint Louis": [],
    "Saint Mary's": [],
    "Saint Peter's": [],
    "Saint Thomas (Minn.)": [],
    "Sam Houston State": [],
    "Samford": [],
    "San Diego": [],
    "San Diego State": [],
    "San Francisco": [],
    "San Jose State": [],
    "Santa Clara": [],
    "Seattle": [],
    "Seton Hall": [],
    "Siena": [],
    "South Alabama": [],
    "South Carolina": [],
    "South Carolina State": [],
    "South Carolina Upstate": [],
    "South Dakota": [],
    "South Dakota State": [],
    "South Florida": [],
    "Southeast Missouri State": [],
    "Southeastern Louisiana": [],
    "Southern": [],
    "Southern Illinois": [],
    "Southern Indiana": [],
    "Southern Mississippi": [],
    "Southern Utah": [],
    "Stanford": [],
    "Stephen F. Austin": [],
    "Stetson": [],
    "Stonehill": [],
    "Stony Brook": [],
    "Syracuse": [],
    "TCU": [],
    "Tarleton State": [],
    "Temple": [],
    "Tennessee": [],
    "Tennessee State": [],
    "Tennessee Tech": [],
    "Tennessee-Martin": [],
    "Texas": [],
    "Texas A&M": [],
    "Texas A&M-Commerce": ["Texas A&M Commerce"],
    "Texas A&M-Corpus Christi": [],
    "Texas Southern": [],
    "Texas State": [],
    "Texas Tech": [],
    "Texas-Rio Grande Valley": [],
    "The Citadel": [],
    "Toledo": [],
    "Towson": [],
    "Troy": [],
    "Tulane": [],
    "Tulsa": [],
    "UAB": [],
    "UC Davis": [],
    "UC Irvine": [],
    "UC Riverside": [],
    "UC San Diego": [],
    "UC Santa Barbara": ["UCSB", "University of California Santa Barbara"],
    "UCF": [],
    "UCLA": [],
    "UMBC": [],
    "UMass Lowell": [],
    "UNC Asheville": [],
    "UNC Greensboro": [],
    "UNC Wilmington": [],
    "UNLV": [],
    "USC": [],
    "UT Arlington": [],
    "UTEP": [],
    "UTSA": [],
    "Utah": [],
    "Utah State": [],
    "Utah Tech": [],
    "Utah Valley": [],
    "VCU": [],
    "VMI": [],
    "Valparaiso": [],
    "Vanderbilt": [],
    "Vermont": [],
    "Villanova": [],
    "Virginia": ["UVA"],
    "Virginia Tech": [],
    "Wagner": [],
    "Wake Forest": [],
    "Washington": [],
    "Washington State": [],
    "Weber State": [],
    "West Virginia": [],
    "Western Carolina": [],
    "Western Illinois": [],
    "Western Kentucky": [],
    "Western Michigan": [],
    "Wichita State": [],
    "William & Mary": [],
    "Winthrop": [],
    "Wisconsin": [],
    "Wofford": [],
    "Wright State": [],
    "Wyoming": [],
    "Xavier": [],
    "Yale": [],
    "Youngstown State": [],
}

name_map = {}
for definitive, nicknames in alternate_names.items():
    name_map[definitive.lower()] = definitive
    for nickname in nicknames:
        name_map[nickname.lower()] = definitive
