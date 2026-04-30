"""Trace schema v1.0.0 — one Trace per request, one JSONL line per trace.

Defines the Pydantic models that anchor the observability substrate.
All Phase 2 reserved fields are present at their default empty/false values.
"""

from __future__ import annotations

import traceback
import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

SCHEMA_VERSION = "1.0.0"


class GenerationRecord(BaseModel):
    """Captured output from a single model generation call.

    Attributes:
        model: Model identifier.
        prompt: The full assembled prompt text sent to the model.
        completion: Raw text returned by the model.
        prompt_tokens: Number of input tokens consumed.
        completion_tokens: Number of output tokens generated.
        latency_ms: Wall-clock latency in milliseconds.
        sampling: Dict of sampling parameters used.
    """

    model: str
    prompt: str
    completion: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    sampling: dict = Field(default_factory=dict)


class ValidationRecord(BaseModel):
    """Output from the validator node (Phase 2).

    Attributes:
        ran: Whether validation was executed.
        verdict: One of pass, fail, or soft_pass.
        confidence: Confidence score 0.0–1.0.
        failure_type: Reason for failure if verdict is fail.
    """

    ran: bool = False
    verdict: Optional[str] = None
    confidence: Optional[float] = None
    failure_type: Optional[str] = None


class FallbackRecord(BaseModel):
    """Output from the frontier fallback handler (Phase 2).

    Attributes:
        triggered: Whether fallback was invoked.
        reason: Why fallback was triggered.
        frontier_model: Identifier of the frontier model used.
        frontier_completion: Raw completion from the frontier model.
    """

    triggered: bool = False
    reason: Optional[str] = None
    frontier_model: Optional[str] = None
    frontier_completion: Optional[str] = None


class Trace(BaseModel):
    """Top-level trace record written as one JSONL line per request.

    Covers identity, input, routing, generation, reserved future fields,
    output, and metadata. Instantiated at the start of handle() and
    written to the sink in a finally block.
    """

    schema_version: str = SCHEMA_VERSION
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_trace_id: Optional[str] = None
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
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
        """Serialize the trace as a single-line JSON string."""
        return self.model_dump_json()

    def capture_exception(self, exc: Exception) -> None:
        """Record exception details into the trace error field.

        Stores the exception type name, message, and full traceback.
        """
        self.error = f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
