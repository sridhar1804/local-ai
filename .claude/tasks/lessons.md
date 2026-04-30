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

---
_Last updated: 2026-04-28_
