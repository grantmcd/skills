---
name: gemini-skill-creator
description: "A meta-skill for designing, testing, and objectively evaluating high-quality specialized skills for the Gemini CLI and other AI agents. Make sure to use this skill whenever the user mentions 'creating a skill', 'automating a workflow', or 'improving an agent capability', even if they don't explicitly ask for an 'evaluation' or 'review UI'."
---

# gemini-skill-creator

A meta-skill for designing, testing, and objectively evaluating high-quality specialized skills for the Gemini CLI and other AI agents.

## Core Mandate
This skill's purpose is to move beyond "vibe-based" skill creation. It enforces a rigorous cycle of:
1.  **Intent Capture**: Understanding the precise goal and target audience.
2.  **Pattern Discovery**: Researching existing codebase conventions or external best practices.
3.  **Iterative Testing**: Running the skill against diverse, realistic prompts in parallel.
4.  **Objective Evaluation**: Using automated grading and human-in-the-loop review via a specialized UI.

---

## 1. Intent & Research
When a user wants to build a skill, don't just draft it. First, define:
- **Success Criteria**: What specifically makes an output "correct"?
- **Triggers**: When exactly should this skill be activated (and when should it *not* be)?
- **Patterns**: Use `codebase_investigator` to find local architectural styles or `google_web_search` for external standards.

## 2. Drafting the SKILL.md
Follow these principles:
- **Imperative Instructions**: Use clear, direct commands.
- **The "Why"**: Explain the reasoning behind instructions to improve agent compliance.
- **Tool-Specific Guidance**: Explicitly mention how to use Gemini-native tools like `generalist`, `google_web_search`, and `mcp_context7`.
- **Safety**: Never hardcode secrets; prioritize standard configuration files (like `.env`) or secure stores.

## 3. Evaluation Framework
Every skill must be tested before being considered "ready."
1.  **Define Evals**: Create `evals/evals.json` with 3-5 diverse test prompts.
2.  **Parallel Execution**: Use the `generalist` sub-agent to run these prompts in parallel:
    - **Run A**: With the new skill enabled.
    - **Run B (Baseline)**: Without the skill (if applicable).
3.  **Capture Timing/Tokens**: Record the execution time and token usage for performance analysis.
4.  **Automated Grading**: Write a script or use a grader sub-agent to check outputs against specific assertions.

## 4. The Review UI
To evaluate results objectively, generate a static HTML review page.
- **Output Comparison**: Show the prompt, the generated files, and the pass/fail status of assertions.
- **User Feedback**: Provide a mechanism for the user to leave qualitative feedback on each test case.
- **Generation Logic**: Use the `assets/generate_review.py` script to transform the test results into a standalone `review.html`.

## 5. Optimization & Packaging
- **Description Tuning**: Optimize the `description` in frontmatter to ensure accurate triggering.
- **Packaging**: Once finalized, create a `.skill` package if the platform supports it.

## 6. Publishing to skills.sh
To ensure skills are discoverable and compatible with the broader agent ecosystem:
- **Repository Structure**: Each skill MUST be in its own directory at the root of the repository (e.g., `my-repo/my-skill/SKILL.md`).
- **Naming**: Directory names and the `name` field in frontmatter MUST be lowercase, using only letters, numbers, and hyphens (e.g., `data-extractor`).
- **Discoverability**: The `description` is the primary metadata for `skills.sh`. Ensure it contains clear keywords and scenarios.
- **Publication**: Once the repository is public on GitHub, it can be shared via `npx skills add <username>/<repo-name>`.

---

## Reporting & Feedback
ALWAYS provide a summary of the evaluation results:
- **Pass Rate**: % of assertions that passed.
- **Efficiency**: Token usage vs. baseline.
- **Recommendations**: Specific areas where the skill instructions need sharpening.
