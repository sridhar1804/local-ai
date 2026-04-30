"""Tests for the main agent (agents/main_agent.py)."""

from __future__ import annotations

from models.client import GenerationResult
from agents.main_agent import SYSTEM_PROMPT, AgentResult, run


class TestSystemPrompt:
    """System prompt constant."""

    def test_is_non_empty_string(self) -> None:
        assert isinstance(SYSTEM_PROMPT, str)
        assert len(SYSTEM_PROMPT) > 0

    def test_contains_helpful_keyword(self) -> None:
        assert "helpful" in SYSTEM_PROMPT


class TestAgentResult:
    """AgentResult dataclass."""

    def test_fields_are_populated(self) -> None:
        gen = GenerationResult(
            completion="Paris",
            prompt_tokens=5,
            completion_tokens=1,
            latency_ms=100.0,
            model="test",
        )
        result = AgentResult(
            output="Paris",
            assembled_prompt="<system>x</system>\n<user>y</user>",
            generation=gen,
        )
        assert result.output == "Paris"
        assert "<system>" in result.assembled_prompt
        assert result.generation == gen


class TestRun:
    """Agent run function."""

    def test_returns_agent_result(self, mock_client) -> None:
        result = run(query="What is 2+2?", client=mock_client)
        assert isinstance(result, AgentResult)
        assert result.output == "The capital of France is Paris."

    def test_assembled_prompt_has_both_tags(self, mock_client) -> None:
        result = run(query="test query", client=mock_client)
        assert "<system>" in result.assembled_prompt
        assert "<user>" in result.assembled_prompt
        assert "test query" in result.assembled_prompt

    def test_calls_client_generate_with_correct_args(self, mock_client) -> None:
        run(query="my query", client=mock_client)
        mock_client.generate.assert_called_once_with(
            user_message="my query",
            system_message=SYSTEM_PROMPT,
        )
