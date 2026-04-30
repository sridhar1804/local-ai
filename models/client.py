"""Thin HTTP wrapper around the vLLM OpenAI-compatible API.

Provides a Phi3Client that sends chat requests and returns GenerationResult
dataclass instances. No retry logic, no caching, no prompt assembly.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

import httpx

from config import BASE_URL, MODEL, TIMEOUT


@dataclass
class GenerationResult:
    """Raw output from a single model generation call.

    Attributes:
        completion: The text produced by the model.
        prompt_tokens: Number of tokens in the input.
        completion_tokens: Number of tokens in the generated output.
        latency_ms: Wall-clock milliseconds for the HTTP round-trip.
        model: Model identifier used for the request.
        sampling: Dict of the sampling parameters applied.
    """

    completion: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    model: str
    sampling: dict = field(default_factory=dict)


class Phi3Client:
    """HTTP client for the vLLM OpenAI-compatible chat completions endpoint.

    Wraps a single httpx.Client. Callers must invoke close() to release
    the underlying connection pool.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        model: str = MODEL,
        timeout: float = TIMEOUT,
    ) -> None:
        """Initialize the client with connection parameters.

        Args:
            base_url: Root URL of the vLLM server (default from config).
            model: HuggingFace model identifier (default from config).
            timeout: HTTP request timeout in seconds (default from config).
        """
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._client = httpx.Client(timeout=timeout)

    def generate(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        max_tokens: int = 512,
        temperature: float = 0.2,
        top_p: float = 0.95,
    ) -> GenerationResult:
        """Send a chat completion request and return the result.

        Args:
            user_message: The user's query text.
            system_message: Optional system prompt.
            max_tokens: Maximum completion tokens to generate.
            temperature: Sampling temperature (0.0–2.0).
            top_p: Nucleus sampling probability threshold.

        Returns:
            GenerationResult with completion text, token counts, and latency.

        Raises:
            httpx.HTTPStatusError: On non-2xx responses.
        """
        messages: list[dict] = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self._model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
        }

        start = time.perf_counter()
        response = self._client.post(
            f"{self._base_url}/chat/completions",
            json=payload,
        )
        response.raise_for_status()
        elapsed_ms = (time.perf_counter() - start) * 1000

        data = response.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})

        return GenerationResult(
            completion=choice["message"]["content"],
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            latency_ms=elapsed_ms,
            model=data.get("model", self._model),
            sampling={
                "temperature": temperature,
                "top_p": top_p,
                "max_tokens": max_tokens,
            },
        )

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._client.close()
