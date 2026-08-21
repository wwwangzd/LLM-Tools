---
name: maintain-workspace-context
description: 维护多仓库工作区的协作空间，生成或更新工作区级 AGENTS.md、CONTEXT.md 和 docs。
---

# 维护多仓库工作区上下文

创建或更新文档前，读取 [references/structures.md](references/structures.md)，并结合现有文件调整，不强制套用模板。

## 1. 收集工作区信息

- 读取用户输入以及已有的根 `AGENTS.md`、`CONTEXT.md` 和 `docs/`。
- 识别工作区内的 Git 仓库，检查各仓库的 README、根级协作规范、主要配置和文档入口。
- 查找仓库内其他 `AGENTS.md`，记录相对路径和适用范围。
- 修改前检查相关仓库的 Git 状态，保留已有改动。

只收集完成本次文档维护所需的信息；缺少依据的内容标记为待确认。

## 2. 更新工作区文档

### AGENTS.md

按参考结构维护：

- 工作区定位和 `CONTEXT.md` 入口；
- 工作前必读事项；
- 基于用户输入和各仓库规范整理的工作区协作规则；
- 工作区及各仓库 `AGENTS.md` 的快速索引；
- 工作区级完成标准。

仓库专属规则保留在对应仓库中，根文件只汇总跨仓库规则和检索入口。

### CONTEXT.md

按参考结构维护：

- 仓库清单和职责；
- 仓库间协作关系与边界；
- 按任务组织的关键入口；
- 各仓库常用验证命令。

### docs

按实际内容沉淀需求、设计和实现文档，并维护 `docs/README.md` 索引。沿用已有目录结构；新建时参考 `requirements/`、`designs/` 和 `implementation/` 分类。

## 3. 检查结果

- 检查文档中的仓库路径、命令和相对链接。
- 检查 `AGENTS.md`、`CONTEXT.md` 与 `docs` 的内容是否一致。
- 更新失效内容，保留无关的已有内容。
- 汇报更新内容、验证结果和待确认事项。
