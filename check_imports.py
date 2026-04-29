#!/usr/bin/env python3
"""Quick validation of all modules."""
import sys
sys.path.insert(0, "/home/ubuntu/ai/code")

from memory.trace import Trace, GenerationRecord, ValidationRecord, FallbackRecord, SCHEMA_VERSION
from memory.sink import NullSink, JsonlTraceSink
from models.client import Phi3Client, GenerationResult
from agents.main_agent import SYSTEM_PROMPT, run as agent_run
from agents.router import route

print(f"SCHEMA_VERSION: {SCHEMA_VERSION}")
t = Trace(input_query="test")
print(f"Trace OK: {t.trace_id[:8]}...")
line = t.to_jsonl()
import json
parsed = json.loads(line)
assert parsed["schema_version"] == "1.0.0"
assert parsed["validation"]["ran"] == False
assert parsed["fallback"]["triggered"] == False
assert parsed["retrieval"] is None
assert parsed["tool_calls"] == []
print("JSONL roundtrip OK")

sink = NullSink()
sink.write(t)
print("NullSink OK")

from pathlib import Path
import tempfile
with tempfile.TemporaryDirectory() as td:
    sink2 = JsonlTraceSink(log_dir=td)
    sink2.write(t)
    files = list(Path(td).glob("*.jsonl"))
    assert len(files) == 1
    print("JsonlTraceSink OK")

d = route("hello")
assert d.route == "main_agent"
assert d.reason == "phase_1_default"
print("Router OK")

print("SYSTEM_PROMPT:", SYSTEM_PROMPT[:50])
print()
print("ALL IMPORTS AND BASIC TESTS PASS")
