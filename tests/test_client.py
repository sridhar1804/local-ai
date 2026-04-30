"""Tests for Phi3Client (models/client.py)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from models.client import GenerationResult, Phi3Client


class TestGenerationResult:
    """GenerationResult dataclass."""

    def test_fields_are_populated(self) -> None:
        result = GenerationResult(
            completion="Paris",
            prompt_tokens=5,
            completion_tokens=1,
            latency_ms=100.0,
            model="test-model",
            sampling={"temperature": 0.0},
        )
        assert result.completion == "Paris"
        assert result.prompt_tokens == 5
        assert result.completion_tokens == 1
        assert result.latency_ms == 100.0
        assert result.model == "test-model"
        assert result.sampling == {"temperature": 0.0}


class TestPhi3Client:
    """Phi3Client HTTP wrapper."""

    def test_constructs_with_defaults(self) -> None:
        client = Phi3Client()
        assert client._base_url == "http://localhost:8000/v1"
        assert "phi-3-mini" in client._model.lower()
        client.close()

    def test_constructs_with_custom_url(self) -> None:
        client = Phi3Client(base_url="http://custom:9999/v1")
        assert client._base_url == "http://custom:9999/v1"
        client.close()

    def test_close_releases_client(self) -> None:
        client = Phi3Client()
        client.close()

    def test_generate_sends_correct_payload(self) -> None:
        client = Phi3Client()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "hello"}}],
            "usage": {"prompt_tokens": 5, "completion_tokens": 1},
            "model": "test",
        }
        mock_response.raise_for_status = MagicMock()

        with patch.object(
            client._client, "post", return_value=mock_response,
        ) as mock_post:
            result = client.generate(user_message="hi")

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0].endswith("/chat/completions")
        payload = call_args[1]["json"]
        assert payload["messages"] == [{"role": "user", "content": "hi"}]
        assert result.completion == "hello"
        client.close()

    def test_generate_includes_system_message(self) -> None:
        client = Phi3Client()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "done"}}],
            "usage": {},
            "model": "test",
        }
        mock_response.raise_for_status = MagicMock()

        with patch.object(client._client, "post", return_value=mock_response) as mock_post:
            client.generate(
                user_message="hi",
                system_message="You are helpful.",
            )

        payload = mock_post.call_args[1]["json"]
        assert payload["messages"][0] == {"role": "system", "content": "You are helpful."}
        assert payload["messages"][1] == {"role": "user", "content": "hi"}
        client.close()

    def test_generate_sets_sampling_params(self) -> None:
        client = Phi3Client()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "x"}}],
            "usage": {},
            "model": "test",
        }
        mock_response.raise_for_status = MagicMock()

        with patch.object(client._client, "post", return_value=mock_response) as mock_post:
            client.generate(
                user_message="hi",
                max_tokens=100,
                temperature=0.5,
                top_p=0.8,
            )

        payload = mock_post.call_args[1]["json"]
        assert payload["max_tokens"] == 100
        assert payload["temperature"] == 0.5
        assert payload["top_p"] == 0.8
        client.close()

    def test_generate_raises_on_http_error(self) -> None:
        client = Phi3Client()
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )

        with patch.object(client._client, "post", return_value=mock_response):
            with pytest.raises(httpx.HTTPStatusError):
                client.generate(user_message="hi")
        client.close()
