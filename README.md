# Agent Skills

A collection of specialized, high-quality skills for the Gemini CLI and other AI agents.

## Core Skills
- [**gemini-skill-creator**](./gemini-skill-creator): A meta-skill for designing, testing, and objectively evaluating high-quality specialized skills.
- [**skill-evolver**](./skill-evolver): A proactive meta-skill that reflects on task execution to surgically refine other skills through automated friction capture and secure review.

## Why this Repository?
Agent skills should be more than just instructions. They should be:
- **Testable**: Verified against real-world prompts.
- **Performant**: Optimized for token usage and execution speed.
- **Collaborative**: Open for review and improvement by the community.

## How to use the Gemini Skill Creator
1.  **Draft**: Use the skill to capture intent and research patterns.
2.  **Evaluate**: Run parallel tests using the `generalist` tool.
3.  **Review**: Analyze the generated `review.html` to see how the skill performs against a baseline.
4.  **Refine**: Sharpen instructions based on objective feedback.

## Safety & Security
- **No Secrets**: We never commit API keys, passwords, or sensitive credentials.
- **Isolated Tests**: Evaluation runs are performed in isolated workspace directories.
- **Standardized Tools**: We prioritize the use of standard, well-documented CLI and MCP tools.
