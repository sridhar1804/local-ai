# Learned Patterns & Anti-Patterns

## Anti-Patterns (Never Do)

- **WSL path confusion with Write tool**: The Write tool resolves `\\wsl.localhost\Ubuntu-24.04\home\ubuntu\ai\code\` to the Windows C: drive sometimes, not the WSL filesystem. Always verify files landed at the correct WSL path after writing. Alternative: use `wsl bash -c 'cat > /path/file << EOF'` for critical files.
- **Nested quotes through PowerShell→WSL→bash→python**: Multiple layers of quote escaping fail silently. Write scripts to files and execute them, don't inline multi-line Python in `wsl bash -c`.
- **PowerShell interprets `|` and `||`**: Use `;` or write scripts instead of piping inside `wsl bash -c`.

## Patterns That Work

- **Write tool + `\\wsl.localhost\...` path**: Works correctly for writing files to WSL when using the full UNC path. Files end up at the correct WSL location.
- **Shell scripts for complex commands**: Write `.sh` scripts with Write tool, `chmod +x`, then execute via `wsl bash /path/script.sh`. Avoids all quoting hell.
- **Background processes via `&` + wait loop**: Start vLLM with `&` inside a script, then poll health endpoint. The WSL session stays alive as long as the bash command is running.
- **Version spec flexibility**: When working with a spec that targets older versions (e.g., vLLM 0.6.x), check CLI `--help` for the current version's flags. Most flags survive, some are renamed.

## Rules Derived From Corrections

- **Check file locations after Write tool**: Always run `wsl bash -c 'ls -la <path>'` to verify files landed in WSL, not on the Windows C: drive.
- **Version audit before implementation**: Check actual installed versions against spec. v1.md targeted vLLM 0.6.x but 0.19.1 is installed — flags differ. Audit first, code second.

## New Patterns Added This Session (2026-04-30)

- **Comprehensive file rewrite vs incremental edits**: When applying 10+ style fixes to a file (docstrings, logging, imports, formatting), rewriting the entire file with Write tool produces cleaner results than chaining Edit calls.
- **dynaconf setup pattern**: Create `settings.toml` with defaults, optional `.secrets.toml` (gitignored), and a `config.py` that exports module-level constants accessed by other modules. Use `Dynaconf(settings_files=[...])` without `environments=True` unless multi-env is needed.

---
_Last updated: 2026-04-30_
