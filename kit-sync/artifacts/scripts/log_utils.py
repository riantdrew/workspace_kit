#!/usr/bin/env python3
"""Минимальное dev-логирование для kit-sync артефактов в пилотах."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs" / "dev"


def dev_log(script_name: str, event: str, data: dict | None = None) -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"{script_name}_{datetime.now():%Y-%m-%d}.log"
    entry = {
        "ts": datetime.now().isoformat(),
        "script": script_name,
        "event": event,
        "data": data or {},
    }
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
