#!/bin/bash
VLLM=/home/ubuntu/ai/bin/vllm
MODEL=microsoft/Phi-3-mini-4k-instruct
LOG=/home/ubuntu/ai/code/logs/vllm.log
PIDFILE=/home/ubuntu/ai/code/logs/vllm.pid

echo "$(date): Starting vLLM $MODEL on port 8000" >> "$LOG"

"$VLLM" serve "$MODEL" \
  --dtype float16 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.85 \
  --port 8000 \
  --disable-uvicorn-access-log \
  >> "$LOG" 2>&1 &
PID=$!
echo "$PID" > "$PIDFILE"
echo "vLLM PID: $PID"

# Wait for server to be ready
for i in $(seq 1 30); do
  sleep 5
  if curl -s -o /dev/null http://localhost:8000/health 2>/dev/null; then
    echo "vLLM ready after ${i}x5 seconds"
    exit 0
  fi
  echo "Waiting... ${i}x5s"
done
echo "Timed out waiting for vLLM"
