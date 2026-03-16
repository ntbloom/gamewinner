#!/usr/bin/env python3
"""
Fetch the 2026 NCAA Tournament bracket from the ESPN API and print
the extracted team/region/seed/record data as JSON for further processing.
"""
import json
import urllib.request

# ESPN scoreboard API for tournament games (group 100 = NCAA tournament)
BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"

# Fetch games from multiple tournament dates to get all first round + first four
DATES = [
    "20260317",  # First Four
    "20260318",  # First Four
    "20260319",  # Round 1 day 1
    "20260320",  # Round 1 day 2
]

all_games = []
seen_ids = set()

for date in DATES:
    url = f"{BASE}?groups=100&dates={date}&limit=100"
    print(f"Fetching {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  Error: {e}")
        continue

    events = data.get("events", [])
    print(f"  Found {len(events)} events")
    for event in events:
        eid = event["id"]
        if eid in seen_ids:
            continue
        seen_ids.add(eid)

        comp = event["competitions"][0]
        notes = comp.get("notes", [])
        headline = notes[0]["headline"] if notes else ""

        # Determine region from headline
        region = None
        for r in ["East", "West", "South", "Midwest"]:
            if r in headline:
                region = r
                break

        is_first_four = "First Four" in headline

        for competitor in comp["competitors"]:
            team_data = competitor["team"]
            name = team_data["displayName"]
            short = team_data.get("shortDisplayName", "")
            location = team_data.get("location", "")
            abbrev = team_data.get("abbreviation", "")

            seed = competitor.get("curatedRank", {}).get("current", 0)

            # Get record
            records = competitor.get("records", [])
            overall = ""
            for rec in records:
                if rec.get("type") == "total":
                    overall = rec.get("summary", "")
                    break

            all_games.append({
                "event_id": eid,
                "headline": headline,
                "region": region,
                "is_first_four": is_first_four,
                "team_name": name,
                "team_short": short,
                "team_location": location,
                "team_abbrev": abbrev,
                "seed": seed,
                "record": overall,
            })

# Deduplicate teams
teams = {}
for g in all_games:
    key = g["team_abbrev"]
    if key not in teams or (g["region"] and not teams[key].get("region")):
        teams[key] = g

# Sort and print
print("\n" + "=" * 80)
print("EXTRACTED BRACKET DATA")
print("=" * 80)

by_region = {}
for t in teams.values():
    r = t["region"] or "Unknown"
    by_region.setdefault(r, []).append(t)

for region in ["East", "West", "South", "Midwest", "Unknown"]:
    if region not in by_region:
        continue
    entries = sorted(by_region[region], key=lambda x: x["seed"])
    print(f"\n{region}:")
    for e in entries:
        ff = " [FIRST FOUR]" if e["is_first_four"] else ""
        print(f"  {e['seed']:>2}. {e['team_location']:<25} ({e['team_abbrev']}) {e['record']}{ff}")

# Also dump raw JSON for processing
with open("scripts/bracket_2026_raw.json", "w") as f:
    json.dump(all_games, f, indent=2)
print(f"\nRaw data written to scripts/bracket_2026_raw.json")
