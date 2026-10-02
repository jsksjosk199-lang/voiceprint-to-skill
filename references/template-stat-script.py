# -*- coding: utf-8 -*-
"""【模板】语料全量指纹统计脚本（可复用）
用法：把 CORPUS 改成目标语料目录，运行即输出该账号的皮相指纹。
产出：句末语气词/口头禅/句首词/"你"密度/呢化连接词/纯断句判断——这是 style-guide 与 anchor-sentences 的数据基础。
"""
import os, re, glob
from collections import Counter

CORPUS = r"改成你的语料目录"  # ← 改这里，指向字幕/文本目录

files = sorted(glob.glob(os.path.join(CORPUS, "*.txt")))
files = [f for f in files if "README" not in os.path.basename(f)]

def read_body(path):
    """去掉 B 站字幕头部元信息（标题/UP主/BV号/时长…），只留正文断句行"""
    with open(path, encoding="utf-8") as fp:
        lines = fp.read().split("\n")
    out = []
    for ln in lines:
        if ln.startswith("===="): continue
        if any(ln.startswith(k) for k in ["标题:","UP主:","BV号:","时长:","播放:","字幕来源:"]):
            continue
        out.append(ln.strip())
    return [s for s in out if s]

all_segs = []   # 所有断句单元（每行一句）
all_zh = ""     # 所有纯中文字符
for f in files:
    segs = read_body(f)
    all_segs.extend(segs)
    all_zh += "".join(re.findall(r"[\u4e00-\u9fff]", " ".join(segs)))

print(f"文件数:{len(files)}  断句单元:{len(all_segs)}  纯中文字符:{len(all_zh)}")
k = len(all_zh)/1000

# 1. 句末语气词
end_moody = Counter()
for s in all_segs:
    m = re.search(r"[呢啊哈吧呀啦嘛]$", s)
    if m: end_moody[m.group()] += 1
print("\n【句末语气词】", dict(end_moody.most_common()))

# 2. 高频口头禅
kouchan = ["大家","其实","但是","所以","比如","说实话","对不对","是不是","对吧","真的","而且","然后","一定要","说白了"]
print("\n【口头禅频次】")
for w in kouchan:
    c = all_zh.count(w)
    if c: print(f"  {w}: {c}")

# 3. 人称密度（我/你/我们 —— "我">"你" 多为演示型；反之多为说教型）
you = all_zh.count("你"); wo = all_zh.count("我"); women = all_zh.count("我们")
print(f"\n【人称密度】你:{you}({you/k:.0f}/千字)  我:{wo}({wo/k:.0f}/千字)  我们:{women}({women/k:.0f}/千字)")
print("  → 我 >> 你：演示型（我做给你看）；你 >> 我：说教型（你应该）")

# 3b. 句长分布（最强指纹之一，必看）
lens = sorted(len(s) for s in all_segs)
print(f"\n【句长】平均{sum(lens)/len(lens):.1f}字  中位数{lens[len(lens)//2]}  最短{lens[0]}  最长{lens[-1]}")
print(f"  <=10字占比:{sum(1 for l in lens if l<=10)/len(lens):.0%}  <=20字占比:{sum(1 for l in lens if l<=20)/len(lens):.0%}")

# 3c. 通用 2-gram 高频词（先跑这个，再据此重写上方 kouchan 词表！）
print("\n【高频2字词TOP40（据此改 kouchan 词表）】")
w2 = Counter(re.findall(r"(?=([\u4e00-\u9fff]{2}))", all_zh))
for w,c in w2.most_common(40): print(f"  {w}:{c}")

# 4. 呢化连接词
print("\n【呢化连接词】")
for w in ["但是呢","所以呢","然后呢","而且呢","其实呢","这个呢"]:
    c = all_zh.count(w)
    if c: print(f"  {w}: {c}")

# 5. 句首高频（2/3字）
print("\n【句首2字TOP20】")
c2 = Counter(s[:2] for s in all_segs if len(s)>=2)
for w,c in c2.most_common(20): print(f"  {w}:{c}")
print("\n【句首3字TOP20】")
c3 = Counter(s[:3] for s in all_segs if len(s)>=3)
for w,c in c3.most_common(20): print(f"  {w}:{c}")

# 6. 是否纯断句（统计有无常见中文标点）
has_punct = sum(1 for s in all_segs if re.search(r"[。？！，]", s))
print(f"\n【标点判断】含标点断句比例:{has_punct}/{len(all_segs)}  (若极低→B站纯断句，短句+语气词当句号)")
