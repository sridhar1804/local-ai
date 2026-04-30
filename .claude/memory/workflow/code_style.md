# coding_style.md — Authoring Style Guide

## CORE PHILOSOPHY

Write code that holds up under extensive testing. When solving a problem, search for the elegant path before reaching for a complex one. Prefer clean, readable code that is easy to debug over clever code that is hard to follow. Keep structure tight — do not write hundreds of lines when tens will do. Be concise. For every implementation, ask whether there is a more elegant way to express the same logic, and choose that one.

Every rule below is in service of this philosophy. If a rule and the philosophy ever conflict, the philosophy wins.

---

## 1. NAMING

- No abbreviations. Spell every word.
- `snake_case` for variables, functions, modules. `PascalCase` for classes. `ALL_CAPS` for constants.
- Booleans prefixed with `is_`, `has_`, or `should_`.
- Functions named in one or two words that describe what they do. If you need three words, the function probably does too much.
- Private methods use double underscore. Used sparingly.
- File names follow the same rules as functions — descriptive, snake_case, no version suffixes.

---

## 2. FUNCTIONS

- Maximum 30–40 lines per function. If longer, split it.
- Single return at the bottom. No scattered early returns.
- Functions return new values. Do not mutate arguments.
- Lambdas are fine for short transformations and callbacks. If a lambda needs a name, it needs `def` instead.
- If parameters cluster semantically, group them into a dataclass or Pydantic model.

---

## 3. TYPE HINTS & DATA STRUCTURES

- Type-hint everything. All parameters, all returns, all class attributes. No exceptions.
- Use `Optional[X]` and `Union[X, Y]`.
- Use `list[dict]` inline. Only alias a shape when it appears 3+ times in the same module.
- Reach for the leftmost option that fits: Pydantic for external boundaries and validation, dataclass for internal value objects, TypedDict only when interfacing with code that expects a plain dict.

---

## 4. ERROR HANDLING

- Catch narrow, specific exceptions. Never bare `except` or broad `except Exception` unless re-raising.
- Use built-in exception classes with descriptive messages. Do not write custom exception classes.
- On error: log it, then raise it. Do not swallow errors or hide them behind sentinel return values.
- Wrap only the lines that can actually raise. Use the full `try/except/else/finally` construct when it adds clarity.

---

## 5. DOCSTRINGS & COMMENTS

- Every function, class, and module gets a docstring.
- Maximum 5 lines per docstring. Google style.
- Module docstrings are one to three lines, stating what the module is for.
- Inline comments are sparing. The docstring carries the explanation.
- No `TODO`, `FIXME`, or `HACK` tags. Clean as you go. If a refactor is needed, do it now.

---

## 6. IMPORTS

- All imports at the top of the file.
- `from x import y` preferred for individual symbols. `import x` is fine when many symbols are pulled or the namespace itself matters.
- Order: standard library, then third-party, then local. Blank line between each group.
- File length capped at 200–250 lines including imports and docstrings. Past that, split into modules.

---

## 7. CLASSES

- Use a class when state is needed or when grouping related methods makes the code clearer. Do not avoid classes on principle, but do not write them when a function would do.
- `@dataclass`, `@staticmethod`, `@classmethod` used freely where appropriate.
- Inheritance is fine. Composition is also fine. Choose whichever expresses the relationship more directly.
- Write `__repr__` and `__str__` only when debugging genuinely demands them.

---

## 8. CONFIGURATION

- All configuration centralised in one file. No scattered environment variable reads across the codebase.
- Use `dynaconf`. Access config through a wrapped `settings` object, never raw `os.environ`.
- Validate required keys at startup. Fail fast — if a required value is missing, the process must not start.
- Constants live at module level, `ALL_CAPS`, just below imports.

---

## 9. LOGGING

- Use `logging` from day one. Never `print`.
- Root logger. Structured JSON payloads — one JSON object per log line.
- Use all four levels strictly: `DEBUG` for stepping through failures, `INFO` for meaningful state changes, `WARNING` for recoverable anomalies, `ERROR` for unrecoverable failures (always paired with a raise).
- Log meaningful state changes and external boundary crossings. Do not log routine function entry and exit.
- Never log API keys, tokens, or sensitive payloads.

---

## 10. TESTING

- Write tests during implementation, not before or after.
- `pytest` and `unittest` are both acceptable. Match what the repo already uses.
- Prefer integration-style tests that hit real code paths. Mock only at boundaries that are slow, paid, or non-deterministic.
- Test what matters first. Once core paths pass, add coverage tests for robustness on edge cases. Do not chase a coverage percentage as the goal.
- Test both private and public functions when private logic is worth testing.

---

## 11. FORMATTING

- Multi-line brackets: opening bracket starts a new line context, every item on its own line, closing bracket on its own line.
- Trailing commas in all multi-line collections and signatures.
- Blank lines between logical blocks inside a function. Two blank lines between top-level definitions.
- Soft line length limit of 100 characters. If a line wraps, use the multi-line bracket pattern.

---

## 12. TRADE-OFFS

- Performance wins when it conflicts with readability at the micro level. Note the trade-off in the docstring if a reader would be surprised.
- Refactor before committing. Do not ship code known to be ugly with intent to clean later.
- 2–3 levels of nesting is acceptable. Past that, extract a helper.
- A small amount of duplication is better than a premature abstraction.
- If the same function keeps needing to be debugged, that is a signal to rewrite it for clarity, even at a small performance cost.

---

## THE FINGERPRINT

Code written in this style is recognisable by:

- Short, descriptive function names — one or two words.
- Tight files, deep folders, no clutter.
- Type hints on everything, docstrings short and present.
- Single return at the bottom of every function.
- Multi-line brackets opening and closing on their own lines.
- Logging structured as JSON from the first commit.
- Whatever solves the problem in the fewest lines that still read cleanly.