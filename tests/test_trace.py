"""Tests for the Trace schema (model_memory/trace.py)."""

from __future__ import annotations

import json

import pytest

from model_memory.trace import (
    SCHEMA_VERSION,
    FallbackRecord,
    GenerationRecord,
    Trace,
    ValidationRecord,
)


class TestSchemaVersion:
    """Schema version constant is set correctly."""

    def test_version_is_1_0_0(self) -> None:
        assert SCHEMA_VERSION == "1.0.0"


class TestTraceDefaults:
    """Trace defaults and reserved fields are present at construction."""

    def test_default_schema_version(self) -> None:
        trace = Trace(input_query="test")
        assert trace.schema_version == "1.0.0"

    def test_trace_id_is_generated(self) -> None:
        trace = Trace(input_query="test")
        assert len(trace.trace_id) == 36
        assert Trace(input_query="a").trace_id != Trace(input_query="b").trace_id

    def test_timestamp_utc_is_generated(self) -> None:
        trace = Trace(input_query="test")
        assert trace.timestamp_utc is not None
        assert "T" in trace.timestamp_utc

    def test_reserved_fields_at_defaults(self) -> None:
        trace = Trace(input_query="test")
        assert trace.retrieval is None
        assert trace.tool_calls == []
        assert trace.validation.ran is False
        assert trace.validation.verdict is None
        assert trace.fallback.triggered is False
        assert trace.fallback.reason is None

    def test_parent_trace_id_null_by_default(self) -> None:
        trace = Trace(input_query="test")
        assert trace.parent_trace_id is None

    def test_env_is_wsl_dev(self) -> None:
        trace = Trace(input_query="test")
        assert trace.env == "wsl-dev"

    def test_redaction_applied_false(self) -> None:
        trace = Trace(input_query="test")
        assert trace.redaction_applied is False


class TestToJsonl:
    """Trace serialization to JSONL."""

    def test_to_jsonl_returns_valid_json(self) -> None:
        trace = Trace(input_query="test")
        line = trace.to_jsonl()
        parsed = json.loads(line)
        assert isinstance(parsed, dict)

    def test_to_jsonl_is_single_line(self) -> None:
        trace = Trace(input_query="test")
        line = trace.to_jsonl()
        assert "\n" not in line.rstrip("\n")

    def test_to_jsonl_contains_all_top_level_keys(self) -> None:
        trace = Trace(input_query="test")
        parsed = json.loads(trace.to_jsonl())
        expected_keys = {
            "schema_version", "trace_id", "parent_trace_id", "timestamp_utc",
            "input_query", "session_id", "user_id", "route", "decision_path",
            "generation", "retrieval", "tool_calls", "validation", "fallback",
            "final_output", "env", "git_sha", "error", "redaction_applied",
        }
        assert set(parsed.keys()) == expected_keys


class TestCaptureException:
    """Exception capture into trace error field."""

    def test_error_field_set_on_exception(self) -> None:
        trace = Trace(input_query="test")
        try:
            raise ValueError("something went wrong")
        except ValueError as exc:
            trace.capture_exception(exc)
        assert trace.error is not None
        assert "ValueError" in trace.error
        assert "something went wrong" in trace.error

    def test_error_field_null_by_default(self) -> None:
        trace = Trace(input_query="test")
        assert trace.error is None


class TestGenerationRecord:
    """GenerationRecord model."""

    def test_construct_with_required_fields(self) -> None:
        record = GenerationRecord(
            model="test",
            prompt="hello",
            completion="world",
            prompt_tokens=5,
            completion_tokens=3,
            latency_ms=42.0,
        )
        assert record.model == "test"
        assert record.completion == "world"

    def test_sampling_defaults_to_empty_dict(self) -> None:
        record = GenerationRecord(
            model="x",
            prompt="p",
            completion="c",
            prompt_tokens=1,
            completion_tokens=1,
            latency_ms=1.0,
        )
        assert record.sampling == {}


class TestValidationRecord:
    """ValidationRecord model."""

    def test_ran_false_by_default(self) -> None:
        record = ValidationRecord()
        assert record.ran is False

    def test_verdict_none_by_default(self) -> None:
        record = ValidationRecord()
        assert record.verdict is None


class TestFallbackRecord:
    """FallbackRecord model."""

    def test_triggered_false_by_default(self) -> None:
        record = FallbackRecord()
        assert record.triggered is False
