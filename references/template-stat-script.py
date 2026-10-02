# -*- coding: utf-8 -*-
"""中文表达统计模板。Python 3.9+，只读输入，不写文件。

用法：python template-stat-script.py "语料目录"
也可修改 CORPUS 后直接运行。只统计目录第一层的 .txt 文件（排除 README）。
每条非空正文行是一个断句单元；不自动按标点切句。原文与输出均留在私有工作区。
"""
import argparse
from collections import Counter
from pathlib import Path
import re
import statistics
import sys

CORPUS = r"改成你的语料目录"
HEADER = re.compile(r"^(?:标题|UP主|BV号|时长|播放|字幕来源)\s*[:：]", re.I)
CHINESE_RUN = re.compile(r"[\u4e00-\u9fff]+")
END_PUNCTUATION = "。？！!?，,；;：:、…—.\"'”’）)]】}」』〉》"


def read_body(path):
    """读取 UTF-8（含 BOM）；过滤常见字幕元信息和分隔线。"""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    return [line for raw in lines if (line := raw.strip())
            and not line.startswith("====") and not HEADER.match(line)]


def analyze(corpus):
    if not corpus.is_dir():
        raise ValueError("语料目录不存在；请传入实际目录，或先修改 CORPUS。")
    files = sorted(p for p in corpus.iterdir() if p.is_file()
                   and p.suffix.lower() == ".txt" and "readme" not in p.name.lower())
    segments = [line for path in files for line in read_body(path)]
    if not segments:
        raise ValueError("没有可统计的正文：检查目录第一层的 .txt 文件及元信息过滤。")
    # 连续中文片段分别统计，避免跨行、跨文件、跨标点拼出不存在的词。
    runs = [run for segment in segments for run in CHINESE_RUN.findall(segment)]
    chinese_count = sum(map(len, runs))
    count_word = lambda word: sum(run.count(word) for run in runs)
    print(f"文件数:{len(files)}  断句单元:{len(segments)}  纯中文字符:{chinese_count}")
    print("口径：每条正文行为一个单元；行长含标点和非中文字符；中文密度以中文字符数为分母。")

    endings = Counter()
    for segment in segments:
        ending = segment.rstrip().rstrip(END_PUNCTUATION).rstrip()
        match = re.search(r"[呢啊哈吧呀啦嘛]$", ending)
        if match:
            endings[match.group()] += 1
    print("\n【句末语气词】", dict(endings.most_common()))

    print("\n【口头禅频次】")
    for word in ["大家", "其实", "但是", "所以", "比如", "说实话", "对不对", "是不是",
                 "对吧", "真的", "而且", "然后", "一定要", "说白了"]:
        count = count_word(word)
        if count:
            print(f"  {word}: {count}")

    print("\n【人称密度】（字面计数：我包含我们中的我，各项可能重叠）")
    for word in ["你", "我", "我们"]:
        count = count_word(word)
        density = f"{count * 1000 / chinese_count:.0f}/千字" if chinese_count else "不适用：无中文字符"
        print(f"  {word}:{count}({density})")
    print("  人称频次是观察指标；结合上下文分析，不能直接证明文体或效果。")

    lengths = [len(segment) for segment in segments]
    print(f"\n【行长】平均{statistics.mean(lengths):.1f}字  中位数{statistics.median(lengths):g}"
          f"  最短{min(lengths)}  最长{max(lengths)}")
    print(f"  <=10字占比:{sum(length <= 10 for length in lengths) / len(lengths):.0%}"
          f"  <=20字占比:{sum(length <= 20 for length in lengths) / len(lengths):.0%}")

    bigrams = Counter(run[index:index + 2] for run in runs for index in range(len(run) - 1))
    print("\n【高频2字片段TOP40（片段不等于分词结果）】")
    for word, count in bigrams.most_common(40):
        print(f"  {word}:{count}")
    print("\n【呢化连接词】")
    for word in ["但是呢", "所以呢", "然后呢", "而且呢", "其实呢", "这个呢"]:
        count = count_word(word)
        if count:
            print(f"  {word}: {count}")
    for width in [2, 3]:
        print(f"\n【行首{width}字TOP20（保留原行标点）】")
        starts = Counter(segment[:width] for segment in segments if len(segment) >= width)
        for word, count in starts.most_common(20):
            print(f"  {word}:{count}")
    punctuated = sum(bool(re.search(r"[。？！，]", segment)) for segment in segments)
    print(f"\n【标点观察】含常见中文标点的行:{punctuated}/{len(segments)}；转写标点可能由转写工具加入。")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", nargs="?", default=CORPUS, type=Path)
    args = parser.parse_args()
    try:
        analyze(args.corpus)
    except (ValueError, OSError, UnicodeError) as error:
        print(f"统计失败：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
