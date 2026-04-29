#!/bin/bash
set -euo pipefail

MODEL_NAME="${MODEL_NAME:-microsoft/Phi-3-mini-4k-instruct}"
VLLM_PORT="${VLLM_PORT:-8000}"
GPU_UTIL="${GPU_UTIL:-0.85}"

echo "Starting vLLM server..."
echo "  Model:      $MODEL_NAME"
echo "  Port:       $VLLM_PORT"
echo "  GPU util:   $GPU_UTIL"

vllm serve "$MODEL_NAME" \
  --dtype float16 \
  --max-model-len 4096 \
  --gpu-memory-utilization "$GPU_UTIL" \
  --port "$VLLM_PORT" \
  --disable-uvicorn-access-log
