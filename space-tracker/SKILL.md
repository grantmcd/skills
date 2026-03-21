---
name: space-tracker
description: "Use this skill to track global space launch schedules and real-time mission telemetry. Activate whenever the user asks about upcoming rocket launches, SpaceX missions, NASA schedules, or wants to watch a live space stream, even if they don't explicitly mention 'Launch Library' or 'telemetry'. Provides live countdowns, pad maps, and booster flight history."
license: MIT
compatibility: Requires Python 3.8+, network access to ll.thespacedevs.com, and a modern web browser for the dashboard.
---

## Triggers
- "When is the next space launch?"
- "Show me the space launch schedule."
- "What's happening in space this week?"
- "Track the next SpaceX mission."

## Instructions
1. **Fetch Data:** When triggered, run the `scripts/fetch_launches.py` script. Pass `--agency` (e.g., "SpaceX") or `--search` (e.g., "Crew-7") if the user specifies a particular mission or provider.
2. **Mandate: CLI-First Reporting:** ALWAYS provide a high-signal text summary directly in the CLI (Launch Name, Time, Agency, Vehicle, Status, and Live Stream link) *before* or *alongside* the UI preview.
3. **Mandate: Date Filtering:** The `fetch_launches.py` script MUST filter results to only include future missions (NET > now). Never show "stale" data in the UI or CLI.
4. **Mandate: Defensive Parsing:** When parsing the complex LL2 API, ALWAYS use defensive dictionary access (`.get()` with defaults) to prevent crashes on missing optional fields (e.g., `vidURLs`, `launcher_stage`).
5. **Handle Rate Limits:** The script includes built-in caching (60 minutes) to respect the API's 15 requests per hour limit.
6. **Generate Review:** Once data is fetched, run the `scripts/generate_review.py` script with the same `--agency` or `--search` arguments to prepare the filtered JSON payload and update the dashboard.
7. **Display UI:** Open the `ui/viewer.html` file (generated from `ui/viewer.template.html`) to show the user a visual dashboard of the specific launches they requested.

## Available Resources
- `space-tracker/scripts/fetch_launches.py`: Python script to fetch, filter, and cache launch data with CLI-first output.
- `space-tracker/scripts/generate_review.py`: Python script to format data for the Review UI with defensive parsing.
- `space-tracker/ui/viewer.html`: High-fidelity dashboard for visualizing upcoming launches.

## Review UI
- `space-tracker/ui/viewer.html`
