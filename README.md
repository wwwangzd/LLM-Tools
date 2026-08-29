# LLM Tools

A personal workspace for daily LLM prompts, Codex skills, agent rules, tool references, and model migration utilities.

Chinese version: [README.zh-CN.md](README.zh-CN.md)

## Directory Overview
- `rule/`: Agent rules and project-level operating instructions.
  - `AGENTS.md`: Shared AGENTS instructions, including Chinese response defaults, low-intrusion fix principles, Lark tool guidance, and local runtime selection rules.
- `skills/`: General Codex skills.
  - `ai-daily-brief/`: Generates concise Chinese AI daily briefs from recent X/community discussions, official AI company updates, model releases, and technical blogs.
  - `project-onboarding-guide/`: Summarizes a repository based on real project files, including project overview, key directory responsibilities, and run workflow.
- `tools/`: Tool setup and usage references.
  - `lark-cli.md`: Lark CLI installation and integration reference.
- `prompts/`: General-purpose prompts.
  - `smol-ai-ai.prompt.md`: Prompt for reading the latest smol.ai AI news and summarizing it in Simplified Chinese.
- `model-move/`: Utilities for migrating x86 + CUDA model services to ARM + Ascend NPU environments.
  - `prompts/`
    - `migrate-project-summary.prompt.md`: Analyzes a model service project structure, key file responsibilities, and service startup order.
  - `skills/`
    - `torch-cuda-to-euler-npu-migration/`: Generates Dockerfile and requirements.txt outputs for OpenEuler + Ascend NPU migration based on project summaries and runtime details.
- `workspace-workflows/`: Codex skills for workspace collaboration and development automation flows.
  - `bootstrap-requirement-worktree/`: Records requirement source and PRD references, then creates isolated worktrees from the latest remote default branches.
  - `brainstorm/`: Builds a map of possibilities for open-ended ideas before narrowing into a direction.
  - `git-safe-commit/`: Reviews Git changes for sensitive information and creates a conventional commit after the review passes.
  - `issue-solve/`: Confirms, organizes, assesses, and resolves one or more issues according to project requirements.
  - `maintain-workspace-context/`: Maintains workspace-level collaboration rules, repository context, and shared documentation for multi-repository workspaces.
  - `systematic-debugging/`: Investigates the root cause of an individual technical issue and supports targeted fixes.
  - `test-driven-development/`: Guides feature and bug-fix work through the red-green-refactor cycle.
  - `verification-before-completion/`: Requires fresh, risk-appropriate verification before completion claims or commits.
