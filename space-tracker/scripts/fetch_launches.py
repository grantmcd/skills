#!/usr/bin/env python3
import json
import os
import urllib.request
import argparse
import sys
from datetime import datetime, timedelta

# Adjust path to import shared utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.utils import get_dist_dir

# Paths
SKILL_NAME = "space-tracker"
DIST_DIR = get_dist_dir(SKILL_NAME)
CACHE_FILE = os.path.join(DIST_DIR, "launches_cache.json")
CACHE_EXPIRY_MINUTES = 60
API_URL = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=50&mode=detailed"

def fetch_launches(agency_filter=None, search_filter=None):
    # Check cache
    data = None
    if os.path.exists(CACHE_FILE):
        file_mtime = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        if datetime.now() - file_mtime < timedelta(minutes=CACHE_EXPIRY_MINUTES):
            with open(CACHE_FILE, "r") as f:
                data = json.load(f)

    if not data:
        # Fetch fresh data
        try:
            headers = {"User-Agent": "Space-Tracker-Skill/1.0"}
            req = urllib.request.Request(API_URL, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                # Filter for future launches only (plus 2 hours for "Now" window)
                now_iso = (datetime.utcnow() - timedelta(hours=2)).isoformat() + "Z"
                if data.get("results"):
                    data["results"] = [l for l in data["results"] if l.get("net", "") > now_iso]

                with open(CACHE_FILE, "w") as f:
                    json.dump(data, f, indent=4)
        except Exception as e:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r") as f:
                    data = json.load(f)
            else:
                data = {"results": []}

    # Apply filters locally
    results = data.get("results", [])
    if agency_filter:
        results = [l for l in results if agency_filter.lower() in l.get("launch_service_provider", {}).get("name", "").lower()]
    if search_filter:
        results = [l for l in results if search_filter.lower() in l.get("name", "").lower() or search_filter.lower() in l.get("mission", {}).get("description", "").lower()]

    return {"results": results}

def format_cli_summary(launch):
    name = launch.get("name", "Unknown Mission")
    net = launch.get("net", "TBD")
    agency = launch.get("launch_service_provider", {}).get("name", "Unknown Agency")
    rocket = launch.get("rocket", {}).get("configuration", {}).get("full_name", "Unknown Rocket")
    status = launch.get("status", {}).get("name", "TBD")
    mission = launch.get("mission") or {}
    description = mission.get("description", "No details available.")
    
    # ANSI Colors
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    END = "\033[0m"
    
    output = []
    output.append(f"{BOLD}{BLUE}🚀 NEXT SPACE MISSION: {name}{END}")
    output.append(f"{BOLD}📅 Scheduled for:{END} {net}")
    output.append(f"{BOLD}🏢 Agency:       {END} {agency}")
    output.append(f"{BOLD}🚀 Vehicle:      {END} {rocket}")
    output.append(f"{BOLD}📊 Status:       {END} {GREEN if 'Go' in status else YELLOW}{status}{END}")
    output.append(f"\n{description[:300]}...")
    
    vid = launch.get("vidURLs", [])
    if vid:
        output.append(f"\n{BOLD}📺 WATCH LIVE:{END} {vid[0].get('url')}")
    
    return "\n".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch upcoming space launches.")
    parser.add_argument("--agency", help="Filter by agency name")
    parser.add_argument("--search", help="Search in mission name or description")
    args = parser.parse_args()

    launches = fetch_launches(agency_filter=args.agency, search_filter=args.search)
    if launches.get("results"):
        print(format_cli_summary(launches["results"][0]))
        print(f"\n{'-'*40}")
        print(f"Total upcoming missions tracked: {len(launches['results'])}")
    else:
        print(f"No upcoming launches found matching your criteria.")
