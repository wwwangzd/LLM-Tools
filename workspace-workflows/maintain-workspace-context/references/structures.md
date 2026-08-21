# 工作区文档参考结构

按工作区实际情况裁剪，不要求保留所有章节。

## AGENTS.md

```markdown
# <工作区名称> — 协作规范

> 本目录是多仓库协作空间。仓库信息与检索入口见 [`CONTEXT.md`](CONTEXT.md)。

## 工作前必读

1. 先读 `CONTEXT.md`，再读取目标仓库的协作规范和相关文档。
2. 修改前进入目标仓库运行 `git status --short`。
3. 跨仓库变更同步检查相关仓库和文档。

## 协作规范

- `<repo-a>/`：<职责与协作边界>。
- `<repo-b>/`：<职责与协作边界>。
- <基于用户输入和仓库规范整理的跨仓库规则>。

## 协作规范索引

| 作用域 | 规范 |
| --- | --- |
| 工作区 | [`AGENTS.md`](AGENTS.md) |
| `<repo-a>/` | [`<repo-a>/AGENTS.md`](<repo-a>/AGENTS.md) |
| `<repo-b>/<module>/` | [`<repo-b>/<module>/AGENTS.md`](<repo-b>/<module>/AGENTS.md) |

## 完成标准

- 运行受影响仓库的必要验证。
- 保持代码、契约和文档一致。
- 说明未完成或待确认事项。
```

## CONTEXT.md

````markdown
# <工作区名称> — Context

本文件记录多仓库协作信息与检索入口。执行规则见 [`AGENTS.md`](AGENTS.md)。

## 仓库清单

| Path | Repo | 角色 |
| --- | --- | --- |
| `<repo-a>/` | `<repo-name-or-remote>` | <核心职责> |
| `<repo-b>/` | `<repo-name-or-remote>` | <核心职责> |

## 职责与协作关系

- `<repo-a>/` 负责 <内容>，向 <对象> 提供 <接口或产物>。
- `<repo-b>/` 负责 <内容>，依赖 <仓库或契约>。
- <关键依赖、数据流或契约边界>。

## 关键入口

| 任务 | 优先阅读 |
| --- | --- |
| <任务类型> | `<repo>/README.md`、`<repo>/docs/...` |
| <接口或契约> | `<repo>/path/to/contract` |
| <跨仓库主题> | `docs/<category>/<topic>.md` |

## 常用验证

`<repo-a>/`：

```bash
cd <repo-a>
<test-or-check-command>
```
````

## docs

新建文档体系时可参考：

```text
docs/
├── README.md
├── requirements/
├── designs/
└── implementation/
```

`docs/README.md`：

```markdown
# 工作区文档

| 主题 | 类型 | 状态 | 相关仓库 | 文档 |
| --- | --- | --- | --- | --- |
| <主题> | 需求 / 设计 / 实现 | 草案 / 已确认 / 已落地 / 归档 | `<repo-a>`、`<repo-b>` | [`<标题>`](<relative-path>) |
```

主题文档：

```markdown
# <主题>

- 状态：<状态>
- 相关仓库：`<repo-a>`、`<repo-b>`

## 背景与目标

## <需求、设计或实现>

## 验证与验收

## 待确认事项
```
