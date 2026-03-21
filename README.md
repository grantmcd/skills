# Agent Skills

A collection of specialized, high-quality, and objectively evaluated skills for AI agents. These skills follow the [Agent Skills](https://agentskills.io/) open standard managed by the [skills CLI](https://github.com/vercel-labs/skills) and are compatible with **Claude Code**, **GitHub Copilot**, **Gemini CLI**, **Kiro**, and other modern AI coding tools.

## 🛠 Core Meta-Skills

This repository features two powerful meta-skills designed to help you build and maintain your own agent capabilities:

- [**Skill Creator**](./gemini-skill-creator): A specialized skill for designing, testing, and objectively evaluating new agent capabilities. It enforces a rigorous cycle of intent capture, pattern discovery, and automated evaluation.
- [**Skill Evolver**](./skill-evolver): A proactive skill that reflects on task execution to surgically refine other skills through automated friction capture and secure human-in-the-loop review.

---

## 🚀 Installation

### 1. Universal Method (Recommended)
The easiest way to install these skills across all your agents simultaneously is using the [skills CLI](https://github.com/vercel-labs/skills):

```bash
# Interactively choose which skills to install from this repository
npx skills add https://github.com/grantmcd/skills

# OR explicitly install a specific skill directly
npx skills add https://github.com/grantmcd/skills --skill skill-evolver
```

### 2. Tool-Specific Usage

| Tool | Installation Path | Command / Prefix |
| :--- | :--- | :--- |
| **Claude Code** | `~/.config/claude-code/skills/` | `/` (e.g., `/create-skill`) |
| **GitHub Copilot** | `~/.copilot/skills/` | `/` (e.g., `/evolve-skill`) |
| **Gemini CLI** | `~/.gemini/skills/` | Auto-detected via frontmatter |
| **Kiro** | `~/.kiro/skills/` | Slash commands in panel |
| **OpenAI Codex** | `~/.codex/skills/` | `$` (e.g., `$create-skill`) |

---

## ✨ Why Agent Skills?

Agent skills are more than just system prompts. They are modular, testable, and refined capabilities that embody four key ideals:

1.  **Intuitiveness**: Designed with clear triggers and imperative instructions that agents follow reliably.
2.  **Objectivity**: Verified against real-world test cases with automated assertions and visual diffs.
3.  **Refined**: Surgically updated based on actual friction points and session history.
4.  **Secure**: Built with mandates for credential protection and authenticated human-in-the-loop approval.

---

## 🛠 Development & Quality

This repository uses a rigorous automated quality gate to ensure all skills and supporting scripts are production-ready.

- **Python Linting/Formatting**: Powered by [Ruff](https://github.com/astral-sh/ruff).
- **UI Formatting**: Powered by [Prettier](https://prettier.io).
- **CI/CD**: GitHub Actions runs a unified quality check on every push.

To run checks locally:
```bash
./check.sh
```

---

## 🤝 Contributing

We welcome community contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for details on how to add new skills or improve existing ones.

