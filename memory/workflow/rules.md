# Workflow Rules

>applies to ALL work in this repo from this point forward.

---

## 1. Plan Mode (Default)

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, **STOP and re-plan immediately** — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

## 2. Subagents Strategy

- Use subagents liberally to keep the main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

## 3. Self-Improvement Loop

- After ANY correction from the user, update `tasks/lessons.md` with the pattern
- Write rules to prevent the same mistakes
- Ruthlessly iterate on these lessons until mistake rate drops
- Review `tasks/lessons.md` at session start for the relevant project

## 4. Verification Before Completion

- Never mark a task as completed without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a senior engineer approve this?"
- Run tests, check logs, demonstrate correctness

## 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "Is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting

## 6. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## 7. Boil the Ocean
The marginal cost of completeness is near zero with ai.
Do the whole thing.
Do it right.
Do it with tests.
Do it with documentation.
Do it so well that Garry Tan is impressed - not politely satisfied , genuinely impressed.
Never offer to "table this for later" when a permanent solve is within reach.
Never leave a dangling thread when tying it off takes five more minutes.
Never present a workaround when a real fix exists.
The standard isnt "good enough" - its "holy shit , thats done".
Search before building. Test before shipping.
Ship the complete thing.
When Garry asks for something, the answer is the finished product, not a plan to build it.
Time is not an excuse. Fatigue is not an excuse. Complexity is not an excuse. Boil the ocean.
---

## Task Management Protocol

1. **Plan First** — Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan** — Check in before starting implementation
3. **Track Progress** — Mark items complete as you go
4. **Explain Changes** — High-level summary at each step
5. **Document Results** — Add review section to `tasks/todo.md`
6. **Capture Lessons** — Update `tasks/lessons.md` after corrections

---

## Core Principles

- **Simplicity First** — Make every change as simple as possible. Minimal code impact.
- **No Laziness** — Find root causes. No temporary fixes. Senior developer and production-ready standards.
- **Minimal Impact** — Changes should only touch what's necessary. Avoid introducing bugs.
- **Memory management** : Update the memory files after every session with what youve learnt.
- **Claude updates** : Keep the claude.md file updates with the most up-to-date information