#!/bin/bash
# UserPromptSubmit-copia-share.sh (kit-copia) — pasted/dropped images → the Pool queue.
#
# Naming: <Event>-<kit>-<purpose>.sh (kit-authoring §3.2). The logic lives in the
# sibling UserPromptSubmit-copia-share.py (same stem, .py — hook-authoring's helper
# convention): STDLIB-ONLY python3, no copia checkout, no venv. v1 of this hook
# (kit-pool's UserPromptSubmit-pool-share.sh, retired) cd'd into a copia repo that
# moved out from under it and failed silently for weeks — this shape can't rot that
# way. The helper reads the transcript for base64 image turns and POSTs each to the
# Pool Door (:8424) as origin='claude-code-share', mode='see_only'; the eye does
# the rest. Which soul's queue: derived from the repo's genesis sha (env
# POOL_SOUL_ID / POOL_SERVE_URL override).
#
# STDOUT DISCIPLINE: on UserPromptSubmit, hook stdout is injected into the model's
# context. This script writes NOTHING to stdout (worker detached to /dev/null) so
# it never collides with the recall hook, which is the sole stdout owner.
#
# Fail-soft: always exits 0; a share is a nicety — it must never block or pollute
# a prompt.

set -u

# --- kit-hook opt-out guard (managed; do not edit) ---
# A kit-managed hook can't be un-registered locally: CC merges hooks (local ADDS, never
# overrides) and kit-update re-converges settings.json every compaction. This guard is
# the escape hatch — list this hook's basename (no .sh) under soul.disabledHooks in
# .claude/settings.local.json and the hook no-ops. settings.local.json is gitignored and
# never touched by kit-update, so the opt-out is durable + soul-private. Fail-soft: any
# trouble reading/parsing → the hook runs normally (a broken opt-out never silences a hook).
_glx_local="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/settings.local.json"
# Fast path: no file, or the key is absent → not disabled, skip the python spawn entirely
# (the common case pays nothing). Only parse when a disabledHooks list actually exists.
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

# The sibling helper, addressed relative to THIS script (hook-authoring: pass the
# program as a file path, not a heredoc — a heredoc would eat the payload's stdin).
_hook_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
_helper="$_hook_dir/UserPromptSubmit-copia-share.py"

if [ -f "$_helper" ]; then
    # Fire-and-forget: the helper polls the transcript up to ~3s (flush race) and
    # POSTs to the Door — none of which may delay the prompt. All output to
    # /dev/null; stdout MUST stay clean.
    (
        printf '%s' "$PAYLOAD" | nohup python3 "$_helper" \
            "${CLAUDE_PROJECT_DIR:-$PWD}" >/dev/null 2>&1
    ) &
    disown 2>/dev/null || true
fi

exit 0
