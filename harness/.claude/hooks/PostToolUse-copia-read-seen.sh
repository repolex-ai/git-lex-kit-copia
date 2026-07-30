#!/bin/bash
# PostToolUse-copia-read-seen.sh (kit-copia) — read = seen: a Familiar's Read of a
# Pool image blob lands on the copia shared window, by architecture.
#
# Naming: <Event>-<kit>-<purpose>.sh. Leading segment `PostToolUse` is the CC event;
# git-lex registers this script under it. The script self-filters (PostToolUse fires
# for EVERY tool): only a Read whose file_path walks a Pool image blob tree does
# anything. The logic half is the companion PostToolUse-copia-read-seen.py (same
# stem, the sanctioned .sh-shim + .py pattern — a bare .py never fires as a hook).
#
# WHY (Rob, Day 120): the look verbs (`cosee look show`, `cosee go`) flash the frame
# the Familiar is judging onto the human's screen — but nothing FORCED their use. A
# Read straight off the filesystem was an invisible look: the human saw the agent
# reading, but the shared window never moved. Discipline-based rules rot; this hook
# makes the tee structural: every Claude-eye look at a Pool image = a main_image set
# — gated, actor-attributed (familiar), activity-logged, broadcast, and refused
# structurally when cosee is OFF. Through copia's gated surface, never around it.
# Cross-soul guard is fail-closed: copia bound to another soul => no push (see .py).
#
# Fail-soft: always exits 0; warns (server down, 403) are one gentle stderr line.

set -u

# --- kit-hook opt-out guard (managed; do not edit) ---
# A kit-managed hook can't be un-registered locally: CC merges hooks (local ADDS, never
# overrides) and kit-update re-converges settings.json every compaction. This guard is
# the escape hatch — list this hook's basename (no .sh) under soul.disabledHooks in
# .claude/settings.local.json and the hook no-ops. settings.local.json is gitignored and
# never touched by kit-update, so the opt-out is durable + soul-private. Fail-soft: any
# trouble reading/parsing → the hook runs normally (a broken opt-out never silences a hook).
_glx_local="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/settings.local.json"
if [ -f "$_glx_local" ] && grep -q disabledHooks "$_glx_local" 2>/dev/null; then
    _glx_self="$(basename "${BASH_SOURCE[0]:-$0}" .sh)"
    if python3 - "$_glx_local" "$_glx_self" <<'PY' 2>/dev/null
import json, sys
cfg, name = sys.argv[1], sys.argv[2]
try:
    with open(cfg) as f:
        disabled = (json.load(f).get("soul") or {}).get("disabledHooks") or []
    sys.exit(0 if name in disabled else 1)
except Exception:
    sys.exit(1)   # no file / bad json / no key → NOT disabled, run the hook
PY
    then
        exit 0
    fi
fi
# --- end kit-hook opt-out guard ---

PAYLOAD="$(cat)"

# FAST PATH: PostToolUse fires on every tool call — bail on cheap string checks
# before spawning python. Only a Read of a Pool image blob
# (…/blob/image/YYYY/MM/DD/<stem>.png — the Pool layout every soul shares) matters.
printf '%s' "$PAYLOAD" | grep -Eq '"tool_name"[[:space:]]*:[[:space:]]*"Read"' || exit 0
printf '%s' "$PAYLOAD" | grep -q '/blob/image/' || exit 0

# Program from FILE so stdin stays free to carry the payload (a heredoc would eat
# it). Messages ride the .py's stdout; route them to stderr, capped — hook stderr
# must stay one gentle line, never a traceback flood.
_hook_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
printf '%s' "$PAYLOAD" | python3 "$_hook_dir/PostToolUse-copia-read-seen.py" \
    "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null | head -3 >&2 || true

exit 0
