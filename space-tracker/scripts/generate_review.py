#!/usr/bin/env python3
import json
import os
import sys
import datetime
import argparse

# Adjust path to import shared utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.utils import get_dist_dir

# Paths
SKILL_NAME = "space-tracker"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = get_dist_dir(SKILL_NAME)

DATA_PATH = os.path.join(DIST_DIR, "launches_cache.json")
OUTPUT_PATH = os.path.join(DIST_DIR, "review_data.json")
TEMPLATE_PATH = os.path.join(ROOT_DIR, "ui", "viewer.template.html")
FINAL_HTML_PATH = os.path.join(DIST_DIR, "viewer.html")

def generate_review_data(agency_filter=None, search_filter=None):
    if not os.path.exists(DATA_PATH):
        print("No launch data found. Fetch data first.")
        sys.exit(1)

    with open(DATA_PATH, "r") as f:
        raw_data = json.load(f)

    # Apply filters
    results = raw_data.get("results", [])
    if agency_filter:
        results = [l for l in results if agency_filter.lower() in l.get("launch_service_provider", {}).get("name", "").lower()]
    if search_filter:
        results = [l for l in results if search_filter.lower() in l.get("name", "").lower() or search_filter.lower() in l.get("mission", {}).get("description", "").lower()]

    launches = []
    for launch in results:
        rocket_data = launch.get("rocket", {})
        launcher_stages = rocket_data.get("launcher_stage", [])
        is_reused = False
        if launcher_stages and len(launcher_stages) > 0:
            launcher = launcher_stages[0].get("launcher")
            if launcher:
                is_reused = launcher.get("flight_proven", False)

        launches.append({
            "id": launch.get("id"),
            "name": launch.get("name"),
            "status": launch.get("status", {}),
            "net": launch.get("net"),
            "window_start": launch.get("window_start"),
            "window_end": launch.get("window_end"),
            "lsp_name": launch.get("launch_service_provider", {}).get("name"),
            "rocket_name": rocket_data.get("configuration", {}).get("full_name"),
            "mission_name": launch.get("mission", {}).get("name") if launch.get("mission") else "Unknown",
            "mission_description": launch.get("mission", {}).get("description") if launch.get("mission") else "No mission details available.",
            "pad_name": launch.get("pad", {}).get("name"),
            "location_name": launch.get("pad", {}).get("location", {}).get("name"),
            "latitude": launch.get("pad", {}).get("latitude"),
            "longitude": launch.get("pad", {}).get("longitude"),
            "image": launch.get("image"),
            "video_url": launch.get("vidURLs", [{}])[0].get("url") if launch.get("vidURLs") else None,
            "is_reused": is_reused
        })

    review_data = {
        "title": f"Upcoming {'SpaceX ' if agency_filter and 'spacex' in agency_filter.lower() else ''}Space Launches",
        "timestamp": datetime.datetime.now().isoformat(),
        "launches": launches
    }

    # Write review data JSON
    with open(OUTPUT_PATH, "w") as f:
        json.dump(review_data, f, indent=4)
    
    # Inject into viewer.html
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r") as f:
            template = f.read()
        
        # Replace the placeholder with the JSON string
        final_html = template.replace("{{DATA}}", json.dumps(review_data, indent=4))
        
        with open(FINAL_HTML_PATH, "w") as f:
            f.write(final_html)
        print(f"Final dashboard generated at {FINAL_HTML_PATH}")
    else:
        print(f"Warning: Template not found at {TEMPLATE_PATH}")

    print(f"Review data generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate review data for the Space Tracker UI.")
    parser.add_argument("--agency", help="Filter by agency name")
    parser.add_argument("--search", help="Search in mission name or description")
    args = parser.parse_args()
    
    generate_review_data(agency_filter=args.agency, search_filter=args.search)
