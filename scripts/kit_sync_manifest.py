#!/usr/bin/env python3
"""
Собрать kit-sync/manifest.json — только в репозитории workspace_kit.

Использование:
  python3 scripts/kit_sync_manifest.py [kit_version]

Перед релизом обновите kit-sync/artifacts/ (снимок workspace_kit.md и скрипты).
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT_SYNC = ROOT / "kit-sync"
ARTIFACTS = KIT_SYNC / "artifacts"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


# dest в пилоте ← src в kit-sync/artifacts/
ARTIFACT_MAP = [
    (
        "workspace-kit-doc",
        "workspace/reports/kit-remote-workspace_kit.md",
        "artifacts/workspace_kit.md",
        0,
        "kit_managed",
    ),
    ("kit-common", "scripts/kit_common.py", "artifacts/scripts/kit_common.py", 3, "kit_managed"),
    ("kit-sync", "scripts/kit_sync.py", "artifacts/scripts/kit_sync.py", 3, "kit_managed"),
    ("kit-learning-issue", "scripts/kit_learning_issue.py", "artifacts/scripts/kit_learning_issue.py", 3, "kit_managed"),
    ("kit-log-utils", "scripts/log_utils.py", "artifacts/scripts/log_utils.py", 3, "kit_managed"),
    ("cmd-kit-sync", ".cursor/commands/kit-sync.md", "artifacts/.cursor/commands/kit-sync.md", 3, "kit_managed"),
    ("cmd-kit-submit", ".cursor/commands/kit-submit.md", "artifacts/.cursor/commands/kit-submit.md", 3, "kit_managed"),
    (
        "rule-starter-kit-learnings",
        ".cursor/rules/starter-kit-learnings.mdc",
        "artifacts/.cursor/rules/starter-kit-learnings.mdc",
        3,
        "kit_managed",
    ),
]


def main() -> int:
    kit_version = "1.9"
    if len(sys.argv) > 1:
        kit_version = sys.argv[1]

    artifacts = []
    for art_id, dest, src, stage_min, mode in ARTIFACT_MAP:
        src_path = KIT_SYNC / src
        if not src_path.is_file():
            print(f"MISSING {src_path}", file=sys.stderr)
            return 1
        artifacts.append({
            "id": art_id,
            "dest": dest,
            "src": f"kit-sync/{src}",
            "sha256": sha256_file(src_path),
            "stage_min": stage_min,
            "mode": mode,
        })

    manifest = {
        "schema": 1,
        "kit_version": kit_version,
        "released_at": datetime.now().isoformat(),
        "changelog": "Kit-sync v1.9: workspace_kit.md snapshot + скрипты pull/push из пилота.",
        "artifacts": artifacts,
    }

    KIT_SYNC.mkdir(parents=True, exist_ok=True)
    out = KIT_SYNC / "manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out} kit_version={kit_version} artifacts={len(artifacts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
