#!/usr/bin/env python3
"""PreInvocation-copia-coview.py — Antigravity hook to inject current shared view.

Fetches the active frame and caption from the CoPIA server and injects an
ephemeral message so the agent sees what Rob is seeing in real-time.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({}))
        return

    # Read token and port
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

    headers = {"X-Copia-Client": "cosee"}
    if token:
        headers["X-Copia-Token"] = token

    url = f"http://127.0.0.1:{port}/ui/view/pairsee"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            moment_id = data.get("momentId") or data.get("mid")
            filepath = data.get("filepath") or data.get("file")
            caption = data.get("caption")
            if moment_id or filepath:
                msg = f"[cosee hook]\nmomentId: {moment_id or '·'}\nfilepath: {filepath or '·'}\ncaption: {caption or '·'}"
                print(json.dumps({
                    "injectSteps": [
                        {"ephemeralMessage": msg}
                    ]
                }))
                return
    except Exception:
        pass

    print(json.dumps({}))

if __name__ == "__main__":
    main()
