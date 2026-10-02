#!/usr/bin/env bash
# ============================================================
# 双副本一致性检查 / 同步工具
# 配合 SKILL.md 第 16 条硬规则：同一 Skill 的用户级与项目级副本必须一致。
#
# 用法：
#   bash tool-sync-copies.sh <skill名>                     # 只检查（默认）
#   bash tool-sync-copies.sh <skill名> --sync               # 以用户级为准，覆盖项目级
#   bash tool-sync-copies.sh <skill名> --sync <路径1> <路径2>  # 显式指定项目级副本
#                                                            # （给项目根目录或 skill 目录都行）
#
# 例：
#   bash references/tool-sync-copies.sh wochuangzao-skill --sync "C:/path/to/your/project"
#
# 背景（2026-09-11 实测翻车）：
#   同一 Skill 常同时存在于
#     用户级  ~/.workbuddy/skills/<名>
#     项目级  <项目>/.workbuddy/skills/<名>
#   两份各自演化 → 漂移。实测 wochuangzao-skill 项目级停在 v1.1.0（落后 4 版），
#   且缺少 cross-account-patterns.md 与整个 lessons/。
#   ⚠️ 漂移副本被下游调用时，跑的是旧规则 —— 不是"少一条经验"，是"错的规则在生效"。
# ============================================================

set -uo pipefail

NAME="${1:-}"
shift || true
MODE=""
EXPLICIT=()

for arg in "$@"; do
  if [ "$arg" = "--sync" ]; then
    MODE="--sync"
  else
    EXPLICIT+=("$arg")
  fi
done

if [ -z "$NAME" ]; then
  echo "用法：bash $0 <skill名> [--sync] [项目路径...]"
  exit 2
fi

USER_DIR="$HOME/.workbuddy/skills/$NAME"
if [ ! -d "$USER_DIR" ]; then
  echo "❌ 用户级副本不存在：$USER_DIR"
  exit 1
fi

echo "✅ 用户级（基准）：$USER_DIR"
grep -m1 "当前版本" "$USER_DIR/SKILL.md" 2>/dev/null || true

# ---------- 收集项目级副本 ----------
PROJ=()
if [ "${#EXPLICIT[@]}" -gt 0 ]; then
  for p in "${EXPLICIT[@]}"; do
    p="${p%/}"
    if [ "$(basename "$p")" = "$NAME" ]; then
      PROJ+=("$p")
    else
      PROJ+=("$p/.workbuddy/skills/$NAME")
    fi
  done
else
  # 默认：从当前目录往上找
  while IFS= read -r line; do
    [ -n "$line" ] && PROJ+=("$line")
  done < <(find "$(pwd)" "$(pwd)/.." "$(pwd)/../.." -maxdepth 4 -type d \
             -path "*/.workbuddy/skills/$NAME" 2>/dev/null | sort -u)
fi

if [ "${#PROJ[@]}" -eq 0 ]; then
  echo "ℹ️  没找到项目级副本，无需同步。"
  exit 0
fi

# ---------- 逐个比对 ----------
RC=0
for P in "${PROJ[@]}"; do
  echo ""
  echo "--- 项目级副本：$P"
  if [ ! -d "$P" ]; then
    echo "   ⚠️  不存在（如需创建：加 --sync 会一并建好）"
    RC=1
    [ "$MODE" = "--sync" ] || continue
  else
    grep -m1 "当前版本" "$P/SKILL.md" 2>/dev/null || true
    if diff -rq "$USER_DIR" "$P" >/dev/null 2>&1; then
      echo "   ✅ 一致（diff = 0）"
      continue
    fi
    echo "   ⚠️  存在差异："
    diff -rq "$USER_DIR" "$P" 2>&1 | sed 's/^/      /'
    RC=1
  fi

  if [ "$MODE" = "--sync" ]; then
    # 安全阀：只允许动 .workbuddy/skills/<名> 这一层
    case "$P" in
      *".workbuddy/skills/$NAME") ;;
      *) echo "   ❌ 拒绝操作（路径不像 .workbuddy/skills/$NAME）：$P"; RC=1; continue ;;
    esac
    echo "   → 以用户级为准同步中…"
    rm -rf "$P"
    mkdir -p "$(dirname "$P")"
    cp -r "$USER_DIR" "$P"
    if diff -rq "$USER_DIR" "$P" >/dev/null 2>&1; then
      echo "   ✅ 已同步，校验 diff = 0"
      RC=0
    else
      echo "   ❌ 同步后仍有差异，请手工检查"
      RC=1
    fi
  fi
done

echo ""
if [ "$RC" -eq 0 ]; then
  echo "🎉 全部副本一致。"
else
  echo "❗ 有副本不一致 —— 加 --sync 可一键以用户级为准覆盖。"
fi
exit "$RC"
