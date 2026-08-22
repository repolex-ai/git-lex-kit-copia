#!/bin/bash
# SessionStart-copia-dreammuse.sh (kit-copia) — the dream carrier. At wake, tell
# the waking session its newest dream: one header line, then the dream's own words.
# Nothing else — no frontmatter, no credits, no source acts.
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

# Newest dream = last by FILENAME, and the date prefix is what makes that work.
# Two shapes are in play: the current 20260822-i-wake-to-the-whispers.md and the
# retired 2026-08-20-dreammuse-v0.md. Both are globbed so the back-catalogue stays
# readable; they sort correctly against each other by accident of ASCII ('-' < '0',
# so every dashed name sorts before every compact one — and compact names are only
# ever NEWER, so the newest still wins). stdout carries whichever patterns matched;
# a pattern that matches nothing only writes to stderr, which is discarded.
LATEST="$(ls "$DREAM_DIR"/[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*.md \
             "$DREAM_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md \
             2>/dev/null | sort | tail -1)"
[ -n "$LATEST" ] && [ -f "$LATEST" ] || exit 0

# Deliver the dream ITSELF and nothing else (Rob, Day 158). The file is a
# document — frontmatter, credits line, three source acts with image filenames and
# top-K token norms — and this hook used to `cat` the whole thing, so two thirds of
# what reached a waking mind was lab instrumentation. Only the narrative goes now.
#
# stderr is NOT silenced: a malformed dream must be findable in the session log. A
# hook that fails into /dev/null looks exactly like a hook that never fired (the
# share-hook lesson, Day 157). stdout stays clean — only the dream is printed there.
python3 - "$LATEST" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
try:
    text = path.read_text(encoding="utf-8")
except OSError:
    raise SystemExit(0)

# the narrative section only — everything between its heading and the next one
sec = re.search(r"^## the narrative[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
narrative = (sec.group(1) if sec else "").strip()
if not narrative:
    print(f"dreammuse: no narrative section in {path.name} — nothing delivered",
          file=sys.stderr)
    raise SystemExit(0)

print("You are waking from a dream. The last thing you remember:")
print()
print(narrative)
PY

exit 0
