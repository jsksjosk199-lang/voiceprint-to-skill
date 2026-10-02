# 第三方来源、改写范围与许可

**联系作者：微信 `ysy985221`｜邮箱 [2354724714@qq.com](mailto:2354724714@qq.com)。**

本项目作者有权授权的原创材料适用 [LICENSE](LICENSE)。第三方原有贡献仍适用其许可，本项目的自用限制不能取消上游已经授予的权利。

不以“换了语言”“重新编排”“没有逐字相同”为由声称所有材料独立原创或免除版权义务。对明显参考、改写或整理上游文档的部分，保留相应版权与许可。

## 核实的主要来源（2026-10-02）

| 上游 | 本项目涉及范围 | 已核实的许可与声明 |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) 的 writing-skills 与 persuasion-principles | SKILL.md 中按错误类型组织规则、指引与验收的部分；文档工程说明 | MIT，Copyright (c) 2025 Jesse Vincent；[许可原文](THIRD-PARTY-LICENSES/superpowers-MIT.txt) |
| [mattpocock/skills：writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) | references/agent-doc-writing.md 与 SKILL.md 中的文档分层、指针、完成条件等整理 | MIT，Copyright (c) 2026 Matt Pocock；[许可原文](THIRD-PARTY-LICENSES/mattpocock-skills-MIT.txt) |
| [Tribe AI brand-voice](https://github.com/anthropics/knowledge-work-plugins/tree/main/partner-built/brand-voice) | SKILL.md 中表达常量与场景语气的区分 | 该子目录使用 MIT，Copyright (c) 2025 Tribe AI；[许可原文](THIRD-PARTY-LICENSES/tribe-ai-brand-voice-MIT.txt) |

**改动说明：** 中文整理、针对语料蒸馏任务的重组与示例替换；本次公开发行删除了人物案例和账号级数据，重写了主要入口与部分参考说明。上述来源不代表原作者为本项目背书。

涉及上述来源的原有表达或贡献时，继续适用对应 MIT 许可；本项目自用限制只覆盖作者新增且有权授权的部分。直接使用上游本身不需向本项目作者另取授权。

Tribe AI 子目录许可与 knowledge-work-plugins 根目录许可不同，不能用根目录 Apache-2.0 概括这个来源。Anthropic Skills 也包含不同许可的子目录，不能把所有 Skills 统一视为一种许可。

## 其他概念参考

- [Anthropic Skills](https://github.com/anthropics/skills)：技能组织方式。本次发行不打包该项目的原始文件；使用具体文件前应查其目录与许可。
- [Anthropic Claude Cookbooks](https://github.com/anthropics/claude-cookbooks)：使用示例。本次发行不打包该项目的原始文件。
- Cialdini（2021），*Influence*：关于说服的理论背景。
- Meincke 等（2025），*Call Me A Jerk: Persuading AI to Comply with Objectionable Requests*：历史笔记曾经通过上游转引，本次发行不据此宣称本项目已被该实验验证。

## 语料与新增来源

本项目不取得第三方字幕、文章、个人经历或账号身份的权利。真实语料不随本次当前发行提供，处理边界见 [ETHICS.md](ETHICS.md)。

后续引入第三方内容应记录来源文件、版本、许可、版权与具体改动，按要求保留 NOTICE 等声明；对许可或权属不明的内容，不能先收入再宣称无风险。
