#!/usr/bin/env python3
"""
Fetch W-L records for all 2026 tournament teams using the ESPN team API.
"""
import json
import urllib.request
import time

# ESPN team IDs - we need to look these up
# First, let's use the bracket raw data to get team IDs from the API
# The scoreboard API includes team IDs in the competitor objects.

# Actually, let's re-fetch and capture team IDs this time
BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"
DATES = ["20260317", "20260318", "20260319", "20260320"]

all_teams = {}

for date in DATES:
    url = f"{BASE}?groups=100&dates={date}&limit=100"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())

    for event in data.get("events", []):
        comp = event["competitions"][0]
        notes = comp.get("notes", [])
        headline = notes[0]["headline"] if notes else ""
        
        region = None
        for r in ["East", "West", "South", "Midwest"]:
            if r in headline:
                region = r
                break
        is_first_four = "First Four" in headline
        
        for competitor in comp["competitors"]:
            td = competitor["team"]
            team_id = td["id"]
            abbrev = td["abbreviation"]
            location = td.get("location", "")
            seed = competitor.get("curatedRank", {}).get("current", 0)
            
            # Try to get record from records array
            record = ""
            for rec in competitor.get("records", []):
                if rec.get("type") == "total":
                    record = rec.get("summary", "")
                    break
            
            if abbrev == "TBD":
                continue
                
            key = abbrev
            if key not in all_teams:
                all_teams[key] = {
                    "team_id": team_id,
                    "abbrev": abbrev,
                    "location": location,
                    "seed": seed,
                    "region": region,
                    "is_first_four": is_first_four,
                    "record": record,
                }
            elif record and not all_teams[key]["record"]:
                all_teams[key]["record"] = record

# For teams without records, fetch from team API
for key, team in all_teams.items():
    if not team["record"]:
        tid = team["team_id"]
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{tid}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp:
                tdata = json.loads(resp.read().decode())
            
            # Extract record
            team_info = tdata.get("team", {})
            record_items = team_info.get("record", {}).get("items", [])
            for ri in record_items:
                if ri.get("type") == "total":
                    team["record"] = ri.get("summary", "")
                    break
            time.sleep(0.1)  # Be polite
        except Exception as e:
            print(f"  Error fetching {key}: {e}")

# Print results
print("Team Name,Region,Seed,Record,FirstFour,ESPN_Location")
for key in sorted(all_teams.keys(), key=lambda k: (all_teams[k]["region"] or "ZZ", all_teams[k]["seed"])):
    t = all_teams[key]
    print(f"{t['location']},{t['region']},{t['seed']},{t['record']},{t['is_first_four']},{t['location']}")

# Also save as JSON
with open("scripts/bracket_2026_teams.json", "w") as f:
    json.dump(all_teams, f, indent=2)
print(f"\nSaved to scripts/bracket_2026_teams.json")
