#!/usr/bin/env python3
"""Check which 2026 tournament team names need to be added to alternate_names.py"""
import sys, os
# Parse alternate_names.py manually to avoid importing gamewinner (needs Python 3.10+)
names_file = os.path.join(os.path.dirname(__file__), "..", "gamewinner", "teams", "alternate_names.py")
with open(names_file) as f:
    code = f.read()
exec(code)  # defines alternate_names and name_map

canonical_names = [
    "Duke", "Connecticut", "Michigan State", "Kansas", "Saint John's",
    "Louisville", "UCLA", "Ohio State", "TCU", "UCF", "South Florida",
    "Northern Iowa", "California Baptist", "North Dakota State", "Furman",
    "Siena", "Michigan", "Iowa State", "Virginia", "Alabama", "Texas Tech",
    "Tennessee", "Kentucky", "Georgia", "Saint Louis", "Santa Clara", "SMU",
    "Miami (Ohio)", "Akron", "Hofstra", "Wright State", "Tennessee State",
    "Howard", "UMBC", "Florida", "Houston", "Illinois", "Nebraska",
    "Vanderbilt", "North Carolina", "Saint Mary's", "Clemson", "Iowa",
    "Texas A&M", "VCU", "McNeese State", "Troy", "Penn", "Idaho", "Lehigh",
    "Prairie View", "Arizona", "Purdue", "Gonzaga", "Arkansas", "Wisconsin",
    "BYU", "Miami (Fla.)", "Villanova", "Utah State", "Missouri", "NC State",
    "Texas", "High Point", "Hawaii", "Kennesaw State", "Queens", "Long Island",
]

print("=== Canonical name check ===")
missing = []
for name in canonical_names:
    if name_map.get(name.lower()):
        pass
    else:
        missing.append(name)
        print(f"  MISSING: {name}")

if not missing:
    print("All canonical names found!")

# Check aliases that ESPN uses
print("\n=== ESPN alias check ===")
espn_aliases = {
    "UConn": "Connecticut",
    "McNeese": "McNeese State",
    "St. John's": "Saint John's",
    "Hawai'i": "Hawaii",
    "Queens University": "Queens",
    "Long Island University": "Long Island",
    "Prairie View A&M": "Prairie View",
    "Pennsylvania": "Penn",
    "Miami (OH)": "Miami (Ohio)",
}
for alias, canonical in espn_aliases.items():
    found = name_map.get(alias.lower())
    if found:
        print(f"  OK: '{alias}' -> {found}")
    else:
        print(f"  NEED ALIAS: '{alias}' should map to '{canonical}'")
