"""Trace schema v1.0.0 — one Trace per request, one JSONL line per trace."""

from __future__ import annotations

import json
import traceback
import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

SCHEMA_VERSION = "1.0.0"


class GenerationRecord(BaseModel):
    model: str
    prompt: str
    completion: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    sampling: dict = Field(default_factory=dict)


class ValidationRecord(BaseModel):
    ran: bool = False
    verdict: Optional[str] = None
    confidence: Optional[float] = None
    failure_type: Optional[str] = None


class FallbackRecord(BaseModel):
    triggered: bool = False
    reason: Optional[str] = None
    frontier_model: Optional[str] = None
    frontier_completion: Optional[str] = None


class Trace(BaseModel):
    schema_version: str = SCHEMA_VERSION
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_trace_id: Optional[str] = None
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    input_query: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

    route: Optional[str] = None
    decision_path: list[str] = Field(default_factory=list)

    generation: Optional[GenerationRecord] = None

    retrieval: Optional[dict] = None
    tool_calls: list[dict] = Field(default_factory=list)
    validation: ValidationRecord = Field(default_factory=ValidationRecord)
    fallback: FallbackRecord = Field(default_factory=FallbackRecord)

    final_output: Optional[str] = None

    env: str = "wsl-dev"
    git_sha: Optional[str] = None
    error: Optional[str] = None
    redaction_applied: bool = False

    def to_jsonl(self) -> str:
        return self.model_dump_json()

    def capture_exception(self, exc: Exception) -> None:
        self.error = f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
