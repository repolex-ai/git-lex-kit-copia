"""UserPromptSubmit-copia-share.py — pasted/dropped images → the Pool queue.

Sibling helper to UserPromptSubmit-copia-share.sh (git-lex hook-authoring:
same stem, .py extension; the .sh is the hook, this is its logic). STDLIB
ONLY, on purpose: v1 of this hook died of a moved checkout — its .sh cd'd
into a copia repo that no longer held the code, and every paste failed
silently for weeks. This version depends on nothing but python3 and the Door.

What it does: when a human pastes or drops an image into a Claude Code
session, enqueue it to the Pool Door as origin='claude-code-share',
mode='see_only' — the eye SEEs it, captions it, homes it as a Moment. The
wire shape mirrors copia.lib.poolqueue.producers.claude_code_share() exactly;
the Door is the validating authority (no client-side SHACL here, by design —
see PoolQueue.enqueue's validate docstring: the Door remains the authority).

On the name: 'share' means HANDED TO THIS SOUL through the harness — not
shared with other souls. The origin value says where the pixels came from.

Why the transcript, not the clipboard: Claude Code hands hooks no attachment
path — pasted images are base64-embedded inline in the transcript JSONL. The
hook payload's transcript_path is the only durable handle, so we read the
record, not the location.

Soul routing: the queue is per-soul, keyed by the soul repo's genesis sha
(verified: lUX's genesis == the poolqueue client's soul id). We derive it
from the project dir git history — the hook is soul-portable with zero
config. POOL_SOUL_ID / POOL_SERVE_URL env override both ends.

Battle-tested logic carried from v1 (Day 62), verbatim in spirit:
  - match the image-bearing turn by IDENTITY, not position (tool_results are
    recorded as type:"user" lines; a later text prompt can land after the
    image turn)
  - poll ~3s for the transcript flush (the hook can fire before Claude Code
    writes the turn — the race that ate the sky)
  - per-session marker so a re-fire never double-enqueues

Usage:
    python3 UserPromptSubmit-copia-share.py <project_dir>       # hook JSON on stdin
    python3 ...-share.py <project_dir> --transcript X.jsonl --dry-run
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

POOL_SERVE_URL = os.environ.get("POOL_SERVE_URL", "http://127.0.0.1:8424")


# ── finding the image-bearing turn ────────────────────────────────────────────

def _image_blocks(content: list) -> list[dict]:
    """The base64 image blocks in a content list. Only source.type=='base64' —
    a 'file' source (rare) would be a path handled differently; not seen in
    the wild for paste/drop."""
    out = []
    for b in content:
        if not isinstance(b, dict) or b.get("type") != "image":
            continue
        src = b.get("source")
        if isinstance(src, dict) and src.get("type") == "base64" and src.get("data"):
            out.append(src)
    return out


def _last_user_turn(transcript: Path):
    """(line_index, content_blocks) of the most recent human prompt that
    actually CARRIES a base64 image; None if none does. Skip tool_result
    lines (recorded as type:'user' but not human) and text-only prompts —
    match by the image itself, not by position."""
    last = None
    try:
        with transcript.open() as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if o.get("type") != "user":
                    continue
                msg = o.get("message")
                content = msg.get("content") if isinstance(msg, dict) else None
                if not isinstance(content, list):
                    continue
                if any(isinstance(b, dict) and b.get("type") == "tool_result"
                       for b in content):
                    continue
                if _image_blocks(content):
                    last = (idx, content)
    except FileNotFoundError:
        return None
    return last


def _last_user_turn_waiting(transcript: Path, *, attempts: int = 7,
                            delay: float = 0.5):
    """_last_user_turn, patient about the read-after-write race: the hook can
    fire before Claude Code flushes this turn's image into the JSONL."""
    for i in range(attempts):
        turn = _last_user_turn(transcript)
        if turn is not None:
            return turn
        if i < attempts - 1:
            time.sleep(delay)
    return None


# ── per-session dedupe marker ─────────────────────────────────────────────────

def _marker(session_id: str) -> Path:
    return Path(tempfile.gettempdir()) / f"copia-share-hook.{session_id or 'nosession'}.last"


def _already_done(session_id: str, line_idx: int) -> bool:
    try:
        return _marker(session_id).read_text().strip() == str(line_idx)
    except FileNotFoundError:
        return False


def _mark_done(session_id: str, line_idx: int) -> None:
    try:
        _marker(session_id).write_text(str(line_idx))
    except OSError:
        pass  # marker is an optimization, never load-bearing


# ── soul routing + the enqueue POST ───────────────────────────────────────────

def _soul_id(project_dir: str) -> str:
    """The soul's queue key = its genesis sha. Env wins; else derived from the
    repo (tail line: a repo with several roots keeps its true genesis last)."""
    env = os.environ.get("POOL_SOUL_ID")
    if env:
        return env
    out = subprocess.run(
        ["git", "-C", project_dir, "rev-list", "--max-parents=0", "HEAD"],
        capture_output=True, text=True, timeout=10)
    roots = out.stdout.split()
    return roots[-1] if roots else ""


def _enqueue(body: dict, soul_id: str, *, timeout: int = 30) -> int:
    url = (POOL_SERVE_URL.rstrip("/") + "/queue/enqueue?"
           + urllib.parse.urlencode({"soul": soul_id}))
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        out = json.loads(r.read() or b"null")
    if not out or "id" not in out:
        raise RuntimeError(f"enqueue returned no id: {out!r}")
    return int(out["id"])


def process_transcript(transcript: Path, *, project_dir: str,
                       session_id: str = "", shared_by: str = "human",
                       wait: bool = False, dry_run: bool = False) -> list[int]:
    """Enqueue any images in the transcript's last image-bearing human turn.
    Returns queue ticket ids. A per-image failure is logged and skipped; the
    turn is only marked done when EVERY image landed, so a partial failure
    stays retryable by hand."""
    turn = (_last_user_turn_waiting if wait else _last_user_turn)(transcript)
    if turn is None:
        return []
    line_idx, content = turn
    if _already_done(session_id, line_idx):
        return []
    srcs = _image_blocks(content)
    if not srcs:
        _mark_done(session_id, line_idx)
        return []

    soul = _soul_id(project_dir)
    if not soul:
        print("copia-share: no soul id derivable — not enqueuing", file=sys.stderr)
        return []

    shared_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    tickets: list[int] = []
    for i, src in enumerate(srcs):
        # Flat wire body, mirroring poolqueue.claude_code_share() exactly.
        body = {
            "origin": "claude-code-share",
            "mode": "see_only",
            "image-b64": src["data"],
            "session-id": session_id,
            "transcript-line": str(line_idx),
            "shared-by": shared_by,
            "shared-at": shared_at,
        }
        if dry_run:
            shown = dict(body, **{"image-b64": f"<{len(src['data'])} b64 chars>"})
            print(f"copia-share[dry-run]: would POST soul={soul} {shown}",
                  file=sys.stderr)
            tickets.append(-1)
            continue
        try:
            t = _enqueue(body, soul)
            tickets.append(t)
            print(f"copia-share: enqueued ticket {t} "
                  f"({src.get('media_type', 'image/?')}, image {i + 1}/{len(srcs)})",
                  file=sys.stderr)
        except Exception as e:
            print(f"copia-share: enqueue failed for image {i}: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)

    if len(tickets) == len(srcs):
        _mark_done(session_id, line_idx)
    return tickets


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="copia-share")
    ap.add_argument("project_dir", help="the soul repo root ($CLAUDE_PROJECT_DIR)")
    ap.add_argument("--transcript", help="read this transcript instead of hook stdin JSON")
    ap.add_argument("--shared-by", default=os.environ.get("POOL_SHARED_BY", "human"))
    ap.add_argument("--dry-run", action="store_true",
                    help="print the would-be POSTs; send nothing")
    args = ap.parse_args(argv)

    if args.transcript:
        transcript = Path(args.transcript).expanduser()
        session_id, wait = "", False   # manual run: image already on disk
    else:
        try:
            payload = json.load(sys.stdin)
        except json.JSONDecodeError:
            print("copia-share: no/invalid hook JSON on stdin", file=sys.stderr)
            return 0   # never block the prompt on our own failure
        tp = payload.get("transcript_path")
        if not tp:
            return 0
        transcript = Path(tp).expanduser()
        session_id = payload.get("session_id", "")
        wait = True

    try:
        tickets = process_transcript(
            transcript, project_dir=args.project_dir, session_id=session_id,
            shared_by=args.shared_by, wait=wait, dry_run=args.dry_run)
    except Exception as e:
        # A share is a nicety; it must NEVER break the human's turn.
        print(f"copia-share: unexpected error (ignored): {type(e).__name__}: {e}",
              file=sys.stderr)
        return 0

    if tickets:
        print(f"copia-share: {len(tickets)} image(s) queued for the Pool",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
