# 【模板】主题扫描与分批精读（大语料用）

> **数据边界：** 本文件是空白方法模板。真实账号身份、原文摘录、私人事件及个体统计只能填写在本地私有副本；不要回填到公开仓库。这里的例子是方法示意，不能充当真实个人案例。


> 当语料很大且产出 Skill 只服务某类主题时，按以下流程处理：**正文扫描找相关子集 → 人工复核 → 分批精读 → 汇总方法。** 可以由当前 Agent 顺序处理；只有当前任务授权委派且具备相应能力时，才使用多个 Agent。模板不授予额外的委派权限。

## 一、为什么不能只看文件名

很多相关内容标题根本不体现主题。例：讲"用 AI 工具/做 AI 视频"的集，标题可能只写产品名（Seedance/数字人/Gemini），不含"AI"二字。**只看文件名会漏掉大量真正相关语料。**

## 二、内容级扫描脚本（筛相关子集）

写脚本，对每个文件**读正文**统计主题关键词频次，而非只看文件名：

```python
from pathlib import Path
import re

CORPUS = Path("改成自己的私有语料目录")
KEYWORDS = ["ai", "agent", "数字人", "视频", "工具", "自动化"]
THRESHOLD = 5  # 示例阈值，按语料调整；关键词命中不等于主题判定
HEADER = re.compile(r"^(?:标题|UP主|BV号|时长|播放|字幕来源)\s*[:：]", re.I)
if not CORPUS.is_dir():
    raise SystemExit("请先将 CORPUS 改成实际语料目录")
matches = []
for path in sorted(CORPUS.glob("*.txt")):
    if "readme" in path.name.lower():
        continue
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    body = "\n".join(line.strip() for line in lines
                     if not HEADER.match(line.strip()) and not line.strip().startswith("===="))
    count = sum(body.lower().count(keyword.lower()) for keyword in KEYWORDS)
    if count >= THRESHOLD:
        matches.append((count, path.name))
for count, name in sorted(matches, reverse=True):
    print(name, count)  # 文件名与扫描结果仅保存在私有工作区
```

产出候选清单，按命中次数排序后人工复核；记录未命中、空文件与读取失败的范围。关键词统计不能代替精读。

## 三、分批策略

- 把子集按"相关度/主题"分成若干批，每批 3~5 篇（每篇 3000~12000 字）。
- 当前 Agent 逐批读取完整正文，输出 A~G 结构化笔记（见下），存成私有 md 文件；记录每批实际覆盖与缺口。
- 获得委派授权时可为每批分配 Agent，并给出明确文件清单与私有输出路径；未授权时继续顺序处理。
- 一次读不完就分多轮；抽样必须说明范围，不能当作全量精读。

## 四、每批精读任务模板（也可用于已获授权的委派）

> "你是内容风格分析师。请精读以下 [N] 篇 [账号] 字幕，逐字读完，产出结构化笔记。对每篇提炼：
> A. 主题相关度判定（高/中/低）+ 主要用什么工具/方法
> B. 开头怎么钩（现象/见闻/极端假设/人物案例/反常识/靶子反驳/扎心提问/预测/成果前置）+ 原句
> C. 讲[主题]的专属话术/比喻（怎么让小白秒懂）+ 原句
> D. 真实案例与数字（注明是他自己还是学员/别人）
> E. 论证逻辑（怎么让人信服）
> F. 结尾 CTA + 原句
> G. 对[产出目的：如AI Skill获客]的启示
> 写成文件：...md。完成后 200 字内汇报。"

## 五、汇总成主题方法库

先在私有工作区汇总各批证据。拟公开的 Skill reference（如 `topic-library.md`）只包含不带个人线索的结构说明、自写示例，或已另行核查权利的引用，可包含：
- 该主题的开头钩子库
- 核心比喻/翻译层（把技术讲成人话的资产）
- 论证三板斧
- 观点表达方式与自写示例
- 主题价值主张迁移
- 避坑（该主题容易踩的坑）

## 六、精读笔记存档

各批笔记和原文证据仅存入本地私有工作区（如 private/reference-notes/），不写入公共 reference，也不自动提交。
