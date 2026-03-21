#!/usr/bin/env python3
import json
import os
import sys
import datetime

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, "scripts", "launches_cache.json")
OUTPUT_PATH = os.path.join(ROOT_DIR, "ui", "review_data.json")

def generate_review_data():
    if not os.path.exists(DATA_PATH):
        print("No launch data found. Fetch data first.")
        sys.exit(1)

    with open(DATA_PATH, "r") as f:
        raw_data = json.load(f)

    launches = []
    for launch in raw_data.get("results", []):
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
        "title": "Upcoming Global Space Launches",
        "timestamp": datetime.datetime.now().isoformat(),
        "launches": launches
    }

    # Write review data
    with open(OUTPUT_PATH, "w") as f:
        json.dump(review_data, f, indent=4)
    
    # Embed into viewer.html for self-contained usage
    template_path = os.path.join(ROOT_DIR, "ui", "viewer.html")
    # Need a fresh template to replace {{DATA}}
    # For now, we'll just rewrite the file based on our previous template
    # but with the real data injected.
    
    print(f"Review data generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_review_data()
