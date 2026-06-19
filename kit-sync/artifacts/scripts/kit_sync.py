#!/usr/bin/env python3
"""
Двусторонний sync с workspace_kit (сервер).

  pull  — обновления workspace/Cursor-логики с сервера (manifest + artifacts)
  push  — анонимизированные learnings в issues kit
  sync  — pull, затем push (по команде)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from kit_common import (
    ROOT,
    WORKSPACE,
    anonymize_text,
    backup_file,
    fetch_kit_path,
    fetch_url,
    gh_auth_status,
    is_protected_dest,
    load_sync_state,
    parse_remote_kit_version,
    pilot_fingerprint,
    read_index_kit_version,
    read_workspace_stage,
    save_sync_state,
    sha256_text,
    update_index_kit_version,
)
from log_utils import dev_log

REPORT_DIR = WORKSPACE / "reports"

MANIFEST_PATHS = ("kit-sync/manifest.json", "pilot-sync/manifest.json")
DOC_PATHS = ("workspace_kit.md", "starter_kit.md")


def _fetch_manifest() -> tuple[dict[str, Any] | None, str]:
    for path in MANIFEST_PATHS:
        status, body = fetch_kit_path(path)
        if status != 200:
            continue
        try:
            return json.loads(body), ""
        except json.JSONDecodeError as e:
            return None, f"manifest JSON ({path}): {e}"
    return None, "manifest недоступен (kit-sync и pilot-sync)"


def _fetch_kit_doc() -> tuple[int, str]:
    for path in DOC_PATHS:
        status, body = fetch_kit_path(path)
        if status == 200 and body:
            return status, body
    return 404, ""


def _fetch_artifact(src: str) -> tuple[str | None, str]:
    path = src.lstrip("/")
    if path.startswith("http"):
        status, body = fetch_url(path)
        return (body, "") if status == 200 else (None, f"HTTP {status}")

    for candidate in (path, f"kit-sync/{path}", f"pilot-sync/{path}"):
        if candidate.startswith("kit-sync/kit-sync/") or candidate.startswith("pilot-sync/pilot-sync/"):
            continue
        status, body = fetch_kit_path(candidate)
        if status == 200:
            return body, ""
    return None, f"HTTP 404 for {path}"


def _version_tuple(v: str) -> tuple[int, ...]:
    parts: list[int] = []
    for p in v.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def pull_updates(*, dry_run: bool, force: bool) -> int:
    local_ver = read_index_kit_version() or "0"
    stage = read_workspace_stage()
    fp = pilot_fingerprint()

    status, doc_body = _fetch_kit_doc()
    remote_doc_ver = parse_remote_kit_version(doc_body) if status == 200 else None

    manifest, err = _fetch_manifest()
    lines: list[str] = [
        f"# Kit pull — {datetime.now():%Y-%m-%d %H:%M}",
        "",
        f"- **pilot_fingerprint:** `{fp}`",
        f"- **workspace_stage:** {stage}",
        f"- **local kit version:** {local_ver}",
        f"- **remote workspace_kit.md:** {remote_doc_ver or 'недоступен'}",
        "",
    ]

    if manifest is None:
        lines.extend([
            "## Манифест",
            "",
            f"Не загружен: {err}",
            "",
            "Пока доступна только сверка версии `workspace_kit.md`.",
            "Полный pull заработает после публикации `kit-sync/manifest.json` на сервере kit.",
            "",
        ])
        if remote_doc_ver and _version_tuple(remote_doc_ver) > _version_tuple(local_ver):
            lines.append(f"**Доступна новая версия kit:** {remote_doc_ver} (у вас {local_ver}).")
            snapshot = REPORT_DIR / "kit-remote-workspace_kit.md"
            if not dry_run and status == 200:
                snapshot.write_text(doc_body, encoding="utf-8")
                lines.append(f"Снимок сохранён: `{snapshot.relative_to(ROOT)}`")
        _write_report(lines, applied=0, dry_run=dry_run)
        print("\n".join(lines))
        return 0

    kit_ver = str(manifest.get("kit_version", remote_doc_ver or local_ver))
    lines.extend([
        "## Манифест",
        "",
        f"- **kit_version:** {kit_ver}",
        f"- **released_at:** {manifest.get('released_at', '—')}",
        f"- **changelog:** {manifest.get('changelog', '—')}",
        "",
        "## Артефакты",
        "",
    ])

    state = load_sync_state()
    inbound = state.setdefault("inbound", {})
    applied_map: dict[str, str] = inbound.setdefault("applied", {})
    if inbound.get("last_applied_version") == kit_ver and not force and not dry_run:
        if _version_tuple(kit_ver) <= _version_tuple(local_ver):
            print(f"Уже на версии {kit_ver}. Используйте --force для повторного pull.")
            return 0

    applied_count = 0
    artifacts = manifest.get("artifacts") or []

    for art in artifacts:
        art_id = art.get("id", "?")
        dest = art.get("dest", "").replace("\\", "/").lstrip("./")
        src = art.get("src", "")
        expected_sha = (art.get("sha256") or "").lower()
        stage_min = int(art.get("stage_min", 0))
        mode = art.get("mode", "kit_managed")

        if not dest or not src:
            lines.append(f"- skip `{art_id}`: нет dest/src")
            continue
        if is_protected_dest(dest):
            lines.append(f"- skip `{art_id}` → `{dest}`: protected")
            continue
        if stage < stage_min:
            lines.append(f"- skip `{art_id}` → `{dest}`: нужна стадия ≥{stage_min}")
            continue

        content, fetch_err = _fetch_artifact(src)
        if content is None:
            lines.append(f"- FAIL `{art_id}`: {fetch_err}")
            continue

        actual_sha = sha256_text(content)
        if expected_sha and actual_sha != expected_sha:
            lines.append(f"- FAIL `{art_id}`: sha256 mismatch")
            continue

        dest_path = ROOT / dest
        if dest_path.is_file() and mode == "skip_if_exists":
            lines.append(f"- skip `{art_id}` → `{dest}`: уже есть (skip_if_exists)")
            applied_map[art_id] = actual_sha
            continue

        if applied_map.get(art_id) == actual_sha and not force:
            lines.append(f"- skip `{art_id}` → `{dest}`: без изменений")
            continue

        if dry_run:
            lines.append(f"- [dry-run] apply `{art_id}` → `{dest}` ({len(content)} bytes)")
            applied_count += 1
            continue

        backup_file(dest_path, kit_ver)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(content, encoding="utf-8")
        applied_map[art_id] = actual_sha
        lines.append(f"- OK `{art_id}` → `{dest}`")
        applied_count += 1
        dev_log("kit_sync", "artifact_applied", {"id": art_id, "dest": dest, "version": kit_ver})

    if not dry_run and applied_count:
        update_index_kit_version(kit_ver, "remote")
        inbound["last_applied_version"] = kit_ver
        inbound["last_pull_at"] = datetime.now().isoformat()
        save_sync_state(state)

    lines.append("")
    lines.append(f"**Применено:** {applied_count}")
    _write_report(lines, applied=applied_count, dry_run=dry_run)
    print("\n".join(lines))
    return 0


def _write_report(lines: list[str], *, applied: int, dry_run: bool) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "dry-run" if dry_run else "applied"
    path = REPORT_DIR / f"kit-pull-{datetime.now():%Y-%m-%d}-{suffix}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nОтчёт: {path.relative_to(ROOT)}")


def push_learnings(argv: list[str]) -> int:
    from kit_learning_issue import main as issue_main

    return issue_main(argv)


def status_report() -> int:
    local_ver = read_index_kit_version() or "—"
    fp = pilot_fingerprint()
    stage = read_workspace_stage()
    state = load_sync_state()
    inbound = state.get("inbound", {})
    outbound = state.get("outbound", {})

    manifest_ver = "—"
    for path in MANIFEST_PATHS:
        status, body = fetch_kit_path(path)
        if status == 200:
            try:
                manifest_ver = json.loads(body).get("kit_version", "—")
                break
            except json.JSONDecodeError:
                manifest_ver = "invalid json"

    _, doc_body = _fetch_kit_doc()
    doc_ver = parse_remote_kit_version(doc_body) or "—"

    print("=== Kit sync status ===")
    print(f"pilot_fingerprint: {fp}")
    print(f"workspace_stage:   {stage}")
    print(f"local version:     {local_ver}")
    print(f"remote manifest:   {manifest_ver}")
    print(f"remote doc:        {doc_ver}")
    print(f"last pull:         {inbound.get('last_applied_version', '—')} @ {inbound.get('last_pull_at', '—')}")
    print(f"last push:         {outbound.get('last_run', '—')}")
    submitted = outbound.get("submitted") or {}
    print(f"issues submitted:  {len(submitted)}")
    if inbound.get("applied"):
        print(f"artifacts cached:  {len(inbound['applied'])}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Двусторонний sync с workspace_kit (pull / push learnings)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_pull = sub.add_parser("pull", help="Получить обновления workspace с сервера kit")
    p_pull.add_argument("--dry-run", action="store_true")
    p_pull.add_argument("--force", action="store_true")

    p_push = sub.add_parser("push", help="Отправить анонимизированные learnings (issues)")
    p_push.add_argument("--check-auth", action="store_true")
    p_push.add_argument("--dry-run", action="store_true")
    p_push.add_argument("--skl", action="append", metavar="SKL-NNN")
    p_push.add_argument("--ready", action="store_true")
    p_push.add_argument("--force", action="store_true")
    p_push.add_argument("--list", action="store_true")

    p_sync = sub.add_parser("sync", help="pull затем push")
    p_sync.add_argument("--dry-run", action="store_true")
    p_sync.add_argument("--push-ready", action="store_true")
    p_sync.add_argument("--force", action="store_true")

    sub.add_parser("status", help="Сверка версий и состояния sync")

    args, rest = parser.parse_known_args(argv)

    if args.command == "status":
        return status_report()

    if args.command == "pull":
        return pull_updates(dry_run=args.dry_run, force=args.force)

    if args.command == "push":
        push_argv: list[str] = []
        if args.check_auth:
            push_argv.append("--check-auth")
        if args.dry_run:
            push_argv.append("--dry-run")
        if args.skl:
            for s in args.skl:
                push_argv.extend(["--skl", s])
        if args.ready:
            push_argv.append("--ready")
        if args.force:
            push_argv.append("--force")
        if args.list:
            push_argv.append("--list")
        if not push_argv:
            parser.error("push: укажите --list, --ready, --skl или --check-auth")
        return push_learnings(push_argv + rest)

    if args.command == "sync":
        rc = pull_updates(dry_run=args.dry_run, force=args.force)
        if rc != 0:
            return rc
        if args.push_ready:
            push_argv = ["--ready"]
            if args.dry_run:
                push_argv.append("--dry-run")
            if args.force:
                push_argv.append("--force")
            ok_auth, msg = gh_auth_status()
            if not ok_auth and not args.dry_run:
                print(msg, file=sys.stderr)
                return 1
            return push_learnings(push_argv)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
