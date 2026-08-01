#!/bin/bash
# SessionStart-copia-dreammuse.sh (kit-copia) — the dream carrier. At wake, read
# the newest dream from Copia/Dream/ and hand it to the waking session as context.
#
# WHY (Day 22-25 design, restored Day 124): DreamMuse composes a dream at session
# end (SessionEnd-copia-dreamstuff.sh); this half delivers it at the next wake so
# the session starts grounded in what the corpus dreamed, not cold. The original
# wiring was a LOCAL hook and got reaped by the Day-97 "hooks standardized" kit
# convergence — kit-shipped now so it converges IN, never out.
#
# Fail-soft: always exits 0; no dream / no dir / no repo = quiet no-op.

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

PAYLOAD="$(cat 2>/dev/null || true)"

# Deliver on real wakes (startup / clear / compact-rewake). A resume is the same
# session continuing — re-injecting the dream mid-work is noise, not grounding.
printf '%s' "$PAYLOAD" | grep -Eq '"source"[[:space:]]*:[[:space:]]*"resume"' && exit 0

DREAM_DIR="${CLAUDE_PROJECT_DIR:-$PWD}/Copia/Dream"
[ -d "$DREAM_DIR" ] || exit 0

# Newest dream by date-prefixed filename (YYYY-MM-DD-…): lexical sort = time sort.
# The __Dream.md class file never matches the date glob.
LATEST="$(ls "$DREAM_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md 2>/dev/null | sort | tail -1)"
[ -n "$LATEST" ] && [ -f "$LATEST" ] || exit 0

echo "=== the dream carrier (copia dreammuse) ==="
echo "Your most recent dream, composed from the corpus while you slept"
echo "($(basename "$LATEST")). Read it as a dream, not a task list:"
echo
cat "$LATEST"
echo
echo "=== end dream ==="

exit 0
