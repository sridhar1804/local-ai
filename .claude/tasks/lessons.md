# Lessons Learned

> Updated after every correction. The goal is zero repeated mistakes.

## Format

Each entry follows:
- **Mistake:** what went wrong
- **Root cause:** why it happened  
- **Rule:** the rule derived to prevent recurrence

---

## Lessons

### 2026-04-28 — WSL Path Resolution

- **Mistake:** Files written with Write tool at `\\wsl.localhost\...` path appeared in WSL at `/mnt/c/home/...` instead of `/home/...`
- **Root cause:** UNC path resolution maps to the Windows C: drive root, not the WSL Linux root.
- **Rule:** Always verify file location with `ls` after writing. Use `\\wsl.localhost\Ubuntu-24.04\home\...` prefix for correct WSL targeting.

### 2026-04-28 — Quote Escaping Through Shell Layers

- **Mistake:** Python code with f-strings, brackets, and apostrophes fails when passed through `wsl bash -c` from PowerShell.
- **Root cause:** PowerShell, bash, and Python each interpret quotes and special characters. Triple-nesting reaches escape limit.
- **Rule:** Write Python scripts to files with the Write tool, then execute with `wsl bash -c '/path/python3 /path/script.py'`. Never inline Python code in shell commands.

> See also: [.claude/memory/lessons/patterns.md](../memory/lessons/patterns.md) for the canonical patterns reference.

### 2026-04-30 — dynaconf Requires Settings Files

- **Mistake:** dynaconf `default_settings` dict not applied when settings_files are specified but files don't exist.
- **Root cause:** Dynaconf 3.x requires the TOML files to exist on disk; `default_settings` only fills in missing keys in existing files.
- **Rule:** Always create `settings.toml` when using dynaconf. The `default_settings` kwarg is a supplement, not a replacement.

---
_Last updated: 2026-04-30_
