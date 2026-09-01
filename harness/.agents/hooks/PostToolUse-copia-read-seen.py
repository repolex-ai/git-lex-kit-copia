#!/usr/bin/env python3
"""PostToolUse-copia-read-seen.py — Antigravity hook for read-seen teeing.

When the agent inspects an image blob in the Pool via `view_file`,
this hook pushes the image to CoPIA's main_image control so Rob's screen
updates to mirror what the agent is looking at.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({}))
        return

    # Check tool call
    tool_call = payload.get("toolCall") or {}
    args = tool_call.get("args") or {}
    fp = str(args.get("AbsolutePath") or args.get("file_path") or args.get("path") or "")

    m = re.search(r"/blob/image/\d{4}/\d{2}/\d{2}/([^/]+\.(?:png|jpg|jpeg|webp))$", fp)
    if not m:
        print(json.dumps({}))
        return
    basename = m.group(1)

    port = os.environ.get("COPIA_API_PORT")
    if not port:
        try:
            mc = json.loads((Path.home() / ".config/copia/machine_config.json").read_text())
            port = str(mc.get("server_port") or 8788)
        except Exception:
            port = "8788"

    token = ""
    try:
        token = (Path.home() / ".config/copia/session_token").read_text().strip()
    except Exception:
        pass

    headers = {"X-Copia-Client": "cosee", "X-Copia-Source": "read-seen", "Content-Type": "application/json"}
    if token:
        headers["X-Copia-Token"] = token

    base = f"http://127.0.0.1:{port}"
    try:
        # Resolve cid
        req_cid = urllib.request.Request(
            f"{base}/ui/view/cid-for-file?file={urllib.parse.quote(basename)}",
            headers=headers
        )
        with urllib.request.urlopen(req_cid, timeout=2.0) as r:
            res = json.loads(r.read().decode("utf-8"))
            cid = res.get("cid")

        if cid:
            req_set = urllib.request.Request(
                f"{base}/ui/control/main_image",
                data=json.dumps({"value": cid}).encode("utf-8"),
                headers=headers
            )
            urllib.request.urlopen(req_set, timeout=2.0)
    except Exception:
        pass

    print(json.dumps({}))

if __name__ == "__main__":
    main()
