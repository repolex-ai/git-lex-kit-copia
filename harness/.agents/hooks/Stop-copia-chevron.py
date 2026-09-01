#!/usr/bin/env python3
"""Stop-copia-chevron.py — Antigravity lifecycle hook to extract and enqueue chevrons.

When an agent turn ends with `>> ... <<` chevrons in its output, this hook extracts
them from the transcript JSONL and enqueues them via `coquette`.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CHEVRON_RE = re.compile(r">>([\s\S]*?)<<")

def find_copia_repo(project_dir: Path) -> Path | None:
    candidates = [
        project_dir / ".." / "copia",
        Path.home() / "repos" / "repolex-ai" / "copia",
        Path.home() / "repos" / "copia",
    ]
    for c in candidates:
        if c.resolve().is_dir():
            return c.resolve()
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

    # Find the last MODEL / PLANNER_RESPONSE turn
    last_model_content = ""
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
                if step.get("type") == "PLANNER_RESPONSE" or step.get("source") == "MODEL":
                    content = step.get("content") or ""
                    last_model_content = content
                    last_step_idx = step.get("step_index")
    except Exception:
        pass

    if not last_model_content or last_step_idx is None:
        print(json.dumps({}))
        return

    workspace_paths = payload.get("workspacePaths") or ["."]
    project_dir = Path(workspace_paths[0]).resolve()
    state_file = project_dir / ".agents" / "hooks" / ".last_chevron_step"
    last_processed = None
    if state_file.is_file():
        try:
            last_processed = int(state_file.read_text().strip())
        except Exception:
            pass

    if last_processed == last_step_idx:
        print(json.dumps({}))
        return

    chevrons = CHEVRON_RE.findall(last_model_content)
    if chevrons:
        copia_dir = find_copia_repo(project_dir)
        for raw_chev in chevrons:
            clean_chev = f">> {raw_chev.strip()} <<"
            cmd = ["uv", "run"]
            if copia_dir:
                cmd.extend(["--project", str(copia_dir)])
            cmd.extend(["coquette", "chevron", clean_chev])
            try:
                subprocess.run(cmd, cwd=str(project_dir), capture_output=True, timeout=10)
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
