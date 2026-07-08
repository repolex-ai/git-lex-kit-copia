#!/usr/bin/env python3
"""UserPromptSubmit-copia-coview.py — the CoPIA co-view hook (UserPromptSubmit).

Part of the copia co-view hook UNIT (git-lex-kit-copia territory). The naming is a
functional group: this fires on UserPromptSubmit, belongs to the copia app, and
does co-view. Its server side (the flag + the /api/shared-view scene) lives in
copia's api server; its UI side is the 👁 co-seeing chip.

Staples "what Rob is looking at right now" into each prompt so lUX SEES WHAT ROB
SEES — the caption the eye wrote + the scene grammar + the cast — without a
separate curl or filesystem archaeology. Frozen at the moment Rob hit enter.

This is the immediacy half of the CoPIA shared window
(docs/2026_07_02_COPIA_UI_VISION.md, VIEW-CONTEXT HOOK spec). The shared-window
endpoint already assembles everything; this hook is a THIN HTTP CLIENT that asks
the room and formats one human-meaningful block. All state lives server-side.

Behavior (all four are the spec):
  1. FIRES ONLY WHEN CO-SEEING IS ON. The UI has an on/off affordance that writes
     a server flag (coview_enabled). ON when we're looking together; OFF when
     building (heads-down in code) so view-lines don't clutter context. Absent
     server / flag off → silent no-op.
  2. ONE CAPTION BLOCK, human-meaningful, not raw JSON: the frame id + scene
     spine (location · mood · posture) + the caption sentence + cast + origin.
  3. SUPPRESS ON NO-CHANGE. If the current frame == the frame reported at the
     LAST prompt, emit nothing (Rob hasn't moved his gaze → no new info). State
     kept in .UserPromptSubmit-copia-coview.last.json next to this script.
  4. FAIL-SOFT. Any error → emit nothing, exit 0. Never block or pollute a prompt.

Emits the standard UserPromptSubmit additionalContext JSON on stdout, and ONLY
that (so it can be the sole stdout emitter in its hook slot). Prints nothing when
there's nothing to say.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

PORT = os.environ.get("COPIA_API_PORT", "8788")
BASE = f"http://127.0.0.1:{PORT}"
STATE = Path(__file__).resolve().parent / ".UserPromptSubmit-copia-coview.last.json"
TIMEOUT = 3.5  # frozen at send — a little latency on a prompt is fine; shared-view
#                with ?echo=1 (view + scene + cast + a vector search for the rhyme)
#                runs ~1.5s warm. If CoPIA can't answer in 3.5s it's wedged → skip.


def _get_shared_view():
    """GET /api/shared-view?echo=1 — returns the parsed dict, or None if CoPIA is
    down / unreachable / slow. echo=1 asks the server for the current frame's rhyme
    (the Echo) so I can offer to bring a related memory forward. Never raises."""
    try:
        req = urllib.request.Request(BASE + "/api/shared-view?echo=1",
                                     headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def _last_frame():
    try:
        return json.loads(STATE.read_text()).get("frame")
    except Exception:
        return None


def _remember_frame(frame):
    try:
        STATE.write_text(json.dumps({"frame": frame}))
    except Exception:
        pass


def _fmt_block(view):
    """Format the one human-meaningful co-view block from a /api/shared-view dict.
    Returns the text, or None if there's nothing worth saying."""
    current = view.get("current")
    if not current:
        return None
    frame = Path(current).name  # 2026/07/02/20260702-172304-933a9b5d.png → filename
    short = frame.rsplit("-", 1)[-1].replace(".png", "") if "-" in frame else frame

    scene = view.get("scene") or {}
    cast = [c for c in (view.get("cast") or []) if c]
    following = view.get("following", True)
    origin = None
    for s in (view.get("strip") or []):
        if s.get("file") == current:
            origin = s.get("origin")
            break

    # who put it on screen (from the co-view log tail) — 'you'/'the loop'/'I'.
    # ONE clause that already carries the follow-state, so we never append a
    # redundant "— pinned" on top of "you pinned".
    by = None
    for ev in reversed(view.get("coview") or []):
        if ev.get("file") and Path(ev["file"]).name == frame:
            by = ev.get("by")
            break
    if by == "rob":
        who = "you're watching" if following else "you pinned"
    elif by == "loop":
        who = "the flow just rendered"
    elif by == "lux":
        who = "I surfaced"
    else:
        who = "on the live edge" if following else "pinned to"

    # the glanceable spine: location · mood · posture (only the ones present)
    spine = " · ".join(v for v in (scene.get("location"), scene.get("mood"),
                                   scene.get("posture")) if v)
    head = f"[co-view] {who} {short}"
    if spine:
        head += f" ({spine})"

    lines = [head]
    caption = scene.get("caption")
    if caption:
        lines.append(f'  "{caption.strip()}"')
    # a second detail row for what the caption prose might not carry crisply
    detail = []
    if scene.get("lighting"):
        detail.append(f"light: {scene['lighting']}")
    if scene.get("camera") or scene.get("framing"):
        detail.append("shot: " + " / ".join(
            v for v in (scene.get("camera"), scene.get("framing")) if v))
    if scene.get("gaze"):
        detail.append(f"gaze: {scene['gaze']}")
    if detail:
        lines.append("  " + "  |  ".join(detail))
    meta = []
    if cast:
        meta.append("cast: " + " · ".join(cast))
    if origin:
        meta.append(f"origin: {origin}")
    if meta:
        lines.append("  " + "  |  ".join(meta))
    # THE ECHO (Day 95) — the strongest meaningful rhyme of the current frame,
    # delivered right here in the conversation so I can offer to bring it forward
    # ("this rhymes with the forest morning — want it up?"). One line, only when the
    # server found a real rhyme (semantic neighbor, not a near-dup). This is the
    # remembering-machine's shoulder-tap arriving in my turn, actionable by either hand.
    echo = view.get("echo")
    if echo and echo.get("caption"):
        tb = echo.get("thread_back") or "another time"
        cap = echo["caption"].strip()
        cap = cap if len(cap) <= 160 else cap[:160].rstrip() + "…"
        lines.append(f"  ↺ echoes {tb} (rhyme {echo.get('score')}): {cap}")
        lines.append("    (offer to bring it on screen if it fits the moment)")
    return "\n".join(lines)


def main():
    # drain stdin (the UserPromptSubmit payload) so we don't leave it dangling for
    # a downstream emitter sharing the pipe; we don't need its contents.
    try:
        sys.stdin.read()
    except Exception:
        pass

    view = _get_shared_view()
    if not view:
        return 0  # CoPIA down → silent

    # 1. flag gate — only speak when co-seeing is ON
    if not (view.get("coview_enabled") or {}).get("enabled", False):
        return 0

    block = _fmt_block(view)
    if not block:
        return 0

    # 3. suppress on no-change — same frame as last prompt → say nothing
    current = view.get("current")
    frame = Path(current).name if current else None
    if frame and frame == _last_frame():
        return 0
    _remember_frame(frame)

    context = (
        "What Rob is looking at in CoPIA right now (view-context hook — the shared "
        "window, frozen at send; you're seeing what he sees so you don't have to "
        "query):\n" + block
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
