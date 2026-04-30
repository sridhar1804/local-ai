# Phase 1 POC — Phi-3 Mini 4K Agent Harness

Single-GPU Phi-3 Mini 4K inference path on WSL, backed by vLLM. Structured JSONL tracing on every call.

## Requirements

- WSL 2 with NVIDIA GPU passthrough
- NVIDIA RTX 3090 (or any GPU with >= 10 GB VRAM)
- Python 3.10+

## Quickstart

### 1. Activate the venv

```bash
source /home/ubuntu/ai/bin/activate
cd /home/ubuntu/ai/code
```

### 2. Start the vLLM server

In one terminal:

```bash
bash models/server.sh
```

Or to launch in background with auto-ready detection:

```bash
bash start_vllm.sh
```

Wait for `vLLM ready`. First launch compiles CUDA graphs (~60s). Subsequent launches are faster.

### 3. Run a query

```bash
python -m main "What is the capital of France?"
```

Output goes to stdout. One JSONL trace is written to `logs/traces/<UTC-date>.jsonl`.

### 4. View traces

```bash
cat logs/traces/$(date -u +%Y-%m-%d).jsonl | python3 -m json.tool
```

## Architecture

```
config.py         → centralized dynaconf settings + structured JSON logging
main.py           → entry point, canonical control flow
agents/
  router.py       → RouteDecision placeholder (always main_agent)
  main_agent.py   → single handler, prompt assembly + model call
models/
  client.py       → Phi3Client: thin vLLM HTTP wrapper
  server.sh       → vLLM launch script
model_memory/
  trace.py        → Pydantic Trace schema v1.0.0
  sink.py         → JsonlTraceSink (daily-rotated JSONL), NullSink
tests/
  conftest.py, test_*.py
                  → 58 pytest tests (full pipeline coverage)
.claude/memory/
  INDEX.md, workflow/, project/, sessions/, lessons/, user/
                  → agent (Claude) knowledge base, Markdown only
```

## Configuration

All runtime settings are in `config.py`, sourced from `settings.toml` (committed)
and `.secrets.toml` (gitignored). Import from `config`:

```python
from config import BASE_URL, MODEL, TIMEOUT, LOG_DIR
```

## Trace Schema

Every call writes one JSONL line with:

| Group | Key fields |
|-------|-----------|
| Identity | `trace_id`, `schema_version`, `timestamp_utc` |
| Input | `input_query`, `session_id`, `user_id` |
| Routing | `route`, `decision_path` |
| Generation | `generation.model`, `generation.completion`, `generation.latency_ms`, `generation.prompt_tokens`, `generation.completion_tokens` |
| Output | `final_output` |
| Error | `error` (populated with traceback on failure) |

Reserved fields (`retrieval`, `tool_calls`, `validation`, `fallback`) are present at defaults — ready for Phase 2+.

## Running Benchmarks

```bash
bash benchmark.sh
```

Target: >= 80 tok/s single-stream on a 300-token completion.

## Testing

```bash
python -m pytest tests/ -v
```

58 tests covering: trace schema, sinks, client, agent, router, main control flow, and integration.

## Settings

Edit `settings.toml` to change defaults:

| Key | Default | Description |
|-----|---------|-------------|
| `base_url` | `http://localhost:8000/v1` | vLLM server URL |
| `model` | `microsoft/Phi-3-mini-4k-instruct` | HuggingFace model ID |
| `timeout` | `60.0` | HTTP timeout in seconds |
| `log_dir` | `logs/traces` | Trace output directory |
| `log_level` | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |

## Stopping

```bash
kill $(cat logs/vllm.pid)
```

## Project Structure

```
ai/code/
├── main.py
├── __main__.py
├── config.py
├── pyproject.toml
├── settings.toml
├── pinned_versions.txt
├── start_vllm.sh
├── benchmark.sh
├── README.md
├── agents/
│   ├── __init__.py
│   ├── router.py
│   └── main_agent.py
├── models/
│   ├── __init__.py
│   ├── client.py
│   └── server.sh
├── model_memory/
│   ├── __init__.py
│   ├── trace.py
│   └── sink.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_trace.py
│   ├── test_sink.py
│   ├── test_client.py
│   ├── test_agent.py
│   ├── test_router.py
│   ├── test_main.py
│   └── test_integration.py
├── .claude/
│   ├── settings.json
│   ├── commands/
│   ├── agents/
│   ├── memory/
│   │   ├── INDEX.md
│   │   ├── workflow/   (rules.md, code_style.md)
│   │   ├── project/    (context.md)
│   │   ├── sessions/   (YYYY-MM-DD[-suffix].md)
│   │   ├── lessons/    (patterns.md)
│   │   └── user/       (profile.md)
│   ├── tasks/      (todo.md, lessons.md)
│   └── versions/   (v1.md, v2.md, ...)
└── logs/
    └── traces/
        └── YYYY-MM-DD.jsonl
```
