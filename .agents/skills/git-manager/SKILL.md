---
name: git_manager
description: Manage git operations like status, add, commit, and push for the project.
parameters:
  type: object
  properties:
    command:
      type: string
      enum: [status, diff, commit, push]
      description: The git command to execute.
    commit_message:
      type: string
      description: The commit message explaining the changes. Must strictly follow Conventional Commits format (e.g., 'feat: add text loader', 'fix: resolve bug in retriver'). Required if command is 'commit'.
    files:
      type: array
      items:
        type: string
      description: List of specific files to stage (used if command is 'commit').
    branch:
      type: string
      description: The branch to push to (required if command is 'push').
  required:
    - command
---

# Git Manager Skill

Provides an agent with the ability to safely check status, review diffs, commit specific files with descriptive messages, and push changes to the remote repository.

## Execution
This skill relies on the framework's internal registry loading the python script rather than being called as a standalone CLI tool. The internal script (`scripts/git_utils.py`) handles the secure execution of these subcommands.

## Best Practices
- Never commit `.env` or files containing secrets.
- Always check if `.gitignore` properly excludes `venv`, `__pycache__`, data folders (`datasets/`), and IDE configurations.
