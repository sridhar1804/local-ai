#!/bin/bash
# Benchmark: measure tok/s for a ~300 token completion
set -euo pipefail

PROMPT="Explain the process of photosynthesis in detail, covering light-dependent and light-independent reactions, the role of chlorophyll, and the overall chemical equation. Be thorough and educational."
MAX_TOKENS=300
TEMPERATURE=0.0

START=$(date +%s%N)

RESPONSE=$(curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"microsoft/Phi-3-mini-4k-instruct\",\"messages\":[{\"role\":\"user\",\"content\":\"$PROMPT\"}],\"max_tokens\":$MAX_TOKENS,\"temperature\":$TEMPERATURE}")

END=$(date +%s%N)

# Extract token counts
COMPLETION_TOKENS=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['usage']['completion_tokens'])")
PROMPT_TOKENS=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['usage']['prompt_tokens'])")
COMPLETION=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'])")

ELAPSED_MS=$(( (END - START) / 1000000 ))
ELAPSED_S=$(echo "scale=2; $ELAPSED_MS / 1000" | bc 2>/dev/null || echo "$((ELAPSED_MS / 1000))")
TOK_PER_S=$(echo "scale=1; $COMPLETION_TOKENS / ($ELAPSED_MS / 1000)" | bc 2>/dev/null || echo "N/A")

echo "========================================="
echo "  BENCHMARK RESULTS"
echo "========================================="
echo "  Completion tokens:  $COMPLETION_TOKENS"
echo "  Prompt tokens:      $PROMPT_TOKENS"
echo "  Wall time:          ${ELAPSED_MS}ms (${ELAPSED_S}s)"
echo "  Throughput:         ${TOK_PER_S} tok/s"
echo "========================================="

if command -v bc &> /dev/null; then
  THRESHOLD=80
  if (( $(echo "$TOK_PER_S >= $THRESHOLD" | bc -l) )); then
    echo "  PASS: >= ${THRESHOLD} tok/s"
  else
    echo "  WARNING: Below ${THRESHOLD} tok/s"
  fi
else
  echo "  Target: >= 80 tok/s"
fi

echo "========================================="
echo ""
echo "Completion sample:"
echo "$COMPLETION" | head -c 500
echo ""
echo "..."
