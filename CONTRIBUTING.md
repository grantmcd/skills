# Contributing to Agent Skills

We welcome community contributions! This repository is focused on maintaining high-quality, objectively evaluated skills for AI agents.

## 🤝 Getting Started

To contribute a new skill or improve an existing one, please follow these guidelines:

### 1. Repository Structure
Each skill MUST be contained within its own directory at the root of the repository (e.g., `my-new-skill/`).

### 2. Skill Definition (`SKILL.md`)
Every skill must include a `SKILL.md` file with valid YAML frontmatter:
- **`name`**: Lowercase, letters, numbers, and hyphens only (e.g., `code-reviewer`).
- **`description`**: A concise, keyword-rich summary for agent discovery.

### 3. Development Workflow
We strongly recommend using the meta-skills in this repository during development:
1.  **[Skill Creator](./gemini-skill-creator)**: Use this to draft your skill and define your success criteria.
2.  **Evaluation**: Create temporary `evals/evals.json` files within an isolated sandbox to verify your skill's efficacy.
3.  **Refinement**: Use the **[Skill Evolver](./skill-evolver)** to address any friction points identified during testing.

### 4. Cleanup & Submission
Before submitting your contribution:
- **Run Quality Checks**: Ensure your code passes the unified quality gate:
  ```bash
  npm test
  ```
- **Remove Temporary Artifacts**: **Do NOT commit `evals/`, `results.json`, or `review.html` files.** These are temporary artifacts used during the development lifecycle. The final submission should only include the refined `SKILL.md` and any essential supporting scripts.

## ⚖️ Code Quality Standards
- **Python**: All scripts must be formatted and linted by [Ruff](https://github.com/astral-sh/ruff).
- **UI/HTML**: All viewer files must be formatted by [Prettier](https://prettier.io).

Thank you for helping us build better agent capabilities!
