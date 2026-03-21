#!/usr/bin/env python3
import json
import os
import urllib.request
import argparse
from datetime import datetime, timedelta

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(SCRIPT_DIR, '..', 'dist')
os.makedirs(DIST_DIR, exist_ok=True)

CACHE_FILE = os.path.join(DIST_DIR, "launches_cache.json")
CACHE_EXPIRY_MINUTES = 60
API_URL = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=50&mode=detailed"
def fetch_launches():
    # Check cache
    if os.path.exists(CACHE_FILE):
        file_mtime = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        if datetime.now() - file_mtime < timedelta(minutes=CACHE_EXPIRY_MINUTES):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)

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
            return data
    except Exception as e:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return {"results": []}

def format_cli_summary(launch):
    name = launch.get("name", "Unknown Mission")
    net = launch.get("net", "TBD")
    agency = launch.get("launch_service_provider", {}).get("name", "Unknown Agency")
    rocket = launch.get("rocket", {}).get("configuration", {}).get("full_name", "Unknown Rocket")
    status = launch.get("status", {}).get("name", "TBD")
    description = launch.get("mission", {}).get("description", "No details available.")
    
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
    output.append(f"\n{description[:200]}...")
    
    vid = launch.get("vidURLs", [])
    if vid:
        output.append(f"\n{BOLD}📺 WATCH LIVE:{END} {vid[0].get('url')}")
    
    return "\n".join(output)

if __name__ == "__main__":
    launches = fetch_launches()
    if launches.get("results"):
        print(format_cli_summary(launches["results"][0]))
        print(f"\n{'-'*40}")
        print(f"Total upcoming missions tracked: {len(launches['results'])}")
    else:
        print("No upcoming launches found.")
