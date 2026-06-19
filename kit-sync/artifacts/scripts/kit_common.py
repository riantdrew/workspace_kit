#!/usr/bin/env python3
"""
Общие константы и утилиты для двустороннего sync с workspace_kit.

Сервер (канон): https://github.com/riantdrew/workspace_kit
Манифест: kit-sync/manifest.json (fallback: pilot-sync/manifest.json)
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = ROOT / "workspace"
INDEX_PATH = WORKSPACE / "INDEX.md"
LEARNINGS_PATH = WORKSPACE / "starter-kit-learnings.md"
PUSH_STATE_PATH = ROOT / "data" / "kit_learnings_sync.json"
SYNC_STATE_PATH = ROOT / "data" / "kit_sync_state.json"
BACKUP_DIR = WORKSPACE / "reports" / "kit-backups"

KIT_REPO = "riantdrew/workspace_kit"
KIT_OWNER, KIT_NAME = KIT_REPO.split("/")
KIT_RAW_BASE = f"https://raw.githubusercontent.com/{KIT_REPO}/main"
MANIFEST_URL = f"{KIT_RAW_BASE}/kit-sync/manifest.json"
MANIFEST_URL_LEGACY = f"{KIT_RAW_BASE}/pilot-sync/manifest.json"
WORKSPACE_KIT_URL = f"{KIT_RAW_BASE}/workspace_kit.md"
STARTER_KIT_URL = f"{KIT_RAW_BASE}/starter_kit.md"  # legacy alias

KIT_LABELS = ("kit-learning", "from-pilot", "anonymized")

PROTECTED_PULL_PREFIXES = (
    "workspace/SOUL.md",
    "workspace/USER.md",
    "workspace/GOALS.md",
    "workspace/MEMORY.md",
    "workspace/CONSTITUTION.md",
    "workspace/AUTONOMY.md",
    "workspace/BOOTSTRAP.md",
    "workspace/PROJECT.md",
    "workspace/knowledge/domain/",
    ".cursor/rules/constitution-enforce.mdc",
    ".cursor/rules/agent-knowledge.mdc",
    ".cursor/rules/security-git.mdc",
    ".cursor/rules/workspace-isolation.mdc",
    ".cursor/rules/workspace-read.mdc",
    ".env",
)

KIT_VERSION_RE = re.compile(r"\*\*Версия kit:\*\*\s*([\d.]+)", re.IGNORECASE)
KIT_VERSION_ALT = re.compile(r"kit_version[\"']?\s*[:=]\s*[\"']?([\d.]+)", re.IGNORECASE)

_REDACT_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"/Users/[^\s/]+"), "[HOME]"),
    (re.compile(r"/home/[^\s/]+"), "[HOME]"),
    (re.compile(r"https?://github\.com/[^\s\)]+"), "[github-url]"),
    (re.compile(r"git@github\.com:[^\s]+"), "[github-url]"),
    (re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"), "[email]"),
    (re.compile(r"\b(?:sk|ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"), "[token]"),
    (re.compile(r"\b[A-Za-z0-9]{32,}\b"), "[redacted-id]"),
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "[uuid]"),
]


def run_cmd(cmd: list[str], *, cwd: Path | None = None, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        cwd=str(cwd or ROOT),
    )


def which(name: str) -> str | None:
    result = run_cmd(["which", name])
    path = result.stdout.strip()
    return path if result.returncode == 0 and path else None


def gh_auth_status() -> tuple[bool, str]:
    if not which("gh"):
        return False, "GitHub CLI (gh) не установлен. Установите: https://cli.github.com/"
    result = run_cmd(["gh", "auth", "status"])
    if result.returncode != 0:
        msg = (result.stderr or result.stdout or "").strip()
        return False, f"GitHub не авторизован. Выполните: gh auth login\n{msg}"
    user_match = re.search(r"Logged in to github\.com account (\S+)", result.stdout)
    user = user_match.group(1) if user_match else "unknown"
    return True, f"Авторизован как {user}"


def fetch_url(url: str, *, timeout: int = 30) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "workspace-kit-sync/1.9"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, body
    except urllib.error.URLError as e:
        return 0, str(e.reason)


def fetch_kit_path(path: str) -> tuple[int, str]:
    """Загрузка файла с сервera kit: raw.githubusercontent, затем GitHub API."""
    norm = path.lstrip("/")
    status, body = fetch_url(f"{KIT_RAW_BASE}/{norm}")
    if status == 200 and body and not body.strip().startswith("404"):
        return status, body

    api_url = f"https://api.github.com/repos/{KIT_REPO}/contents/{norm}?ref=main"
    req = urllib.request.Request(
        api_url,
        headers={"User-Agent": "workspace-kit-sync/1.9", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, err_body
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        return 0, str(e)

    if payload.get("encoding") == "base64" and payload.get("content"):
        raw = payload["content"].replace("\n", "")
        return 200, base64.b64decode(raw).decode("utf-8", errors="replace")
    if download := payload.get("download_url"):
        return fetch_url(download)
    return 404, "no content in API response"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_text(path.read_text(encoding="utf-8"))


def git_remote_slug() -> str | None:
    if not (ROOT / ".git").is_dir():
        return None
    result = run_cmd(["git", "-C", str(ROOT), "remote", "get-url", "origin"])
    if result.returncode != 0:
        return None
    url = result.stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+/[^/.]+)", url)
    return m.group(1) if m else url.split("/")[-1].replace(".git", "")


def pilot_fingerprint() -> str:
    state = load_sync_state()
    if fp := state.get("pilot_fingerprint"):
        return str(fp)

    salt = os.environ.get("KIT_PILOT_SALT", "")
    if not salt:
        env_file = ROOT / ".env"
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("KIT_PILOT_SALT="):
                    salt = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not salt:
        slug = git_remote_slug() or ROOT.name
        salt = f"kit-pilot:{slug}"

    digest = hashlib.sha256(salt.encode("utf-8")).hexdigest()[:8]
    state["pilot_fingerprint"] = digest
    save_sync_state(state)
    return digest


def anonymize_text(text: str, *, extra_redact: list[str] | None = None) -> str:
    out = text
    for pattern, repl in _REDACT_PATTERNS:
        out = pattern.sub(repl, out)
    for term in extra_redact or []:
        if term and len(term) > 2:
            out = re.sub(re.escape(term), "[project]", out, flags=re.IGNORECASE)
    return out


def load_project_redact_terms() -> list[str]:
    project_md = WORKSPACE / "PROJECT.md"
    if not project_md.is_file():
        return []
    text = project_md.read_text(encoding="utf-8", errors="replace")
    terms: set[str] = set()
    for m in re.finditer(r"https?://([^\s/\)]+)", text):
        host = m.group(1).lower()
        if "github.com" not in host:
            terms.add(host)
    slug = git_remote_slug()
    if slug:
        terms.add(slug.split("/")[-1])
    return sorted(terms)


def parse_remote_kit_version(text: str) -> str | None:
    for pattern in (KIT_VERSION_RE, KIT_VERSION_ALT):
        if m := pattern.search(text):
            return m.group(1).strip()
    return None


def read_index_kit_version() -> str | None:
    if not INDEX_PATH.is_file():
        return None
    text = INDEX_PATH.read_text(encoding="utf-8")
    m = re.search(r"^##\s+starter_kit_version\s*\n([^\n]+)", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def read_workspace_stage() -> int:
    if not INDEX_PATH.is_file():
        return 0
    text = INDEX_PATH.read_text(encoding="utf-8")
    m = re.search(r"^##\s+workspace_stage\s*\n(\d+)", text, re.MULTILINE)
    return int(m.group(1)) if m else 0


def update_index_kit_version(version: str, source: str = "remote") -> None:
    if not INDEX_PATH.is_file():
        return
    text = INDEX_PATH.read_text(encoding="utf-8")
    text = re.sub(
        r"(^##\s+starter_kit_version\s*\n)([^\n]+)",
        rf"\g<1>{version}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"(^##\s+starter_kit_source\s*\n)([^\n]+)",
        rf"\g<1>{source}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    INDEX_PATH.write_text(text, encoding="utf-8")


def load_sync_state() -> dict[str, Any]:
    if SYNC_STATE_PATH.is_file():
        try:
            return json.loads(SYNC_STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"pilot_fingerprint": None, "inbound": {}, "outbound": {}}


def save_sync_state(state: dict[str, Any]) -> None:
    SYNC_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now().isoformat()
    SYNC_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_push_state() -> dict[str, Any]:
    if PUSH_STATE_PATH.is_file():
        try:
            legacy = json.loads(PUSH_STATE_PATH.read_text(encoding="utf-8"))
            sync = load_sync_state()
            if not sync.get("outbound", {}).get("submitted") and legacy.get("submitted"):
                sync.setdefault("outbound", {})["submitted"] = legacy["submitted"]
                sync["outbound"]["last_run"] = legacy.get("last_run")
                save_sync_state(sync)
            return legacy
        except json.JSONDecodeError:
            pass
    sync = load_sync_state()
    outbound = sync.get("outbound", {})
    return {"submitted": outbound.get("submitted", {}), "last_run": outbound.get("last_run")}


def save_push_state(state: dict[str, Any]) -> None:
    PUSH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state["last_run"] = datetime.now().isoformat()
    PUSH_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sync = load_sync_state()
    sync.setdefault("outbound", {})
    sync["outbound"]["submitted"] = state.get("submitted", {})
    sync["outbound"]["last_run"] = state.get("last_run")
    save_sync_state(sync)


def is_protected_dest(dest: str) -> bool:
    norm = dest.replace("\\", "/").lstrip("./")
    for prefix in PROTECTED_PULL_PREFIXES:
        if norm == prefix.rstrip("/") or norm.startswith(prefix):
            return True
    return False


def backup_file(dest_path: Path, kit_version: str) -> Path | None:
    if not dest_path.is_file():
        return None
    backup = BACKUP_DIR / kit_version / dest_path.relative_to(ROOT)
    backup.parent.mkdir(parents=True, exist_ok=True)
    backup.write_text(dest_path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup
