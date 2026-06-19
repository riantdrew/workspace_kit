#!/usr/bin/env python3
"""
Отправка анонимизированных learnings из пилота в issues workspace_kit.

Требует: GitHub CLI (`gh`) и `gh auth login` для реальной отправки.
Pull обновлений — scripts/kit_sync.py pull (без auth).

Outbound: только универсальные паттерны, без секретов и идентификаторов проекта.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from kit_common import (
    KIT_LABELS,
    KIT_REPO,
    LEARNINGS_PATH,
    ROOT,
    WORKSPACE,
    anonymize_text,
    gh_auth_status,
    load_project_redact_terms,
    load_push_state,
    pilot_fingerprint,
    read_index_kit_version,
    read_workspace_stage,
    save_push_state,
)
from log_utils import dev_log

SESSIONS_JOURNAL = WORKSPACE / "reports" / "sessions" / "journal"
INDEX_PATH = WORKSPACE / "INDEX.md"

BACKLOG_ROW = re.compile(r"^\|\s*(SKL-\d+)\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|\s*$")
JOURNAL_HEAD = re.compile(r"^###\s+(SKL-\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*—\s*(.+?)\s*$")
FIELD_LINE = re.compile(r"^-\s+\*\*([^*]+):\*\*\s*(.+?)\s*$")
META_KIT_VERSION = re.compile(r"kit_version\s*\(проект\)\s*\|\s*([^\|]+)")


@dataclass
class SklEntry:
    skl_id: str
    status: str
    summary: str
    journal: dict[str, str] = field(default_factory=dict)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _parse_meta(text: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    if m := META_KIT_VERSION.search(text):
        meta["kit_version_project"] = m.group(1).strip()
    return meta


def parse_learnings(path: Path = LEARNINGS_PATH) -> dict[str, SklEntry]:
    text = _read_text(path)
    if not text:
        return {}

    entries: dict[str, SklEntry] = {}
    for line in text.splitlines():
        if m := BACKLOG_ROW.match(line):
            skl_id, status, summary = m.group(1), m.group(2), m.group(3)
            entries[skl_id] = SklEntry(skl_id=skl_id, status=status, summary=summary)

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if m := JOURNAL_HEAD.match(lines[i]):
            skl_id, date_s, title = m.group(1), m.group(2), m.group(3)
            block: dict[str, str] = {"date": date_s, "title": title}
            i += 1
            while i < len(lines) and not lines[i].startswith("### SKL-"):
                if fm := FIELD_LINE.match(lines[i]):
                    block[fm.group(1).strip().lower()] = fm.group(2).strip()
                i += 1
            if skl_id in entries:
                entries[skl_id].journal = block
            else:
                entries[skl_id] = SklEntry(
                    skl_id=skl_id, status=block.get("статус", "draft"), summary=title, journal=block
                )
            continue
        i += 1
    return entries


def collect_telemetry(days: int = 7) -> dict[str, Any]:
    """Агрегат телеметрии — только счётчики и обобщённые пути."""
    cutoff = datetime.now() - timedelta(days=days)
    event_counts: dict[str, int] = {}
    paths_touched: set[str] = set()
    journal_files = 0

    if SESSIONS_JOURNAL.is_dir():
        for jpath in SESSIONS_JOURNAL.glob("*.jsonl"):
            journal_files += 1
            for line in jpath.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts_s = row.get("ts", "")
                try:
                    ts = datetime.fromisoformat(ts_s.replace("Z", "+00:00").split("+")[0])
                except ValueError:
                    ts = datetime.now()
                if ts < cutoff:
                    continue
                event = row.get("event", "unknown")
                event_counts[event] = event_counts.get(event, 0) + 1
                payload = row.get("payload") or {}
                for p in payload.get("paths") or []:
                    if not isinstance(p, str):
                        continue
                    if p.startswith("workspace/knowledge/domain/"):
                        paths_touched.add("workspace/knowledge/domain/*")
                    elif p.startswith("workspace/"):
                        parts = p.split("/")
                        paths_touched.add("/".join(parts[:2]) if len(parts) >= 2 else "workspace/*")

    return {
        "period_days": days,
        "journal_files": journal_files,
        "events": event_counts,
        "workspace_path_categories": sorted(paths_touched)[:15],
    }


def _anon(text: str, redact: list[str]) -> str:
    return anonymize_text(text, extra_redact=redact)


def _business_block(entry: SklEntry, redact: list[str]) -> str:
    j = entry.journal
    parts = []
    if s := j.get("суть"):
        parts.append(f"**Проблема/наблюдение:** {_anon(s, redact)}")
    if k := j.get("для kit"):
        parts.append(f"**Ценность для kit:** {_anon(k, redact)}")
    if cat := j.get("категория"):
        parts.append(f"**Категория:** {cat}")
    if not parts:
        parts.append(f"**Сводка backlog:** {_anon(entry.summary, redact)}")
    parts.append(
        "**Зачем майнить:** единый поток обратной связи с пилотов → меньше потерь паттернов "
        "при внедрении workspace в новых репозиториях."
    )
    return "\n\n".join(parts)


def build_issue_body(entry: SklEntry, *, fp: str, meta: dict[str, str], telemetry: dict[str, Any], redact: list[str]) -> str:
    j = entry.journal
    kit_ver = read_index_kit_version() or meta.get("kit_version_project", "—")
    stage = read_workspace_stage()

    telemetry_table = "\n".join(
        f"| {k} | {v} |"
        for k, v in [
            ("Период (дней)", telemetry.get("period_days")),
            ("Файлов журналов", telemetry.get("journal_files")),
            ("События hooks", json.dumps(telemetry.get("events", {}), ensure_ascii=False)),
        ]
    )
    paths = telemetry.get("workspace_path_categories") or []
    paths_block = "\n".join(f"- `{p}`" for p in paths) if paths else "_нет данных за период_"

    title = _anon(j.get("title", entry.summary), redact)
    essence = _anon(j.get("суть", entry.summary), redact)
    for_kit = _anon(j.get("для kit", entry.summary), redact)

    body = f"""## Контекст (анонимизировано)

| Поле | Значение |
|------|----------|
| SKL-ID | `{entry.skl_id}` |
| pilot_fingerprint | `{fp}` |
| Стадия workspace | {stage} |
| Версия kit у клиента | {kit_ver} |
| Дата записи | {j.get("date", "—")} |
| Статус | `{entry.status}` |

> Идентификаторы репозитория, домены, секреты и персональные данные **не передаются**.

## Паттерн

**{title}**

{essence}

## Рекомендация для starter_kit.md

{for_kit}

## Бизнес-обоснование

{_business_block(entry, redact)}

## Телеметрия (агрегат)

| Метрика | Значение |
|---------|----------|
{telemetry_table}

### Категории путей workspace

{paths_block}

---
_Двусторонний канал [workspace kit](https://github.com/riantdrew/workspace_kit)._
_После обработки мейнтейнер публикует обновления в `kit-sync/manifest.json`._
"""
    return body.strip()


def build_issue_title(entry: SklEntry, fp: str, redact: list[str]) -> str:
    title_bit = _anon(entry.journal.get("title") or entry.summary, redact)
    if len(title_bit) > 60:
        title_bit = title_bit[:57] + "..."
    return f"[{entry.skl_id}] [fp:{fp}] {title_bit}"


def create_issue(title: str, body: str, *, dry_run: bool) -> tuple[bool, str]:
    from kit_common import run_cmd

    if dry_run:
        return True, f"[dry-run] {KIT_REPO} — {title}"

    base = ["gh", "issue", "create", "--repo", KIT_REPO, "--title", title, "--body", body]
    for cmd in (
        base + [x for label in KIT_LABELS for x in ("--label", label)],
        base,
    ):
        result = run_cmd(cmd)
        if result.returncode == 0:
            return True, result.stdout.strip()
    err = (result.stderr or result.stdout or "unknown error").strip()
    return False, err


def submit_entries(entries: list[SklEntry], *, dry_run: bool, force: bool) -> int:
    state = load_push_state()
    submitted: dict[str, Any] = state.setdefault("submitted", {})
    meta = _parse_meta(_read_text(LEARNINGS_PATH))
    fp = pilot_fingerprint()
    redact = load_project_redact_terms()
    telemetry = collect_telemetry()

    ok_count = 0
    for entry in entries:
        if entry.status != "ready_for_kit":
            print(f"  skip {entry.skl_id}: статус {entry.status}", file=sys.stderr)
            continue
        if entry.skl_id in submitted and not force:
            print(f"  skip {entry.skl_id}: уже issue #{submitted[entry.skl_id].get('issue_number')}", file=sys.stderr)
            continue

        title = build_issue_title(entry, fp, redact)
        body = build_issue_body(entry, fp=fp, meta=meta, telemetry=telemetry, redact=redact)
        success, msg = create_issue(title, body, dry_run=dry_run)
        if not success:
            print(f"  FAIL {entry.skl_id}: {msg}", file=sys.stderr)
            dev_log("kit_learning_issue", "create_failed", {"skl_id": entry.skl_id, "error": msg})
            continue

        if not dry_run and msg.startswith("http"):
            m = re.search(r"/issues/(\d+)", msg)
            submitted[entry.skl_id] = {
                "issue_url": msg,
                "issue_number": int(m.group(1)) if m else None,
                "submitted_at": datetime.now().isoformat(),
                "pilot_fingerprint": fp,
            }
            save_push_state(state)

        print(f"  OK {entry.skl_id}: {msg}")
        dev_log("kit_learning_issue", "created" if not dry_run else "dry_run", {"skl_id": entry.skl_id, "result": msg})
        ok_count += 1

    return ok_count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Push анонимизированных learnings в workspace_kit")
    parser.add_argument("--check-auth", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skl", action="append", metavar="SKL-NNN")
    parser.add_argument("--ready", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)

    if args.check_auth:
        ok, msg = gh_auth_status()
        print(msg)
        return 0 if ok else 1

    all_entries = parse_learnings()
    if args.list:
        state = load_push_state()
        submitted = state.get("submitted", {})
        print(f"pilot_fingerprint: {pilot_fingerprint()}")
        print(f"Learnings: {LEARNINGS_PATH}")
        for skl_id, e in sorted(all_entries.items()):
            sync = submitted.get(skl_id, {})
            issue = f"#{sync['issue_number']}" if sync.get("issue_number") else "—"
            print(f"  {skl_id}  {e.status:14}  issue {issue}  {e.summary[:50]}")
        return 0

    if not args.skl and not args.ready:
        parser.error("Укажите --skl SKL-NNN, --ready или --list")

    ok_auth, auth_msg = gh_auth_status()
    if not ok_auth and not args.dry_run:
        print(auth_msg, file=sys.stderr)
        print("\nДля предпросмотра: --dry-run", file=sys.stderr)
        return 1
    if ok_auth:
        print(auth_msg)
    print(f"pilot_fingerprint: {pilot_fingerprint()} (анонимный ID пилота)")

    if args.skl:
        selected = []
        for sid in args.skl:
            if sid not in all_entries:
                print(f"Не найден {sid}", file=sys.stderr)
                return 1
            selected.append(all_entries[sid])
    else:
        selected = list(all_entries.values())

    count = submit_entries(selected, dry_run=args.dry_run, force=args.force)
    print(f"\nГотово: {count} issue(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
