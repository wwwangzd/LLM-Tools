# LLM Tools

A personal workspace for daily LLM prompts, Codex skills, agent instructions, and model migration utilities.

Chinese version: [README.zh-CN.md](README.zh-CN.md)

## Directory Overview
- `codex/`: Codex-specific configuration, skills, and tool references.
  - `AGENTS.md`: Project-level Codex instructions, including Chinese response defaults, low-intrusion fix principles, tool capability notes, and local runtime selection rules.
  - `skills/`
    - `ai-daily-brief/`: Generates concise Chinese AI daily briefs from recent X/community discussions, official AI company updates, model releases, and technical blogs.
    - `git-safe-commit/`: Reviews Git changes for sensitive information and creates a conventional commit after the review passes.
    - `project-onboarding-guide/`: Summarizes a repository based on real project files, including project overview, key directory responsibilities, and run workflow.
  - `tools/`
    - `lark-cli.md`: Lark CLI installation and integration reference.
- `model-move/`: Utilities for migrating x86 + CUDA model services to ARM + Ascend NPU environments.
  - `prompts/`
    - `migrate-project-summary.prompt.md`: Analyzes a model service project structure, key file responsibilities, and service startup order.
    - `plan-npuMigrationCheck.prompt.md`: Checks whether a project is suitable for migration to OpenEuler + Ascend NPU based on its directory structure.
  - `skills/`
    - `torch-cuda-to-euler-npu-migration/`: Generates Dockerfile and requirements.txt outputs for OpenEuler + Ascend NPU migration based on project summaries and runtime details.
- `prompts/`: General-purpose prompts.
  - `smol-ai-ai.prompt.md`: Prompt for reading the latest smol.ai AI news and summarizing it in Simplified Chinese.
- `skills/`: Reserved for general-purpose skills. Currently empty.
