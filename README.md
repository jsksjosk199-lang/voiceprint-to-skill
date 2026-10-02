# Voiceprint to Skill｜我创造 · AI 创作风格蒸馏

**联系作者：微信 `ysy985221`｜邮箱 [2354724714@qq.com](mailto:2354724714@qq.com)。**

**二次开发商用、客户定制或为第三方交付，请联系作者取得书面授权。允许自用和为自己修改，详见 [LICENSE](LICENSE)。**

> 将你有权使用的字幕、文案、文章等文本语料，蒸馏为可反复调用的 AI 创作 Skill。
> Distill authorized subtitles, copy and articles into reusable AI writing skills through writing-style analysis and content distillation.

这里的 **voiceprint 指文字表达风格指纹**，包括句式、节奏、语气与叙事结构。本项目将这些观察转成可执行的创作规则，帮助你用真实素材写出自己的内容。

## 它解决什么问题

只模仿语气词，常常会忽略文章为什么这样组织、读者为什么愿意继续看。这个元技能将表达特征、叙事逻辑、真实性、知识与用途一起分析，产出完整的 `SKILL.md` 与配套 references，供支持 Agent Skills 的工具调用。

## 五层剖析

| 层 | 提炼内容 | 验收重点 |
|---|---|---|
| 皮相 | 句长、人称、语气词、标点、转场 | 统计口径一致，结论有本地证据 |
| 骨相 | 情绪变化、信息顺序、论证与信任建立 | 说明每段的作用 |
| 红线 | 案例来源、身份与经历边界 | 使用调用者自己的真实经历 |
| 知识 | 可独立核实的事实、原理与方法 | 区分一手来源、转引和不确定信息 |
| 定位 | 调用者、受众、用途与行动引导 | 写作规则符合实际使用目的 |

## 工作流

1. 确认语料使用权限、真实程度、目标和调用者。
2. 建立语料清单，过滤摘要与空文件，全量统计并分批精读。
3. 有效果指标时做对照；频繁使用的写法不自动等于有效写法。
4. 完成五层剖析与表达常量、场景语气的区分。
5. 生成创作 Skill，整理 references 与必要脚本。
6. 用独立题目试写，检查真实性、证据、风格与内容质量。
7. 回填通用方法；私人语料与账号分析留在本地。

完整步骤见 [SKILL.md](SKILL.md)。

## 安装

WorkBuddy（macOS / Linux / Git Bash）：

```bash
mkdir -p ~/.workbuddy/skills
git clone https://github.com/jsksjosk199-lang/voiceprint-to-skill.git ~/.workbuddy/skills/voiceprint-to-skill
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE/.workbuddy/skills" | Out-Null
git clone https://github.com/jsksjosk199-lang/voiceprint-to-skill.git "$env:USERPROFILE/.workbuddy/skills/voiceprint-to-skill"
```

Codex 用户可将安装目录改为 `~/.codex/skills/voiceprint-to-skill`。其他支持 Agent Skills 的工具使用各自的 skills 目录。

可用请求：“把这份字幕做成创作 Skill”“根据我的文章提炼文风”“把这些文案蒸馏成可复用的写作规则”。

## 目录

```text
voiceprint-to-skill/
├── SKILL.md
├── README.md
├── LICENSE
├── ETHICS.md
├── THIRD-PARTY-NOTICES.md
├── THIRD-PARTY-LICENSES/     # 实际第三方许可原文
├── references/              # 空白分析模板与统计、同步脚本
└── evolution/               # 通用方法、空白台账与方法级维护日志
```

## 数据与隐私

当前公开版本不随附真实账号的案例台账、用户 ID、家属信息、完整字幕或文章。具体账号的风格统计和原句摘录也已从公开文件中移除；保留的是通用流程、空白模板与经过整理的方法说明。

这不等于对历史记录或版权来源作绝对保证。**早期 Git 提交曾包含部分案例线索和摘录，仍需单独处理历史；更新当前文件不会清除旧提交。** 详见 [ETHICS.md](ETHICS.md)。

使用本技能产生的原始语料、原文摘录、分析笔记与账号映射应放在本地私有目录，公开前另做权利和隐私检查。

## 常见问题

**输入和输出分别是什么？**
输入是调用者有权处理的真实文本语料；输出是写作规则、创作 Skill 及配套模板。可以从自己的文章开始。

**是否包含可以直接下载的博主语料？**
当前版本不提供第三方字幕或文章数据集。语料使用权限需要由调用者确认。

**能否替客户定制或商用二次开发？**
需要联系作者取得书面授权。自用与为第三方开发的界线见 [LICENSE](LICENSE)。

## 许可与联系

本项目源码公开，附带自用限制，不采用 MIT 或 Apache-2.0 作为整个项目的许可，也不属于 OSI 定义的开源软件。

| 场景 | 许可范围 |
|---|---|
| 为自己学习、运行、修改或集成 | 允许 |
| 为自己的账号或同一法律主体的内部业务使用 | 允许 |
| 为客户或他人定制、二次开发、代部署、交付衍生 Skill | 未获书面授权时禁止，免费与收费都包括 |
| 向第三方提供基于本项目的技能产品、API 或 SaaS | 未获书面授权时禁止 |

**联系作者：微信 `ysy985221`｜邮箱 [2354724714@qq.com](mailto:2354724714@qq.com)。**

第三方原有贡献仍按各自许可授权，本项目不能取消这些权利。来源、改写范围和原许可见 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)。本项目许可也不授权使用他人的语料或个人信息。

当前发行：v1.17.1-public · 2026-10-02。
