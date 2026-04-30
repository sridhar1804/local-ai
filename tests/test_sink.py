"""Tests for trace sinks (model_memory/sink.py)."""

from __future__ import annotations

import json
from pathlib import Path

from model_memory.sink import JsonlTraceSink, NullSink, TraceSink
from model_memory.trace import Trace


class TestNullSink:
    """NullSink silently discards all traces."""

    def test_write_does_not_raise(self) -> None:
        sink = NullSink()
        sink.write(Trace(input_query="test"))

    def test_is_a_trace_sink(self) -> None:
        assert isinstance(NullSink(), TraceSink)


class TestJsonlTraceSink:
    """JsonlTraceSink writes daily-rotated JSONL files."""

    def test_creates_log_directory(self, tmp_path) -> None:
        log_dir = str(tmp_path / "traces")
        JsonlTraceSink(log_dir=log_dir)
        assert Path(log_dir).is_dir()

    def test_writes_one_line_per_trace(self, tmp_path) -> None:
        log_dir = str(tmp_path)
        sink = JsonlTraceSink(log_dir=log_dir)
        trace = Trace(input_query="hello")
        sink.write(trace)

        files = list(Path(log_dir).glob("*.jsonl"))
        assert len(files) == 1

        content = files[0].read_text().strip().split("\n")
        assert len(content) == 1

    def test_writes_valid_jsonl(self, tmp_path) -> None:
        log_dir = str(tmp_path)
        sink = JsonlTraceSink(log_dir=log_dir)
        trace = Trace(input_query="hello")
        sink.write(trace)

        files = list(Path(log_dir).glob("*.jsonl"))
        line = files[0].read_text().strip()
        parsed = json.loads(line)
        assert parsed["input_query"] == "hello"
        assert parsed["schema_version"] == "1.0.0"

    def test_appends_multiple_traces(self, tmp_path) -> None:
        log_dir = str(tmp_path)
        sink = JsonlTraceSink(log_dir=log_dir)
        sink.write(Trace(input_query="first"))
        sink.write(Trace(input_query="second"))

        files = list(Path(log_dir).glob("*.jsonl"))
        lines = files[0].read_text().strip().split("\n")
        assert len(lines) == 2

    def test_file_name_uses_date_format(self, tmp_path) -> None:
        log_dir = str(tmp_path)
        sink = JsonlTraceSink(log_dir=log_dir)
        sink.write(Trace(input_query="test"))

        files = list(Path(log_dir).glob("*.jsonl"))
        filename = files[0].name
        parts = filename.replace(".jsonl", "").split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4

    def test_appends_not_overwrites(self, tmp_path) -> None:
        log_dir = str(tmp_path)
        sink = JsonlTraceSink(log_dir=log_dir)
        sink.write(Trace(input_query="first"))
        sink.write(Trace(input_query="second"))

        files = list(Path(log_dir).glob("*.jsonl"))
        content = files[0].read_text().strip().split("\n")
        assert len(content) == 2
