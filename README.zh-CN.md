# README

日常和通用的 prompt、skills、Agent 相关工具整理区。

英文版：[README.md](README.md)

## 目录
- `codex/`：Codex 相关配置、专用 skills 与自动化任务 prompt。
  - `AGENTS.md`：Codex 在本项目内工作的基础约束，包含中文输出、低侵入修复、本地运行依赖选择等规则。
  - `automations/`
    - `smol-ai-ai.prompt.md`：每日读取 smol.ai 最新 AI 新闻并整理为中文推送的 automation prompt。
  - `skills/`
    - `git-safe-commit/`：审查当前 Git 改动的敏感信息风险，并在通过后生成规范 commit message 完成提交。
    - `project-onboarding-guide/`：基于仓库真实文件梳理项目概览、关键目录职责与运行流程。
- `model-move/`：x86 + CUDA 模型迁移到 ARM + 昇腾 NPU 的工具。
  - `prompts/`
    - `migrate-project-summary.prompt.md`：分析模型服务项目结构、关键文件职责与服务运行顺序。
    - `plan-npuMigrationCheck.prompt.md`：根据目录结构判断项目是否具备 OpenEuler + Ascend NPU 迁移条件。
  - `skills/`
    - `torch-cuda-to-euler-npu-migration/`：基于项目摘要和运行环境信息生成面向 OpenEuler + Ascend NPU 的 Dockerfile 与 requirements.txt。
- `prompts/`：通用 prompts 预留目录，当前暂无内容。
- `skills/`：通用 skills 预留目录，当前暂无内容。
