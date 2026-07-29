#!/usr/bin/env python3
"""UserPromptSubmit-copia-coview.py — the cosee hook (UserPromptSubmit).

!!! GRUE WARNING — EDIT LOCALLY, THEN PUSH TO THE KIT. ALWAYS. !!!
    We develop and test hooks HERE, locally — that's the workflow. But the kit
    is the managed source of truth: the moment a local edit works, you MUST push
    it up into the kit that owns this hook (repolex-ai/git-lex-kit-copia,
    harness/.claude/hooks/UserPromptSubmit-copia-coview.py) and commit+push the
    kit — same sitting, no "later". A local edit that never reaches the kit is
    unmanaged drift: the next `git lex kit-update` on any repo silently ships the
    STALE kit version and someone runs the wrong hook (this exact drift bit us
    Day 119 — the kit was still shipping the retired /api/shared-view hook this
    file had already replaced). Loop: edit+test here -> copy to kit -> commit &
    push kit. Leave the loop open and a hungry grue eats you in the dark.

The hook end of the cosee tee (Rob's nomenclature, ratified Day 114: cosee =
the umbrella surface; cosee hook = this; cosee cli = the tool; co-steer = acting
on shared controls). The other end is the cosee tab in the copia UI. THIS end
staples the composed payload — ONE string, rendered once — into each of the
Familiar's turns; the tab displays the same string verbatim. Byte-identical by
construction: what the Familiar reads is literally what the Human's tab shows.

Replaces the original co-view hook, which called /api/shared-view — retired in
f7e0afd — and predated the Day-106 session gate (it sent no token, so even a live
endpoint would have 403'd it).

Behavior:
  1. DUMB PIPE. All policy lives server-side: /ui/view/cosee-hook returns empty
     when cosee is OFF, the composed hook_text when ON, and a visible
     "[cosee-hook compose failed: …]" line when the composer breaks. The hook
     staples whatever text arrives, verbatim (tee invariant: never re-render).
  2. AUTHENTICATED. Sends the per-boot session token (X-Copia-Token, read from the
     0600 file the server mints) + X-Copia-Client: coview-hook (a Familiar-side
     client, like cosee).
  3. SUPPRESS ON NO-CHANGE. Same payload text as the last prompt → emit nothing
     (nothing moved → no new info). State in .UserPromptSubmit-copia-coview.last.json.
  4. FAIL-SOFT, BUT LEGIBLY (the Day-113 lesson: silence indistinguishable from
     "off" is a null signal). Server down/unreachable → silent (copia's just not
     running). 403 → ONE stderr line (stale token = a real, fixable break) then
     exit 0. Any other surprise → silent exit 0, never block a prompt.

Emits the standard UserPromptSubmit additionalContext JSON on stdout, and ONLY
that. Prints nothing when there's nothing to say.
"""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PORT = os.environ.get("COPIA_API_PORT", "8788")
BASE = f"http://127.0.0.1:{PORT}"
STATE = Path(__file__).resolve().parent / ".UserPromptSubmit-copia-coview.last.json"
TOKEN_PATH = Path.home() / ".config" / "copia" / "session_token"
TIMEOUT = 3.5  # the compose is registry reads + (memoized) Door lookups; if CoPIA
#                can't answer in 3.5s it's wedged → skip this turn.

# The staple switch (one switch, nothing hidden). Panel-first phase ran 2026-07-24;
# Rob signed the panel off (byte-identical verbatim display, event-only writes,
# send wash, provenance) and enabled the Familiar side same day: "Want to enable
# the staple, and we'll start trying it on for size?"
STAPLE_TO_FAMILIAR = True


def _get_hook_text():
    """GET /ui/view/cosee-hook — the composed hook_text, "" when cosee is
    off, or None when the server is down/unreachable. A 403 warns on stderr (stale
    token is a real break, not an off-state) and returns None. Never raises."""
    headers = {"X-Copia-Client": "coview-hook"}
    try:
        headers["X-Copia-Token"] = TOKEN_PATH.read_text().strip()
    except Exception:
        pass  # no token file → server will 403 and we warn below
    try:
        # sign the fetch with this script's real name — the tab's "by …" provenance
        sender = urllib.parse.quote(Path(__file__).name)
        req = urllib.request.Request(
            BASE + "/ui/view/cosee-hook?sender=" + sender, headers=headers)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("[cosee-hook] 403 from copia — session token stale or missing "
                  f"({TOKEN_PATH}); restart mints a fresh one", file=sys.stderr)
        return None
    except Exception:
        return None  # copia not running → silent


def _changed(text):
    """True if `text` differs from the last stapled payload (then remembers it)."""
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    try:
        if json.loads(STATE.read_text()).get("digest") == digest:
            return False
    except Exception:
        pass
    try:
        STATE.write_text(json.dumps({"digest": digest}))
    except Exception:
        pass
    return True


def main():
    # drain stdin (the UserPromptSubmit payload) so we don't leave it dangling for
    # a downstream emitter sharing the pipe; we don't need its contents.
    try:
        sys.stdin.read()
    except Exception:
        pass

    text = _get_hook_text()   # fires the tee → the panel gets this delivery
    if not STAPLE_TO_FAMILIAR:
        return 0          # panel-first phase: nothing enters the Familiar's turn
    if not text:          # None (down/403) or "" (co-seeing off) → nothing to say
        return 0
    if not _changed(text):
        return 0          # same payload as last prompt → no new info

    context = (
        "cosee hook — what Rob is looking at, frozen at send (the same string "
        "his cosee tab shows, byte-identical):\n" + text
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
