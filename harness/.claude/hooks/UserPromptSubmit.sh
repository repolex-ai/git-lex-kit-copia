#!/bin/bash
# UserPromptSubmit hook (copia kit) — share dropped/pasted images into the Pool.
#
# Claude Code does not hand a hook the image a user pastes or drops; it embeds it
# as base64 inline in the session transcript. But every hook payload carries
# `transcript_path`, so copia.share_hook reads the transcript's last user turn,
# pulls any image blocks, decodes them, and ingests each as a 'share'-origin
# Moment (cid -> iris.see caption -> Pool blob tree).
#
# CRITICAL: this MUST NOT block the prompt. Ingest runs iris.see (~9s); we
# fire-and-forget via nohup and exit fast (<1s). The share lands in the Pool a
# few seconds later, invisibly. The hook reads the UserPromptSubmit JSON on
# stdin and forwards it to the detached worker.
#
# Ships in git-lex-kit-copia; `git lex kit-update` installs it to
# .claude/hooks/UserPromptSubmit.sh and registers it for the UserPromptSubmit
# event. Kit-namespace convention: a single kit shipping this CoPIA-only event
# needs no namespacing; if another kit also targets UserPromptSubmit, name the
# files UserPromptSubmit-<kit>-<purpose>.sh so both register (dedupe-by-command).

set -u

# Where the copia engine lives. Override via COPIA_REPO if installed elsewhere.
COPIA_REPO="${COPIA_REPO:-$HOME/repos/shoresinger/copia}"
LOG_DIR="${CLAUDE_PROJECT_DIR:-$PWD}/.claude"
FIRE_LOG="$LOG_DIR/share-hook-fires.log"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
mkdir -p "$LOG_DIR" 2>/dev/null || true

# Read the hook payload (UserPromptSubmit JSON) from stdin so we can forward it.
PAYLOAD="$(cat)"

if [ ! -d "$COPIA_REPO" ]; then
    echo "$TIMESTAMP share-hook: copia repo missing at $COPIA_REPO — skipping" >> "$FIRE_LOG" 2>/dev/null
    exit 0
fi

# Fire-and-forget: pipe the payload to the detached worker so iris.see (~9s)
# never blocks the prompt. The worker re-reads transcript_path + session_id from
# the JSON and homes any pasted images. All output to the worker's own stderr ->
# the fire log; stdout stays clean (UserPromptSubmit stdout is added to context).
(
    cd "$COPIA_REPO" || exit 0
    printf '%s' "$PAYLOAD" | nohup uv run --no-sync python -m copia.share_hook \
        >> "$FIRE_LOG" 2>&1
) &
disown 2>/dev/null || true

echo "$TIMESTAMP share-hook: dispatched worker (detached)" >> "$FIRE_LOG" 2>/dev/null

# Never emit to stdout (it would be injected into the model's context) and never
# block. Exit 0 immediately.
exit 0
