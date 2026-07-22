---
name: ai-daily-brief
description: "生成简洁的中文 AI 热点简报，汇总今天或最近两天来自 X/Twitter、AI 公司官方博客和新闻页、模型/社区发布渠道以及相关 AI 社区的热门事件。适用于用户询问今天的 AI 大新闻、AI 日报、AI 热点、AI 新闻、AI 社区/官方发布汇总或类似需求。"
---

# AI Daily Brief

## Overview

生成近 1-2 天 AI 热点简报。必须联网确认最新信息，并把 X/社区热点与官方发布分开梳理。

## Workflow

1. 确认时间窗口：默认按用户所在地的“今天”检索；可包含昨天的重要延续事件；不要纳入超过两个自然日的旧内容，除非仅作为一句背景说明。开头明确写出日期范围。
2. 读取渠道配置：使用前先阅读 `references/x-sources.md`、`references/official-sources.md` 和 `references/output-format.md`。渠道、账号、官网入口以后都从这些文件调整。
3. 联网检索：必须使用浏览/搜索工具确认最新信息，不要只凭记忆回答。优先检索直接来源，再用可信二级来源交叉验证。
4. 分层收集：
   - X/社区热点：抓取当天最热、最新颖、讨论度高的一手 AI 消息，不追求数量；热点很多时可适当扩展。
   - 官方发布/技术博客：逐一检查 OpenAI、Anthropic、Google、Qwen、DeepSeek、GLM/Z.ai、MiniMax 是否有当天或昨天的新公告、博客、模型发布、技术文章或开发者更新。
5. 筛选去重：保留模型/产品发布、研究进展、重要技术博客、开发者平台变化、重大安全/政策/产业事件。丢弃重复转述、无来源传闻、营销噪声和与 AI 关联弱的内容。
6. 输出中文简报：按 `references/output-format.md` 的结构呈现，内容精炼但保留关键点、影响和来源链接。

## Quality Bar

- 优先提供原始链接：官方博客、公告、论文、GitHub/Hugging Face release、X 原帖。
- 对只来自 X 的消息标注“未完全确认”或“社区热议”，并尽量找第二来源。
- 对没有新动态的官方社区，简短写“未发现近两天重要官方更新”，不要硬凑。
- 每条说明控制在 1-2 句，避免泛泛地说“引发关注”；说明具体发生了什么、为什么重要。
- 如搜索结果日期与用户“今天”存在时区差异，使用明确日期消除歧义。

## References

- `references/x-sources.md`：X/Twitter 与补充社区的搜索策略和候选来源。
- `references/official-sources.md`：官方社区、博客、公告、模型仓库和 release 入口。
- `references/output-format.md`：最终简报结构、条目格式和取舍规则。
