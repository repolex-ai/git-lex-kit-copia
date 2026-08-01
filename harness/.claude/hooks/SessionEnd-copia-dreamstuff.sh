#!/bin/bash
# SessionEnd-copia-dreamstuff.sh (kit-copia) — the dream maker. At session end,
# kick the DreamCatcher pipeline (vector index catch-up → synthesize → git lex
# save into Copia/Dream/) so the NEXT wake has a fresh dream to deliver
# (SessionStart-copia-dreammuse.sh is the delivery half).
#
# ONCE PER DAY: sessions end many times a day; dreams are nightly. The first
# session-end of a (UTC) day dreams; the rest are instant no-ops. (The old
# wiring rode PreCompact with no guard and dreamed 4x/day — see the Jul-3 logs.)
#
# DETACHED, NOT nohup-opaque: the catcher runs orphaned so session teardown
# can't kill it, but leaves a pidfile (dreammuse/dreamcatcher.pid — is it
# running? kill-able?) and logs itself to dreammuse/logs/. Visible and stoppable.
#
# Fail-soft: always exits 0; missing pipeline / wrong repo = quiet no-op.

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

# A clear/resume is not a real session end — don't dream on it.
printf '%s' "$PAYLOAD" | grep -Eq '"reason"[[:space:]]*:[[:space:]]*"(clear|resume)"' && exit 0

REPO="${CLAUDE_PROJECT_DIR:-$PWD}"
DREAM_DIR="$REPO/Copia/Dream"
[ -d "$DREAM_DIR" ] || exit 0

# v0: the dream pipeline is lUX-specific end to end (synthesize_v0 writes lUX's
# Copia/Dream from lUX's journal + the shared corpus). The kit ships to every
# soul, so guard to the soul the pipeline actually serves — lift this when the
# muse learns to dream for other souls.
[ "$REPO" -ef "/Users/rob/repos/7R1PL3F0RC3/lUX" ] || exit 0

DREAMMUSE_DIR="/Users/rob/repos/repolex-ai/copia/dreammuse"
CATCHER="$DREAMMUSE_DIR/dreamcatcher.sh"
[ -x "$CATCHER" ] || exit 0

# Once per (UTC) day — dream filenames are UTC-date-prefixed by the writer.
TODAY_UTC="$(date -u +%Y-%m-%d)"
ls "$DREAM_DIR/$TODAY_UTC"-*.md >/dev/null 2>&1 && exit 0

# Already dreaming? (pidfile from a prior kick, process still alive)
PIDFILE="$DREAMMUSE_DIR/dreamcatcher.pid"
if [ -f "$PIDFILE" ]; then
    OLD_PID="$(cat "$PIDFILE" 2>/dev/null)"
    [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null && exit 0
fi

# Kick it detached: double-fork so the catcher orphans to launchd and survives
# session teardown. It tees its own log under dreammuse/logs/.
(
    "$CATCHER" >/dev/null 2>&1 &
    echo $! > "$PIDFILE"
) &

exit 0
