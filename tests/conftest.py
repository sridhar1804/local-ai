"""Shared fixtures for the test suite."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock

import pytest

from model_memory.trace import Trace


@pytest.fixture
def sample_trace() -> Trace:
    """Return a minimal Trace with a test query."""
    return Trace(input_query="What is the capital of France?")


@pytest.fixture
def temp_log_dir() -> str:
    """Create a temporary directory for log output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_client():
    """Return a MagicMock that mimics Phi3Client."""

    class MockGenerationResult:
        completion = "The capital of France is Paris."
        prompt_tokens = 10
        completion_tokens = 7
        latency_ms = 100.0
        model = "test-model"
        sampling = {"temperature": 0.2, "top_p": 0.95, "max_tokens": 512}

    client = MagicMock()
    client.generate.return_value = MockGenerationResult()
    return client
