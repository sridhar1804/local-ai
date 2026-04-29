# Project Context

## What This Is

Python framework for building AI agents. Currently implementing Phase 1 POC — single-GPU Phi-3 Mini 4K inference with vLLM, structured tracing, and agent harness.

Three core packages:

- `models/` — LLM client abstractions (`client.py` for vLLM HTTP wrapper)
- `agents/` — Agent implementations (`main_agent.py`, `router.py`)
- `memory/` — Trace schema (`trace.py`) and persistence layer (`sink.py`)

## Current State

**Phase 1 complete.** `python -m main "<query>"` returns completions via vLLM, writes JSONL traces with full schema. Benchmark: 83.3 tok/s on RTX 3090.

Key files:
- `main.py` — entry point with canonical control flow
- `models/server.sh` — vLLM launch script
- `memory/trace.py` — Trace schema v1.0.0
- `agents/main_agent.py` — single handler

## Environment

- **venv**: `/home/ubuntu/ai/` (project at `/home/ubuntu/ai/code/`)
- **vLLM**: v0.19.1, port 8000
- **GPU**: RTX 3090, 24 GB VRAM
- **Python**: 3.12.3
- **Model**: Phi-3-mini-4k-instruct (7.2 GB cached)

## Open Questions / Decisions Pending

- Adjust SYSTEM_PROMPT or swap model if Phi-3 Mini responses remain inconsistent
- Phase 2: multi-agent supervision, tool calling, validator nodes

## Key Decisions Made

1. **Trace-first design**: `memory/trace.py` anchors the observability substrate. Reserved fields (`retrieval`, `tool_calls`, `validation`, `fallback`) present in v1.0.0 even though unused.
2. **Protocol over ABC**: TraceSink uses structural typing.
3. **Router placeholder**: Built in Phase 1 to avoid refactoring `main.py` in Phase 2.
4. **Venv-as-parent**: The venv (`/home/ubuntu/ai/`) is the parent of the project directory (`/home/ubuntu/ai/code/`).

---
_Last updated: 2026-04-28 (Phase 1 complete)_
