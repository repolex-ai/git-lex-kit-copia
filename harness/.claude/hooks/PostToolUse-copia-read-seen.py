#!/usr/bin/env python3
"""Companion to PostToolUse-copia-read-seen.sh (kit-copia) — the logic half.

The .sh is the registered hook (only .sh files fire); it runs the opt-out guard +
cheap string pre-filters, then pipes the PostToolUse payload here on stdin with
the soul repo root as argv[1]. This half: parse, guard, resolve, show.

read = seen: a successful Read of a Pool image blob becomes a main_image set on
the copia shared window — through the server's gated surface (X-Copia-Client:
cosee => actor=familiar, every pull teed to the human's cosee log, and the cosee
OFF switch refuses the push structurally). Cross-soul guard is FAIL-CLOSED: the
server's bound genesis must equal this repo's .lex/identity.yml genesis_sha, or
nothing is pushed (copia serving another soul's window must never show this
agent's looks). Fail-soft always: every path exits 0; messages go to stdout and
the .sh routes them to stderr (server down / 403 warn gently, wrong-soul and
not-in-pool skip quietly).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import NoReturn

TAG = "[copia read-seen]"
TIMEOUT = 2.0   # everything is loopback; a down server refuses instantly, no hang


def quit(msg=None) -> NoReturn:
    if msg:
        print(f"{TAG} {msg}")
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        quit()
    if payload.get("tool_name") != "Read":
        quit()
    fp = str((payload.get("tool_input") or {}).get("file_path") or "")
    # the Pool image blob layout, shared by every soul:
    # .../blob/image/YYYY/MM/DD/<stem>.<ext>
    m = re.search(r"/blob/image/\d{4}/\d{2}/\d{2}/([^/]+\.(?:png|jpg|jpeg|webp))$", fp)
    if not m:
        quit()
    basename = m.group(1)

    # ── the server, its token, this soul ────────────────────────────────────
    port = os.environ.get("COPIA_API_PORT")
    if not port:
        try:
            mc = json.loads(
                (Path.home() / ".config/copia/machine_config.json").read_text())
            port = str(mc.get("server_port") or 8788)
        except Exception:
            port = "8788"
    base = f"http://127.0.0.1:{port}"
    # the Familiar's hand: actor=familiar, teed, cosee-off gated
    headers = {"X-Copia-Client": "cosee"}
    try:
        headers["X-Copia-Token"] = (
            Path.home() / ".config/copia/session_token").read_text().strip()
    except Exception:
        pass   # no token file → the 403 below says so, once

    own_genesis = None
    try:
        repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
        for line in (repo / ".lex/identity.yml").read_text().splitlines():
            if line.strip().startswith("genesis_sha:"):
                own_genesis = line.split(":", 1)[1].strip().strip('"').strip("'")
                break
    except Exception:
        pass
    if not own_genesis:
        quit("no .lex/identity.yml genesis in this repo — look not shared "
             "(no identity, no push)")

    def call(path, data=None):
        req = urllib.request.Request(
            base + path, headers=dict(headers),
            data=(json.dumps(data).encode() if data is not None else None))
        if data is not None:
            req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode() or "{}")

    # ── guard, resolve, show ────────────────────────────────────────────────
    try:
        souls = call("/ui/view/souls")
        if souls.get("genesis") != own_genesis:
            quit()   # copia is serving another soul — correct result is NO push
        cid = (call("/ui/view/cid-for-file?file="
                    + urllib.parse.quote(basename)) or {}).get("cid")
        if not cid:
            quit()   # not in this soul's pool graph (or not walked yet)
        call("/ui/control/main_image", {"value": cid})
    except urllib.error.HTTPError as e:
        if e.code == 403:
            quit("403 from copia (cosee off, or stale session token) — "
                 "look not shared")
        quit()
    except Exception:
        quit("copia not running — look not shared this turn")
    quit()


if __name__ == "__main__":
    main()
