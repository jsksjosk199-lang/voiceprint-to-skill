#!/usr/bin/env bash
# Python 3.9+ 同步工具的 Bash 入口；Windows 也可直接运行同目录 .py 文件。
# 默认只检查；--sync 必须显式提供项目根目录或项目级 Skill 目录。
# 示例：bash references/tool-sync-copies.sh voiceprint-to-skill --sync "C:/path/to/project"
set -eu
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  exec python3 -X utf8 "$SCRIPT_DIR/tool-sync-copies.py" "$@"
elif command -v python >/dev/null 2>&1; then
  exec python -X utf8 "$SCRIPT_DIR/tool-sync-copies.py" "$@"
else
  echo "需要 Python 3.9+；请安装后重试。" >&2
  exit 1
fi
