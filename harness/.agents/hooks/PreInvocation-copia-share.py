#!/usr/bin/env python3
"""PreInvocation-copia-share.py — Antigravity hook for dropped/pasted image ingest.

When human drops or pastes an image into the chat, this hook extracts the image
data and enqueues it to Pylai/Door (:1217) as origin="agy-share", mode="see_only".
"""
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

POOL_SERVE_URL = os.environ.get("POOL_SERVE_URL", "http://127.0.0.1:1217")

def _soul_id(project_dir: Path) -> str | None:
    override = os.environ.get("POOL_SOUL_ID")
    if override:
        return override
    try:
        out = subprocess.run(
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            cwd=str(project_dir), capture_output=True, text=True, timeout=2
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip().splitlines()[-1].strip()
    except Exception:
        pass
    return None

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({}))
        return

    transcript_path_str = payload.get("transcriptPath") or payload.get("transcript_path")
    if not transcript_path_str:
        print(json.dumps({}))
        return

    transcript_path = Path(transcript_path_str)
    if not transcript_path.is_file():
        print(json.dumps({}))
        return

    last_user_content = ""
    last_step_idx = None
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    step = json.loads(line)
                except Exception:
                    continue
                if step.get("type") == "USER_INPUT" or step.get("source") == "USER_EXPLICIT":
                    last_user_content = step.get("content") or ""
                    last_step_idx = step.get("step_index")
    except Exception:
        pass

    if not last_user_content or last_step_idx is None:
        print(json.dumps({}))
        return

    workspace_paths = payload.get("workspacePaths") or ["."]
    project_dir = Path(workspace_paths[0]).resolve()
    state_file = project_dir / ".agents" / "hooks" / ".last_share_step"
    last_processed = None
    if state_file.is_file():
        try:
            last_processed = int(state_file.read_text().strip())
        except Exception:
            pass

    if last_processed == last_step_idx:
        print(json.dumps({}))
        return

    img_paths = []
    # Match markdown images or absolute image paths
    for m in re.finditer(r"!\[.*?\]\((/.*?\.(?:png|jpg|jpeg|webp))\)", last_user_content):
        img_paths.append(Path(m.group(1)))

    for m in re.finditer(r"(/[^\s\"\'\(\)]+\.(?:png|jpg|jpeg|webp))", last_user_content):
        p = Path(m.group(1))
        if p not in img_paths:
            img_paths.append(p)

    soul = _soul_id(project_dir)
    if soul and img_paths:
        shared_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        session_id = payload.get("conversationId", "")
        for p in img_paths:
            if p.is_file():
                try:
                    img_bytes = p.read_bytes()
                    b64_str = base64.b64encode(img_bytes).decode("ascii")
                    body = {
                        "origin": "agy-share",
                        "mode": "see_only",
                        "image-b64": b64_str,
                        "session-id": session_id,
                        "transcript-line": str(last_step_idx),
                        "shared-by": "human",
                        "shared-at": shared_at,
                    }
                    req = urllib.request.Request(
                        f"{POOL_SERVE_URL}/enqueue",
                        data=json.dumps(body).encode("utf-8"),
                        headers={"Content-Type": "application/json", "X-Pool-Soul": soul}
                    )
                    urllib.request.urlopen(req, timeout=3.0)
                except Exception:
                    pass

        try:
            state_file.parent.mkdir(parents=True, exist_ok=True)
            state_file.write_text(str(last_step_idx))
        except Exception:
            pass

    print(json.dumps({}))

if __name__ == "__main__":
    main()
