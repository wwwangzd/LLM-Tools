---
name: torch-cuda-to-euler-npu-migration
description: '将模型服务从 torch+CUDA 迁移到 OpenEuler+Ascend NPU。适用于需要基于项目摘要、运行环境信息、内置Dockerfile样例，自动生成当前项目 Dockerfile 与 requirements.txt 的场景。'
argument-hint: '提供项目摘要结果（含执行顺序）和原运行环境信息，生成 Dockerfile 与 requirements.txt。'
user-invocable: true
---

# Torch+CUDA 到 Euler+Ascend NPU 迁移构建技能

## 适用场景
- 已有模型服务项目，当前依赖 `torch+cuda` 或历史 GPU 运行方式。
- 目标运行环境是 `OpenEuler + Ascend CANN + torch-npu`。
- 需要在分析项目后，生成可直接用于构建的 `Dockerfile` 和 `requirements.txt`。

## 输入要求
至少提供以下输入：
- 已完成的项目摘要结果（包含项目定位、关键文件作用、执行顺序）。
- 原运行环境信息（例如驱动、框架版本、容器运行时、并发控制环境变量）。

调用前提：
- 本技能默认你已通过上游 prompt 得到“项目内容与执行顺序”总结。
- 若缺少摘要结果，技能先提示补齐必要摘要信息，再继续生成。

## 输出目标
在当前项目根目录生成或更新：
- `Dockerfile`
- `requirements.txt`

并给出：
- 迁移假设清单（哪些是事实、哪些是推断）。
- 服务运行顺序（若无法完全确认，标注“推断顺序”）。
- 关键环境变量和容器运行参数建议。

## 执行流程
1. 盘点项目和运行方式
- 识别入口：`run.sh`、`app.py`、`main.py`、`gunicorn`、`flask` 等。
- 收集容器运行参数：端口、并发环境变量等。

2. 形成迁移摘要（事实/推断/未知）
- 事实：文件中明确写出的依赖、命令、镜像、端口。
- 推断：根据已有运行命令得出的建议启动顺序或资源配置。
- 未知：缺少版本固定、入口不明确、缺少 requirements 时逐项标注。

3. 生成 `requirements.txt`
- 从现有依赖清单抽取 Python 包，优先保留业务依赖。
- 优先纳入 CANN 运行基础依赖。
- 去除 CUDA 专属包（如仅 NVIDIA 可用的依赖项），替换为 NPU 兼容方案。
- `torch-npu` 默认不写入 `requirements.txt`，由 `Dockerfile` 单独安装。

4. 生成 `Dockerfile`
- 基于 Ascend OpenEuler 镜像（例如 CANN 对应基础镜像）。
- 设置时区、系统依赖、pip 镜像源（如用户环境要求）。
- 安装 Miniconda，并按给出或推测的 Python 版本创建 conda 环境。
- 复制并安装 `requirements.txt`，再单独安装 `torch-npu`。
- 复制项目代码与模型目录，保留启动命令和端口暴露。
- 若项目依赖 NPU 设备挂载，提醒在运行命令中配置 `--device` 与驱动挂载。

5. 校验与收敛
- 检查 Dockerfile 中 `COPY` 路径是否都存在。
- 检查端口、入口命令与项目运行脚本是否一致。
- 检查 requirements 是否包含明显冲突项（CUDA-only、x86-only 轮子）。

## 决策分支
- 缺少启动入口：
  - 优先从 `run.sh` 或 `gunicorn` 参数推断。
  - 无法确认时，输出候选入口并请求用户确认，不直接硬编码。

- 缺少依赖列表：
  - 从源码 `import` 和已有文档推断最小可运行依赖。
  - 在结果中标记“最小集推断”，并附补充建议。

- 样例 Dockerfile 与当前项目冲突：
  - 保留样例中的基础镜像、conda 环境创建和 NPU 关键设置。
  - 以当前项目实际入口、文件结构覆盖业务层 COPY 与 CMD。
  - 样例视为长期参考基线，来自技能内置模板。

## 完成标准
- 成功产出项目根目录 `Dockerfile` 与 `requirements.txt`。
- 文件内容与项目入口、端口、依赖一致，无明显路径错误。
- 明确列出事实/推断/未知，不将推断伪装成事实。

## 参考与模板
- 迁移检查清单：[migration-checklist](./references/migration-checklist.md)
- 输出模板：[dockerfile-and-requirements-template](./assets/dockerfile-and-requirements-template.md)
