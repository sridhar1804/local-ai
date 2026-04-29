# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Session Protocol

### At Session Start — ALWAYS do this first

1. Read [memory/INDEX.md](memory/INDEX.md)
2. Read [memory/workflow/rules.md](memory/workflow/rules.md) — governs all work
3. Read [memory/project/context.md](memory/project/context.md)
4. Read [memory/user/profile.md](memory/user/profile.md)
5. Read [memory/lessons/patterns.md](memory/lessons/patterns.md)
6. Read [memory/sessions/latest.md](memory/sessions/latest.md)

### At Session End — ALWAYS do this before closing

1. Update [memory/sessions/latest.md](memory/sessions/latest.md) — what was done, decisions made, open threads
2. Update [memory/lessons/patterns.md](memory/lessons/patterns.md) — if any corrections or new patterns emerged
3. Update [memory/project/context.md](memory/project/context.md) — if architecture or goals changed
4. Update [memory/user/profile.md](memory/user/profile.md) — if new preferences were observed
5. Update [tasks/lessons.md](tasks/lessons.md) — after any correction from the user

---

## Workflow Rules

> These rules govern ALL planning and execution in this repo. Non-negotiable.

### 1. Plan Mode (Default)

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, **STOP and re-plan immediately** — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagents Strategy

- Use subagents liberally to keep the main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop

- After ANY correction from the user, update [tasks/lessons.md](tasks/lessons.md) with the pattern
- Write rules to prevent the same mistakes
- Ruthlessly iterate on these lessons until mistake rate drops
- Review [tasks/lessons.md](tasks/lessons.md) at session start

### 4. Verification Before Completion

- Never mark a task completed without proving it works
- Diff behavior between main and your changes when relevant
- Ask: "Would a senior engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "Is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer

### 6. Autonomous Bug Fixing

- When given a bug report: just fix it. No hand-holding.
- Point at logs, errors, failing tests — then resolve them
- Go fix failing CI tests without being told how

### 7. Boil the Ocean

The marginal cost of completeness is near zero with AI.

- Do the whole thing. Do it right. Do it with tests. Do it with documentation.
- Do it so well that Garry Tan is **genuinely** impressed — not politely satisfied.
- Never offer to "table this for later" when a permanent solve is within reach
- Never leave a dangling thread when tying it off takes five more minutes
- Never present a workaround when a real fix exists
- The standard isn't "good enough" — it's "holy shit, that's done"
- Search before building. Test before shipping. Ship the complete thing.

### Task Management Protocol

1. **Plan First** — Write plan to [tasks/todo.md](tasks/todo.md) with checkable items
2. **Verify Plan** — Check in before starting implementation on large tasks
3. **Track Progress** — Mark items complete as you go using TodoWrite
4. **Explain Changes** — High-level summary at each step
5. **Document Results** — Add review section to [tasks/todo.md](tasks/todo.md)
6. **Capture Lessons** — Update [tasks/lessons.md](tasks/lessons.md) after corrections

### Core Principles

- **Simplicity First** — Make every change as simple as possible. Minimal code impact.
- **No Laziness** — Find root causes. No temporary fixes. Senior developer and production-ready standards.
- **Minimal Impact** — Changes should only touch what's necessary.
- **Memory Management** — Update memory files after every session.
- **CLAUDE.md Currency** — Keep this file up-to-date as the project evolves.

---

## Project Structure

Python framework for building AI agents:

- `models/` — LLM client abstractions (`client.py`)
- `agents/` — Agent implementations
- `memory/` — Memory and persistence layer for agents
- `tasks/` — Task tracking (`todo.md`, `lessons.md`)

### Memory Network Layout

```
memory/
  INDEX.md              ← start here every session
  workflow/rules.md     ← governing execution rules
  project/context.md    ← project state, decisions, open questions
  user/profile.md       ← user preferences and collaboration style
  lessons/patterns.md   ← learned patterns and anti-patterns
  sessions/latest.md    ← previous session handoff
```
