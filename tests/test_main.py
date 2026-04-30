"""Tests for the main entry point (main.py)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from main import handle


class TestHandleHappyPath:
    """handle() function — happy path."""

    def test_returns_completion_on_main_agent_route(
        self, mock_client,
    ) -> None:
        sink = MagicMock()
        result = handle(
            query="What is the capital?",
            client=mock_client,
            sink=sink,
        )
        assert result == "The capital of France is Paris."

    def test_writes_trace_on_success(self, mock_client) -> None:
        sink = MagicMock()
        handle(query="test", client=mock_client, sink=sink)
        sink.write.assert_called_once()

    def test_trace_has_correct_decision_path(self, mock_client) -> None:
        sink = MagicMock()
        handle(query="test", client=mock_client, sink=sink)
        trace = sink.write.call_args[0][0]
        assert "router.route" in trace.decision_path
        assert "main_agent.run" in trace.decision_path
        assert "done" in trace.decision_path

    def test_trace_has_final_output_set(self, mock_client) -> None:
        sink = MagicMock()
        handle(query="test", client=mock_client, sink=sink)
        trace = sink.write.call_args[0][0]
        assert trace.final_output == "The capital of France is Paris."

    def test_trace_generation_is_populated(self, mock_client) -> None:
        sink = MagicMock()
        handle(query="test", client=mock_client, sink=sink)
        trace = sink.write.call_args[0][0]
        assert trace.generation is not None
        assert trace.generation.completion == "The capital of France is Paris."


class TestHandleErrorPath:
    """handle() function — error path."""

    def test_writes_trace_on_failure(self, mock_client) -> None:
        sink = MagicMock()
        mock_client.generate.side_effect = RuntimeError("model unavailable")

        with pytest.raises(RuntimeError):
            handle(query="test", client=mock_client, sink=sink)

        sink.write.assert_called_once()

    def test_trace_error_populated_on_failure(self, mock_client) -> None:
        sink = MagicMock()
        mock_client.generate.side_effect = RuntimeError("model unavailable")

        with pytest.raises(RuntimeError):
            handle(query="test", client=mock_client, sink=sink)

        trace = sink.write.call_args[0][0]
        assert trace.error is not None
        assert "RuntimeError" in trace.error
        assert "model unavailable" in trace.error

    def test_trace_decision_path_ends_with_error(self, mock_client) -> None:
        sink = MagicMock()
        mock_client.generate.side_effect = RuntimeError("fail")

        with pytest.raises(RuntimeError):
            handle(query="test", client=mock_client, sink=sink)

        trace = sink.write.call_args[0][0]
        assert trace.decision_path[-1] == "error"

    def test_trace_generation_null_on_failure(self, mock_client) -> None:
        sink = MagicMock()
        mock_client.generate.side_effect = RuntimeError("fail")

        with pytest.raises(RuntimeError):
            handle(query="test", client=mock_client, sink=sink)

        trace = sink.write.call_args[0][0]
        assert trace.generation is None

    def test_trace_final_output_null_on_failure(self, mock_client) -> None:
        sink = MagicMock()
        mock_client.generate.side_effect = RuntimeError("fail")

        with pytest.raises(RuntimeError):
            handle(query="test", client=mock_client, sink=sink)

        trace = sink.write.call_args[0][0]
        assert trace.final_output is None

    def test_unknown_route_raises_value_error(self, mock_client) -> None:
        sink = MagicMock()
        with patch(
            "main.router_route",
            return_value=MagicMock(route="unknown", reason="?"),
        ):
            with pytest.raises(ValueError, match="Unknown route"):
                handle(query="test", client=mock_client, sink=sink)

    def test_unknown_route_still_writes_trace(self, mock_client) -> None:
        sink = MagicMock()
        with patch(
            "main.router_route",
            return_value=MagicMock(route="unknown", reason="?"),
        ):
            with pytest.raises(ValueError):
                handle(query="test", client=mock_client, sink=sink)

        sink.write.assert_called_once()
