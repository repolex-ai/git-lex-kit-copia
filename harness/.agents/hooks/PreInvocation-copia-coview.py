#!/usr/bin/env python3
"""PreInvocation-copia-coview.py — Antigravity lifecycle hook for CoPIA co-viewing.

THE "PAPER WALL" BOUNDARY & PRIVACY CONTRACT:
CoPIA Studio is currently single-tenant: it connects to one soul repository at a
time (e.g. Selkie / lUX or another active squaddie). Because switching in the CoPIA
UI is manual, CoPIA may be displaying renders and private moments intended for a
different soul and the user.

To maintain soul privacy and prevent cross-agent data leaks, this hook enforces a
strict pre-flight identity check against CoPIA's `/ui/view/souls` endpoint:
  1. It inspects this soul repo's identity (genesis_sha in .lex/identity.yml or git root).
  2. It queries CoPIA for its currently connected soul (genesis_sha and soul_repo).
  3. ONLY when CoPIA is verified to be connected to THIS specific soul repository does
     it query `/ui/view/cosee-hook` to inject the active frame into the agent's turn.
  4. If CoPIA is connected to another soul (e.g. Selkie), disconnected, or offline,
     this hook immediately exits with `{}` (silent no-op). Zero prompt injection.

CRITICAL: Never attempt to programmatically redirect or switch CoPIA from this hook.
CoPIA connection is controlled exclusively by the user.
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def _get_my_identity(project_dir: Path) -> tuple[str | None, str]:
    """Returns (genesis_sha, repo_path_resolved) for this soul repository."""
    repo_resolved = str(project_dir.resolve())
    genesis = None

    # 1. Primary: read genesis_sha from .lex/identity.yml
    idf = project_dir / ".lex" / "identity.yml"
    if idf.is_file():
        try:
            for line in idf.read_text().splitlines():
                line = line.strip()
                if line.startswith("genesis_sha:"):
                    genesis = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if genesis:
                        break
        except Exception:
            pass

    # 2. Fallback: query git root commit
    if not genesis:
        try:
            out = subprocess.run(
                ["git", "rev-list", "--max-parents=0", "HEAD"],
                cwd=str(project_dir),
                capture_output=True,
                text=True,
                timeout=2,
            )
            if out.returncode == 0 and out.stdout.strip():
                genesis = out.stdout.strip().splitlines()[-1].strip()
        except Exception:
            pass

    return genesis, repo_resolved


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({}))
        return

    workspace_paths = payload.get("workspacePaths") or ["."]
    project_dir = Path(workspace_paths[0]).resolve()
    my_genesis, my_repo = _get_my_identity(project_dir)

    # Read CoPIA API port (default 8788)
    port = os.environ.get("COPIA_API_PORT")
    if not port:
        try:
            mc = json.loads((Path.home() / ".config/copia/machine_config.json").read_text())
            port = str(mc.get("server_port") or 8788)
        except Exception:
            port = "8788"

    # Read session token
    token = ""
    try:
        token = (Path.home() / ".config/copia/session_token").read_text().strip()
    except Exception:
        pass

    headers = {"X-Copia-Client": "cosee"}
    if token:
        headers["X-Copia-Token"] = token

    base_url = f"http://127.0.0.1:{port}"

    # ── Pre-flight Identity Check ─────────────────────────────────────────
    # Query /ui/view/souls to determine which soul CoPIA is actively serving.
    try:
        req_soul = urllib.request.Request(f"{base_url}/ui/view/souls", headers=headers)
        with urllib.request.urlopen(req_soul, timeout=1.0) as resp:
            state = json.loads(resp.read().decode("utf-8"))
    except Exception:
        # Server down, unreachable, or unauthorized — silently pass
        print(json.dumps({}))
        return

    if not state.get("connected"):
        # CoPIA is not connected to any soul pool
        print(json.dumps({}))
        return

    copia_genesis = state.get("genesis")
    copia_repo = state.get("soul_repo")

    # Verify identity match: either matching genesis SHA or matching resolved repo path
    is_my_soul = False
    if my_genesis and copia_genesis and my_genesis == copia_genesis:
        is_my_soul = True
    elif copia_repo and Path(copia_repo).resolve() == Path(my_repo).resolve():
        is_my_soul = True

    if not is_my_soul:
        # CoPIA is connected to another soul (e.g. Selkie/lUX).
        # SILENT NO-OP: Do not inject another soul's private visual moments.
        print(json.dumps({}))
        return

    # ── Fetch Co-view Frame ───────────────────────────────────────────────
    # CoPIA is confirmed connected to THIS soul. Fetch the active frame for the sender.
    soul_name = project_dir.name
    url = f"{base_url}/ui/view/cosee-hook?sender={urllib.parse.quote(soul_name)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            text = resp.read().decode("utf-8").strip()
            if text and "momentId: ·" not in text:
                print(json.dumps({
                    "injectSteps": [
                        {"ephemeralMessage": text}
                    ]
                }))
                return
    except Exception:
        pass

    print(json.dumps({}))


if __name__ == "__main__":
    main()
