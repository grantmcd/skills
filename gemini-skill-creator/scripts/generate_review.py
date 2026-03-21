import json
import os
import sys


def generate_review(workspace_dir, output_file):
    # This is a simplified version of the review generator
    # In a real scenario, it would use Jinja2 to render the template
    # Here we'll do a basic string replacement for portability

    benchmark_path = os.path.join(workspace_dir, "benchmark.json")
    if not os.path.exists(benchmark_path):
        print(f"Error: {benchmark_path} not found.")
        return

    with open(benchmark_path, "r") as f:
        benchmark = json.load(f)

    # Load template
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "viewer.html")
    with open(template_path, "r") as f:
        template = f.read()

    # Basic metadata replacement
    html = template.replace("{{skill_name}}", benchmark.get("skill_name", "Unknown"))
    html = html.replace("{{iteration}}", str(benchmark.get("iteration", 1)))

    with_skill_results = next(
        (r for r in benchmark["results"] if r["config_name"] == "with_skill"), {}
    )
    html = html.replace(
        "{{pass_rate}}", str(int(with_skill_results.get("pass_rate", 0) * 100))
    )

    # For a static generator without Jinja2, we'd need more complex logic to handle loops
    # For now, let's just write the HTML and note it's a prototype
    # In a real implementation, the agent would use a more robust templating approach

    with open(output_file, "w") as f:
        f.write(html)

    print(f"Successfully generated review at {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_review.py <workspace_dir> <output_file>")
    else:
        generate_review(sys.argv[1], sys.argv[2])
