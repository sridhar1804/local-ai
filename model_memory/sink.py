"""Trace sink interface and implementations."""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol


class TraceSink(Protocol):
    def write(self, trace) -> None: ...


class JsonlTraceSink:
    def __init__(self, log_dir: str = "logs/traces") -> None:
        self._log_dir = Path(log_dir)
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _file_path(self) -> Path:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self._log_dir / f"{date_str}.jsonl"

    def write(self, trace) -> None:
        line = trace.to_jsonl() + "\n"
        with self._lock:
            with open(self._file_path(), "a") as f:
                f.write(line)


class NullSink:
    def write(self, trace) -> None:
        pass
