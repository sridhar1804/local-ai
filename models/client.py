"""Thin HTTP wrapper around the vLLM OpenAI-compatible API."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import httpx


@dataclass
class GenerationResult:
    completion: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    model: str
    sampling: dict = field(default_factory=dict)


class Phi3Client:
    def __init__(
        self,
        base_url: str = "http://localhost:8000/v1",
        model: str = "microsoft/Phi-3-mini-4k-instruct",
        timeout: float = 60.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._client = httpx.Client(timeout=timeout)

    def generate(
        self,
        user_message: str,
        system_message: str | None = None,
        max_tokens: int = 512,
        temperature: float = 0.2,
        top_p: float = 0.95,
    ) -> GenerationResult:
        messages = []
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
            f"{self._base_url}/chat/completions", json=payload
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
        self._client.close()
