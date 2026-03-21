import base64
import json
import os
import sys


def generate_review(results_path, template_path, output_file):
    if not os.path.exists(results_path):
        print(f"Error: {results_path} not found.")
        return

    with open(results_path, "r") as f:
        results_data = json.load(f)

    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        return

    with open(template_path, "r") as f:
        template = f.read()

    # Inject the results data as a base64 encoded string to avoid escaping issues
    results_json = json.dumps(results_data)
    results_base64 = base64.b64encode(results_json.encode("utf-8")).decode("utf-8")

    html = template.replace(
        "const RESULTS_DATA_BASE64 = '';",
        f"const RESULTS_DATA_BASE64 = '{results_base64}';",
    )

    # Inject secure session token
    token_path = os.path.join(os.path.dirname(__file__), "session_token.txt")
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            token = f.read().strip()
            html = html.replace(
                "const SESSION_TOKEN = '';", f"const SESSION_TOKEN = '{token}';"
            )

    with open(output_file, "w") as f:
        f.write(html)

    print(f"Successfully generated interactive review at {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python generate_review.py <results_json> <viewer_html_template> <output_file>"
        )
    else:
        generate_review(sys.argv[1], sys.argv[2], sys.argv[3])
