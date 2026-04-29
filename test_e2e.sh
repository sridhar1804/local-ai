#!/bin/bash
set -euo pipefail
cd /home/ubuntu/ai/code
/home/ubuntu/ai/bin/python3 -m main "What is the capital of France?"
echo "==="
echo "Trace:"
tail -1 logs/traces/2026-04-28.jsonl | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('final_output:', d['final_output'])
print('prompt tokens:', d['generation']['prompt_tokens'])
print('completion tokens:', d['generation']['completion_tokens'])
print('latency_ms:', d['generation']['latency_ms'])
print('decision_path:', d['decision_path'])
"
