#!/bin/bash
# Smoke test vLLM server
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"microsoft/Phi-3-mini-4k-instruct","messages":[{"role":"user","content":"Say hello in exactly 10 words."}],"max_tokens":50,"temperature":0.0}'
