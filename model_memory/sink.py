"""Trace sink interface and implementations.

Defines the TraceSink Protocol and two concrete sinks:
JsonlTraceSink (daily-rotated JSONL, threadsafe) and NullSink (no-op).
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol, runtime_checkable

from config import LOG_DIR


@runtime_checkable
class TraceSink(Protocol):
    """Structural interface for trace persistence.

    Any object with a write(trace) -> None method satisfies this protocol.
    No inheritance required.
    """

    def write(self, trace) -> None: ...


class JsonlTraceSink:
    """Writes traces as JSONL lines to daily-rotated files.

    One JSON line per trace, appended to logs/traces/<UTC-date>.jsonl.
    Threadsafe via a single reentrant lock. Daily rotation is by UTC date.
    """

    def __init__(self, log_dir: str = LOG_DIR) -> None:
        """Initialize the sink and ensure the log directory exists.

        Args:
            log_dir: Path to the trace output directory (default from config).
        """
        self._log_dir = Path(log_dir)
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _file_path(self) -> Path:
        """Compute the JSONL file path for today's UTC date."""
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self._log_dir / f"{date_str}.jsonl"

    def write(self, trace) -> None:
        """Append one trace as a JSONL line to today's file.

        Args:
            trace: A trace object with a to_jsonl() method.
        """
        line = trace.to_jsonl() + "\n"
        with self._lock:
            with open(self._file_path(), "a") as file_handle:
                file_handle.write(line)


class NullSink:
    """No-op sink for testing — write() is a silent pass."""

    def write(self, trace) -> None:
        """Discard the trace."""
        pass
