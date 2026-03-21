# Agent Skills

A collection of specialized skills for the Gemini CLI and interactive agents.

## Contents
- [gemini-skill-creator](./gemini-skill-creator): A meta-skill for building new Gemini CLI capabilities.

## Usage
To use these skills, you can download the `.skill` file or clone this repository and point your agent to the local `SKILL.md`.

## Safety
These skills are designed to be "infrastructure-as-code" friendly and prioritize security by:
- Preferring Kubernetes Secrets over hardcoded credentials.
- Separating configuration from code.
- Using standardized MCP and CLI tools.
