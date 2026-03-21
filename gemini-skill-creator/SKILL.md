# gemini-skill-creator

A skill for designing, testing, and refining specialized skills for the Gemini CLI.

## Triggering
Use this whenever the user wants to "create a skill", "automate a workflow", or "improve an existing capability". 

## Workflow for Gemini
1. **Research Patterns**: Use `grep_search` and `codebase_investigator` to find existing architectural patterns in the user's project.
2. **Draft SKILL.md**: Use the imperative mood. Focus on Gemini's specific tools:
    - Use `generalist` for background/batch tasks.
    - Use `mcp_context7` for library documentation.
    - Use `google_web_search` for external research.
3. **Validation Strategy**: Instead of "baselines", focus on "Direct Verification". Use the `generalist` tool to run the new skill against 2-3 specific scenarios and verify the file outputs directly.
4. **Safety & Privacy**: ALWAYS include instructions to avoid hardcoding secrets and to prefer environment variables or Kubernetes Secrets.

## Skill Structure
```
skill-name/
├── SKILL.md          # Core instructions and triggers
├── README.md         # Public documentation for the agent-skills repo
├── examples/         # Sample inputs/outputs
└── scripts/          # (Optional) Helper scripts the agent can call
```
