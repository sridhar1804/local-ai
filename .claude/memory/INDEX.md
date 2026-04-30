# Memory Network Index

Read this file first at every session start, then read the files listed below.
Update relevant files at every session end.

> This `.claude/memory/` directory is the **agent (Claude) knowledge base** — Markdown only. Code that the *model* uses for runtime memory (trace schema, sinks) lives in [`/model_memory/`](../../model_memory/), a separate Python package. Never put `.py` files here, and never put Markdown context here that the running model code needs.

## Directory Map

| Folder | Purpose |
|--------|---------|
| `workflow/` | Execution rules, planning protocols, task management |
| `project/` | Project goals, architecture decisions, open questions |
| `user/` | User preferences, collaboration style, profile |
| `lessons/` | Mistakes made, patterns learned, rules derived |
| `sessions/` | Per-session summaries and state handoffs |

## Files to Load at Session Start

1. [workflow/rules.md](workflow/rules.md) — **CRITICAL: governing rules for all work**
2. [workflow/code_style.md](workflow/code_style.md) — **CRITICAL: governing style for all code authored in this repo**
3. [project/context.md](project/context.md) — current project state and goals
4. [user/profile.md](user/profile.md) — user preferences and collaboration style
5. [lessons/patterns.md](lessons/patterns.md) — learned patterns and anti-patterns
6. The most recent file in [sessions/](sessions/) — previous session handoff (sessions are dated `YYYY-MM-DD[-suffix].md`, append-only)

## Session End Checklist

- [ ] Write a NEW file `sessions/YYYY-MM-DD[-suffix].md` with full session details (skeleton: see `CLAUDE.md` → Session File Format). Never overwrite prior sessions.
- [ ] Update `lessons/patterns.md` if any corrections or new patterns emerged
- [ ] Update `project/context.md` if architecture or goals changed
- [ ] Update `user/profile.md` if new preferences were expressed
