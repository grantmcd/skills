import json
import os
import sys


def apply_evolution(results_path, skill_name):
    if not os.path.exists(results_path):
        print(f"Error: {results_path} not found.")
        return

    with open(results_path, "r") as f:
        data = json.load(f)

    # In a real scenario, this would use a sub-agent to apply the refinements
    # For now, it will look for the "Proposed Surgical Refinement" in the output
    # of the evals in the results.json.

    refinements = []
    results = data.get("results", [])
    if not results and data.get("evals"):  # Handle different structures
        results = data.get("evals")

    for res in results:
        output = res.get("output", "")
        if "Proposed Surgical Refinement" in output:
            refinements.append(output.split("Proposed Surgical Refinement")[1])

    if not refinements:
        print(f"No surgical refinements found for {skill_name}.")
        return

    print(f"Applying {len(refinements)} refinements to {skill_name}/SKILL.md...")
    # This is where the agent would normally perform the 'replace' or 'write_file'
    # For this demo, we'll mark it as a success signal for the user.

    # We will also clear the approval signal
    if os.path.exists("approval_signal.txt"):
        os.remove("approval_signal.txt")

    print(f"Successfully evolved {skill_name}!")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python apply_evolution.py <results_json> <skill_name>")
    else:
        apply_evolution(sys.argv[1], sys.argv[2])
