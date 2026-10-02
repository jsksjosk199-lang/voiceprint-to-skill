# -*- coding: utf-8 -*-
"""检查 / 同步用户级和项目级 Skill 副本（Python 3.9+）。

默认只检查当前目录及祖先目录的项目级副本；--sync 必须显式提供目标。
目标只允许 <项目>/.workbuddy/skills/<技能名>，或用 --project-layout codex 切换。
同步先复制到暂存目录，校验后替换；旧副本保留为同级 .bak 目录，不递归删除。
排除 Git、常见私有语料和凭证路径；这不是脱敏工具，其他私有文件须人工检查。
"""
import argparse
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
import uuid

EXCLUDED_DIRS = {".git", ".hg", ".svn", "private", "corpus", "raw", "transcripts",
                 "reference-notes", "raw-notes", "__pycache__", "node_modules", ".venv", "venv"}
EXCLUDED_FILES = {".ds_store", "thumbs.db", "desktop.ini"}


def excluded(path):
    name = path.name.lower()
    return (name in EXCLUDED_DIRS or name in EXCLUDED_FILES or name == ".env"
            or name.startswith(".env.") or name.endswith((".bak", ".pyc", ".pyo", ".srt", ".vtt", ".ass"))
            or "account-map" in name or ("opening-corpus-" in name and name.endswith(".md")))


def reject_links(path):
    """拒绝任何已存在的符号链接、Windows junction 或其他重解析组件。"""
    for component in [path, *path.parents]:
        try:
            info = component.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or (getattr(info, "st_file_attributes", 0)
                                        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)):
            raise ValueError(f"拒绝链接或重解析路径：{component}")


def inventory(root):
    files = {}

    def visit(directory):
        for path in sorted(directory.iterdir()):
            if excluded(path):
                continue
            reject_links(path)
            if path.is_dir():
                visit(path)
            elif path.is_file():
                files[path.relative_to(root)] = path
            else:
                raise ValueError(f"不支持的文件类型：{path}")

    visit(root)
    return files


def same_files(left, right):
    return left.keys() == right.keys() and all(left[name].read_bytes() == right[name].read_bytes()
                                              for name in left)


def target_path(argument, name, layout, source):
    raw = Path(argument).expanduser().absolute()
    reject_links(raw)
    suffix = (layout, "skills", name)
    if raw.parts[-3:] == suffix:
        project = raw.parents[2]
    else:
        project = raw
    reject_links(project)
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f"项目根目录不存在：{project}")
    target = project / layout / "skills" / name
    reject_links(target)
    target = target.resolve()
    # 只有解析后的规范项目子路径才能移动，且不能与源目录重叠。
    if target != project / layout / "skills" / name or project not in target.parents:
        raise ValueError("目标不在指定项目的 skills 子目录中")
    if target == source or source in target.parents or target in source.parents:
        raise ValueError("源目录与目标相同或互相包含，拒绝同步")
    if target.exists() and not target.is_dir():
        raise ValueError(f"目标不是目录：{target}")
    return target


def synchronize(source_files, target):
    reject_links(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    reject_links(target.parent)
    stage = Path(tempfile.mkdtemp(prefix=".sync-stage-", suffix=".bak", dir=target.parent))
    backup = None
    try:
        for relative, source_file in source_files.items():
            reject_links(source_file)
            destination = stage / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination)
        if not same_files(source_files, inventory(stage)):
            raise ValueError("暂存副本校验失败，目标未替换")
        reject_links(target)
        if target.exists():
            backup = target.with_name(f".sync-backup-{target.name}-{uuid.uuid4().hex}.bak")
            # 上述目标已经解析并确认属于明确指定的项目目录。
            target.rename(backup)
        try:
            stage.rename(target)
        except OSError:
            if backup is not None and not target.exists():
                backup.rename(target)
                backup = None
            raise
        if not same_files(source_files, inventory(target)):
            raise ValueError("替换后校验失败；请检查目标及保留的备份")
    except (OSError, ValueError):
        if stage.exists():
            print(f"  暂存文件保留于：{stage}", file=sys.stderr)
        if backup is not None and backup.exists():
            print(f"  旧副本保留于：{backup}", file=sys.stderr)
        raise
    if backup is not None:
        print(f"  旧副本备份：{backup}（可能含私有资料，请勿公开）")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="小写字母、数字及单个连字符组成的技能名，最长 64 字符")
    parser.add_argument("projects", nargs="*", help="项目根目录或规范的项目级 Skill 目录")
    parser.add_argument("--sync", action="store_true", help="校验暂存副本后替换，保留旧目录备份")
    parser.add_argument("--skills-root", type=Path, default=Path.home() / ".workbuddy" / "skills",
                        help="用户级 skills 根目录（源目录的父目录）")
    parser.add_argument("--project-layout", choices=["workbuddy", "codex"], default="workbuddy")
    args = parser.parse_intermixed_args()
    if len(args.name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.name):
        parser.error("技能名无效；不能含路径、空格、点或连续连字符")
    if args.sync and not args.projects:
        parser.error("--sync 必须显式提供项目根目录或项目级 Skill 目录")
    try:
        source = args.skills_root.expanduser().absolute() / args.name
        reject_links(source)
        source = source.resolve()
        if not (source / "SKILL.md").is_file():
            raise ValueError("源目录缺少 SKILL.md，请检查 --skills-root 与技能名")
        source_files = inventory(source)
    except (OSError, ValueError) as error:
        print(f"检查失败：{error}", file=sys.stderr)
        return 1
    layout = "." + args.project_layout
    projects = args.projects or [str(project) for project in [Path.cwd(), *Path.cwd().parents]
                                 if (project / layout / "skills" / args.name).exists()
                                 and (project / layout / "skills" / args.name).resolve() != source]
    if not projects:
        print("未发现项目级副本；可显式提供项目根目录进行检查。")
        return 0
    failed = False
    seen = set()
    for project in projects:
        try:
            target = target_path(project, args.name, layout, source)
            if target in seen:
                continue
            seen.add(target)
            print(f"项目级副本：{target}")
            current = inventory(target) if target.exists() else {}
            if same_files(source_files, current):
                print("  所检查的公开文件一致（排除项未比较）。")
            elif args.sync:
                synchronize(source_files, target)
                print("  同步并校验完成。常见私有目录与 Git 元数据未从源复制。")
            else:
                print("  文件存在差异或目标不存在；未修改任何文件。")
                failed = True
        except (OSError, ValueError) as error:
            print(f"  失败：{error}", file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
