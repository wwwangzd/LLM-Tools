# LLM Tools

A personal workspace for daily LLM prompts, Codex skills, agent rules, tool references, and model migration utilities.

Chinese version: [README.zh-CN.md](README.zh-CN.md)

## Directory Overview
- `rule/`: Agent rules and project-level operating instructions.
  - `AGENTS.md`: Shared AGENTS instructions, including Chinese response defaults, low-intrusion fix principles, Lark tool guidance, and local runtime selection rules.
- `skills/`: General Codex skills.
  - `ai-daily-brief/`: Generates concise Chinese AI daily briefs from recent X/community discussions, official AI company updates, model releases, and technical blogs.
  - `brainstorm/`: Builds a map of possibilities for open-ended ideas before narrowing into a direction.
  - `git-safe-commit/`: Reviews Git changes for sensitive information and creates a conventional commit after the review passes.
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
