"""Integration tests for the full pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from main import handle, main


class TestEndToEnd:
    """End-to-end tests using mocks."""

    def test_full_happy_path_integration(self, tmp_path) -> None:
        log_dir = str(tmp_path)

        from model_memory.sink import JsonlTraceSink
        from agents.router import RouteDecision

        mock_client = MagicMock()

        class MockGen:
            completion = "Paris"
            prompt_tokens = 5
            completion_tokens = 1
            latency_ms = 42.0
            model = "test"
            sampling = {"temperature": 0.2, "top_p": 0.95, "max_tokens": 512}

        mock_client.generate.return_value = MockGen()
        sink = JsonlTraceSink(log_dir=log_dir)

        output = handle(
            query="What is the capital of France?",
            client=mock_client,
            sink=sink,
        )

        assert output == "Paris"

        files = list(Path(log_dir).glob("*.jsonl"))
        assert len(files) == 1

        lines = files[0].read_text().strip().split("\n")
        assert len(lines) == 1

        data = json.loads(lines[0])
        assert data["schema_version"] == "1.0.0"
        assert data["input_query"] == "What is the capital of France?"
        assert data["final_output"] == "Paris"
        assert data["generation"] is not None
        assert data["generation"]["completion"] == "Paris"
        assert data["error"] is None
        assert "done" in data["decision_path"]

    def test_full_error_path_integration(self, tmp_path) -> None:
        log_dir = str(tmp_path)
        from model_memory.sink import JsonlTraceSink

        mock_client = MagicMock()
        mock_client.generate.side_effect = RuntimeError("server down")
        sink = JsonlTraceSink(log_dir=log_dir)

        with patch("builtins.print"):
            import pytest
            with pytest.raises(RuntimeError):
                handle(
                    query="test query",
                    client=mock_client,
                    sink=sink,
                )

        files = list(Path(log_dir).glob("*.jsonl"))
        assert len(files) == 1

        lines = files[0].read_text().strip().split("\n")
        data = json.loads(lines[0])
        assert data["error"] is not None
        assert "RuntimeError" in data["error"]
        assert data["decision_path"][-1] == "error"
        assert data["generation"] is None
        assert data["final_output"] is None
