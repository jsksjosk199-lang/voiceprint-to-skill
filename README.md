# Voiceprint to Skill｜我创造 · AI 创作风格蒸馏

**联系作者：微信 `ysy985221`｜邮箱 [2354724714@qq.com](mailto:2354724714@qq.com)。**

> **我可以帮你做写作 Skill 蒸馏，也可以代做字幕采集和语料整理。**
>
> 微信 `ysy985221`｜邮箱 [2354724714@qq.com](mailto:2354724714@qq.com)｜[查看服务内容与委托方式](#代做服务)

**Apache-2.0 开源：个人和企业均可免费商用、接单、修改、二次开发、分享、销售及交付；不因商用本身要求付费或分成。分发时保留适用声明并注明修改，详见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)。**

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

### Skills CLI

需要 Git 和 Node.js 22.20+（含 npm / npx）。在希望使用该技能的项目目录中运行：

```bash
npx skills add jsksjosk199-lang/voiceprint-to-skill
```

按提示选择 CLI 支持的 Agent 和安装方式；当前已验证 Skills CLI 1.7.0 能发现本技能，并完成 Codex 项目安装。也可以显式指定 Codex，并复制文件：

```bash
npx skills add jsksjosk199-lang/voiceprint-to-skill --skill voiceprint-to-skill --agent codex --copy
```

默认安装到当前项目的技能目录；Codex 项目目录为 `.agents/skills/voiceprint-to-skill`。如需安装到用户级目录，可增加 `--global`。更多选项见 [Skills CLI 官方说明](https://github.com/vercel-labs/skills#install-a-skill)。

### 直接使用 Git

以下方式只需要 Git；两个辅助工具另需 Python 3.9+，均只使用标准库。

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

## 辅助工具

在安装目录运行统计工具，输入与统计结果都保存在自己的私有工作区：

```powershell
python -X utf8 references/template-stat-script.py "自己的私有语料目录"
```

仅统计该目录第一层的 `.txt` 正文行，自动过滤常见字幕元信息；每行是一个统计单元，不自动按标点切句。空语料会给出失败原因；没有中文时不计算中文密度。

检查项目级副本，默认不修改文件；确认路径和差异后，加 `--sync` 同步：

```powershell
python -X utf8 references/tool-sync-copies.py voiceprint-to-skill "自己的项目根目录"
python -X utf8 references/tool-sync-copies.py voiceprint-to-skill --sync "自己的项目根目录"
```

默认源为用户级 `.workbuddy/skills/voiceprint-to-skill`，目标为指定项目的 `.workbuddy/skills/voiceprint-to-skill`。Codex 可增加 `--project-layout codex --skills-root "用户级 .codex/skills 目录"`。Bash 用户也可通过 [Shell 入口](references/tool-sync-copies.sh) 传入相同参数。

同步先暂存并校验，保留目标旧目录的 `.bak` 备份；拒绝异常技能名、重叠目录、符号链接和 Windows junction。Git 元数据、常见私有语料目录及 `.env` 不从源复制。**排除规则不能识别任意文件中的个人信息；同步前仍应检查源文件，备份也不能公开。** 实现见 [同步工具](references/tool-sync-copies.py)。

## 目录

```text
voiceprint-to-skill/
├── SKILL.md
├── README.md
├── LICENSE
├── ETHICS.md
├── NOTICE                   # 作者与项目来源声明
├── USE-AGREEMENT.md          # 可选择另行订立的标注约定
├── THIRD-PARTY-NOTICES.md
├── THIRD-PARTY-LICENSES/     # 实际第三方许可原文
├── references/              # 空白分析模板与统计、同步脚本
└── evolution/               # 通用方法、空白台账与方法级维护日志
```

## 数据与隐私

当前公开版本不随附真实账号的案例台账、用户 ID、家属信息、完整字幕或文章。具体账号的风格统计和原句摘录也已从公开文件中移除；保留的是通用流程、空白模板与经过整理的方法说明。

这不等于对历史记录或版权来源作绝对保证。**2026-10-02 已重写公开主分支历史，旧提交不再属于主分支历史。但实测旧提交仍可通过直接链接读取；GitHub 服务端关联、缓存及他人的 Fork/克隆仍需单独处理。** 详见 [ETHICS.md](ETHICS.md)。

使用本技能产生的原始语料、原文摘录、分析笔记与账号映射应放在本地私有目录，公开前另做权利和隐私检查。

## 常见问题

**输入和输出分别是什么？**
输入是调用者有权处理的真实文本语料；输出是写作规则、创作 Skill 及配套模板。可以从自己的文章开始。

**是否包含可以直接下载的博主语料？**
当前版本不提供第三方字幕或文章数据集。语料使用权限需要由调用者确认。

**能否替客户定制或商用二次开发？**
允许，无需仅因商用向作者付费、分成或另取授权。分发实际项目内容时遵守 Apache-2.0 和适用第三方许可，详见 [来源标注指南](references/attribution-guide.md)。

**没有现成字幕，或者需要有人帮我完成蒸馏怎么办？**
可以委托作者提供字幕采集、语料整理和写作 Skill 定制服务。提供目标账号或作品链接及使用目标，即可沟通处理范围与交付需求，详见 [代做服务](#代做服务)。

## 代做服务

**我可以帮你把字幕、文章和文案蒸馏成可复用的写作 Skill。** 如果你需要收集某位创作者的素材、整理语料，或者希望有人完成分析、定制与使用指导，可以把这项工作交给我。

| 服务 | 可以为你完成什么 |
|---|---|
| 字幕采集与语料整理 | 根据你提供的目标账号或作品链接，在确认可处理范围后收集素材，去重、清洗并整理为可分析的文本 |
| 写作 Skill 蒸馏 | 分析表达习惯、叙事结构和内容定位，转成可复用的写作规则、`SKILL.md` 与配套 references |
| 定制与使用指导 | 按你的内容用途调整 Skill，协助安装、试写和修改；写作采用你自己的身份、观点与真实经历 |

**联系时，请先说明：**

- 目标账号或作品链接，以及素材使用权限；也可以提供你自己的内容。
- 是否已有字幕或文章，大致有多少素材。
- 想用于口播、公众号文章、品牌文案还是其他体裁。
- 期望的交付内容与时间。

交付内容按需求约定，可包括整理后的语料、写作 Skill、配套文件、安装说明与试写结果。素材采集、处理和交付需具备相应权限并符合平台允许范围；原始语料和账号分析默认私有交付，公开展示另行确认。

**委托服务按素材规模、交付范围和定制需求单独报价。开源项目仍可免费使用、商用和二次开发。**

**添加微信 `ysy985221`，备注「Skill 定制」；或发送需求到 [2354724714@qq.com](mailto:2354724714@qq.com)。我会先评估素材范围与需求，再沟通报价和交付安排。**

## 许可与联系

本项目作者的原创贡献使用标准 **Apache License 2.0**，完整原文见 [LICENSE](LICENSE)，作者和项目来源见 [NOTICE](NOTICE)。本次 v1.18.0 将旧自用限制改为标准开源授权；已取得的第三方许可权利不受影响，不向旧使用者追溯施加新合同义务。

| 场景 | 许可范围 |
|---|---|
| 个人与企业学习、运行、内部降本增效、商业业务 | 允许，不收许可费或分成 |
| 为客户接单、定制、二次开发、部署、销售或交付 | 允许，不因商用本身另收授权费 |
| 分享原项目或分发复制、修改、改编版 | 允许；保留适用版权、作者、项目链接、许可和 NOTICE，显著说明修改 |
| 使用工具制作未复制项目内容的独立新 Skill | 可自行选择许可；工具来源标注为建议 |
| 自愿另行同意工具来源标注约定后提供新 Skill | 按双方明确同意的合同约定标注，即使未复制文字 |

**制作工具来源标注的边界：** 仅使用本项目不会自动产生新 Skill 的版权署名义务。建议保留制作工具来源段；愿意另行约定者可使用 [自愿使用协议模板](USE-AGREEMENT.md)。该协议不修改 Apache-2.0，不是使用前置条件，未同意者仍可正常开源使用。完整示例见 [来源标注指南](references/attribution-guide.md)。

**联系作者：微信 `ysy985221`｜邮箱 [2354724714@qq.com](mailto:2354724714@qq.com)。**

第三方原有贡献仍按各自许可授权，本项目不能取消这些权利。来源、改写范围和原许可见 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)。本项目许可也不授权使用他人的语料或个人信息。

当前发行：v1.18.1 · 2026-10-02。
