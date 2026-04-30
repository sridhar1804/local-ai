# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Session Protocol

### At Session Start — ALWAYS do this first

1. Read [.claude/memory/INDEX.md](.claude/memory/INDEX.md)
2. Read [.claude/memory/workflow/rules.md](.claude/memory/workflow/rules.md) — governs all work
3. Read [.claude/memory/workflow/code_style.md](.claude/memory/workflow/code_style.md) — **governs all code authored in this repo**
4. Read [.claude/memory/project/context.md](.claude/memory/project/context.md)
5. Read [.claude/memory/user/profile.md](.claude/memory/user/profile.md)
6. Read [.claude/memory/lessons/patterns.md](.claude/memory/lessons/patterns.md)
7. Read the most recent file in [.claude/memory/sessions/](.claude/memory/sessions/) — sessions are stored as dated files (`YYYY-MM-DD[-suffix].md`); the latest one is the handoff

### At Session End — ALWAYS do this before closing

1. Write a NEW dated file at `.claude/memory/sessions/YYYY-MM-DD[-suffix].md` (use `today`'s date; add a short suffix like `-restructure`, `-bugfix`, `-build` if multiple sessions occur in one day) — full details: what was built, decisions made, files changed, open threads. Never overwrite a previous session's file. Format below.
2. Update [.claude/memory/lessons/patterns.md](.claude/memory/lessons/patterns.md) — if any corrections or new patterns emerged
3. Update [.claude/memory/project/context.md](.claude/memory/project/context.md) — if architecture or goals changed
4. Update [.claude/memory/user/profile.md](.claude/memory/user/profile.md) — if new preferences were observed
5. Update [.claude/tasks/lessons.md](.claude/tasks/lessons.md) — after any correction from the user

### Session File Format

Each dated session file uses this skeleton. Sections may be omitted if empty for that session, but the order is fixed.

```markdown
# Session — YYYY-MM-DD[-suffix]

## What Was Done
<bulleted list of substantive work items, grouped by area>

## Decisions Made
<each decision: one line stating the decision, one line on the rationale>

## Files Changed
<list of edited paths with a one-line note on the change>

## New Files
<list of newly created paths with a one-line note on purpose>

## Files Moved / Deleted
<git mv pairs, deletions; one line each>

## Build & Test Results
<commands run, pass/fail, any benchmarks>

## Open Threads
<questions left, follow-ups, anything the next session should pick up>

## Next Session
<one or two lines on what should happen first next time>
```

Sessions are append-only history — never edit a previous session's file except to fix a typo. If a follow-up session corrects something, that correction lives in the new session's file.

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

- After ANY correction from the user, update [.claude/tasks/lessons.md](.claude/tasks/lessons.md) with the pattern
- Write rules to prevent the same mistakes
- Ruthlessly iterate on these lessons until mistake rate drops
- Review [.claude/tasks/lessons.md](.claude/tasks/lessons.md) at session start

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

1. **Plan First** — Write plan to [.claude/tasks/todo.md](.claude/tasks/todo.md) with checkable items
2. **Verify Plan** — Check in before starting implementation on large tasks
3. **Track Progress** — Mark items complete as you go using TodoWrite
4. **Explain Changes** — High-level summary at each step
5. **Document Results** — Add review section to [.claude/tasks/todo.md](.claude/tasks/todo.md)
6. **Capture Lessons** — Update [.claude/tasks/lessons.md](.claude/tasks/lessons.md) after corrections

### Core Principles

- **Simplicity First** — Make every change as simple as possible. Minimal code impact.
- **No Laziness** — Find root causes. No temporary fixes. Senior developer and production-ready standards.
- **Minimal Impact** — Changes should only touch what's necessary.
- **Memory Management** — Update memory files after every session.
- **CLAUDE.md Currency** — Keep this file up-to-date as the project evolves.

---

## Coding Style

> All code authored in this repo MUST follow [.claude/memory/workflow/code_style.md](.claude/memory/workflow/code_style.md). Non-negotiable.

- Read [.claude/memory/workflow/code_style.md](.claude/memory/workflow/code_style.md) at session start, alongside the workflow rules.
- Apply it to every file you create or edit — naming, function shape, type hints, error handling, docstrings, imports, classes, configuration, logging, testing, formatting, and trade-offs.
- If a request conflicts with the style guide, surface the conflict before writing code rather than silently deviating.
- The fingerprint at the bottom of the style guide is the bar — if your output does not look like it, rewrite before shipping.

---

## Project Structure

Python framework for building AI agents:

- `models/` — LLM client abstractions (`client.py`)
- `agents/` — Agent implementations
- `model_memory/` — **Runtime memory for the model**: trace schema (`trace.py`), persistence sinks (`sink.py`). Imported as a Python package.
- `.claude/memory/` — **Agent (Claude) knowledge base**: rules, coding style, project context, sessions, lessons, user profile. Markdown only — never put code here.
- `.claude/tasks/` — Task tracking (`todo.md`, `lessons.md`)
- `.claude/versions/` — Versioned design specs (`v1.md`, `v2.md`, ...)

> The split: `model_memory/` is what the *model* writes (traces of its own runs). `.claude/memory/` is what the *agent assistant* reads and writes (durable working knowledge across sessions). Never mix them.

### Memory Network Layout

```
.claude/memory/
  INDEX.md                ← start here every session
  workflow/rules.md       ← governing execution rules
  workflow/code_style.md  ← governing code authoring style
  project/context.md      ← project state, decisions, open questions
  user/profile.md         ← user preferences and collaboration style
  lessons/patterns.md     ← learned patterns and anti-patterns
  sessions/latest.md      ← previous session handoff
```
