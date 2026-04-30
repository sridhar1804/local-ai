# User Profile

## Identity

- Email: vvss1804@gmail.com

## Collaboration Style

- Wants complete, production-ready output — not plans, not partials, not workarounds
- "Boil the ocean" standard: if a permanent solve is within reach, do it fully
- No hand-holding: given a bug or task, just fix it autonomously
- Explicitly dislikes tabling things for later when a full solution is reachable now

## Quality Bar

- Code should be good enough that Garry Tan is **genuinely** impressed, not politely satisfied
- Tests, docs, correctness — all included, not optional
- "Holy shit, that's done" is the target, not "good enough"

## Preferences

- Uses WSL 2 with NVIDIA GPU passthrough for local LLM development
- Prefers vLLM as the inference runtime (over llama.cpp, HF transformers)
- Python 3.12, venv-based isolation
- Version pinning matters (`pinned_versions.txt`)
- Structured observability from day one (JSONL traces, not printf debugging)
- Forward-compatible design: placeholder components built now to avoid refactoring later

---
_Last updated: 2026-04-28_
