import json
import os
import sys


def capture_friction(skill_name, friction_description, session_snippet):
    # This script would normally call an LLM to analyze the friction
    # For now, it will create a template for an evaluation test case

    eval_path = os.path.join(skill_name, "evals", "evals.json")
    if not os.path.exists(eval_path):
        os.makedirs(os.path.dirname(eval_path), exist_ok=True)
        evals_data = {"skill_name": skill_name, "evals": []}
    else:
        with open(eval_path, "r") as f:
            evals_data = json.load(f)

    new_id = len(evals_data["evals"]) + 1
    new_eval = {
        "id": new_id,
        "name": f"Friction: {friction_description[:30]}...",
        "prompt": f"I had an issue with {skill_name}: {friction_description}. Here's the context: {session_snippet}",
        "assertions": [
            "Identifies the root cause of the friction",
            "Proposes a specific refinement to the SKILL.md",
            "Addresses the provided context specifically",
        ],
    }

    evals_data["evals"].append(new_eval)

    with open(eval_path, "w") as f:
        json.dump(evals_data, f, indent=2)

    print(f"Captured new friction eval for {skill_name} (ID: {new_id})")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python capture_friction.py <skill_name> <friction_description> <session_snippet>"
        )
    else:
        capture_friction(sys.argv[1], sys.argv[2], sys.argv[3])
