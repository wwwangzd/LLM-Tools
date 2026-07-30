# README

日常和通用的 prompt、skills、Agent 规则、工具说明和模型迁移工具整理区。

英文版：[README.md](README.md)

## 目录
- `rule/`：Agent 规则与项目级工作约束。
  - `AGENTS.md`：共享 AGENTS 指令，包含中文输出、低侵入修复、飞书工具能力、本地运行依赖选择等规则。
- `skills/`：通用 Codex skills。
  - `ai-daily-brief/`：生成中文 AI 热点简报，汇总近两天 X/社区讨论、AI 公司官方更新、模型发布和技术博客。
  - `brainstorm/`：在开放性想法收敛前，先构建可选方向和影响分组的可能性地图。
  - `git-safe-commit/`：审查当前 Git 改动的敏感信息风险，并在通过后生成规范 commit message 完成提交。
  - `maintain-workspace-context/`：维护多仓库工作区的协作规范、仓库上下文和共享文档。
  - `project-onboarding-guide/`：基于仓库真实文件梳理项目概览、关键目录职责与运行流程。
  - `systematic-debugging/`：通过证据收集和根因追踪诊断 Bug 与异常行为。
  - `test-driven-development/`：使用红—绿—重构循环指导功能开发和 Bug 修复。
  - `verification-before-completion/`：在提交或声称完成前执行最新且与风险相称的验证。
- `tools/`：工具安装和使用说明。
  - `lark-cli.md`：飞书 / Lark CLI 安装与接入说明。
- `prompts/`：通用 prompts。
  - `smol-ai-ai.prompt.md`：每日读取 smol.ai 最新 AI 新闻并整理为中文推送的 prompt。
- `model-move/`：x86 + CUDA 模型迁移到 ARM + 昇腾 NPU 的工具。
  - `prompts/`
    - `migrate-project-summary.prompt.md`：分析模型服务项目结构、关键文件职责与服务运行顺序。
  - `skills/`
    - `torch-cuda-to-euler-npu-migration/`：基于项目摘要和运行环境信息生成面向 OpenEuler + Ascend NPU 的 Dockerfile 与 requirements.txt。
