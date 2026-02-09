# Research: pt-pa5v

## Status
Research enabled. Analysis performed by examining codebase directly.

## Findings

### Drift Identified Between Docs and Actual Implementation

#### 1. docs/configuration.md
- **Model mismatch**: Lists `review-secop` as `github-copilot/grok-code-fast-1` but actual config has `google-antigravity/gemini-3-flash`
- **Config key error**: Example shows `models:` but actual key is `metaModels:`
- **Missing sections**: Example config doesn't include `prompts` mapping
- **Ralph config**: Documents `logFile: true` but actual key is `captureJson`

#### 2. docs/ralph-logging.md
- **Log format**: Documents `TIMESTAMP [LEVEL] ...` but actual format is `TIMESTAMP | LEVEL | key=value | message`
- **Log levels**: Documents ERROR/WARN/INFO/DEBUG but actual values are lowercase (error/warn/info/debug)
- **Events**: Documents events like `iteration_start`, `phase_transition` that don't exist in code
- **Log files**: Documents `.tf/ralph/logs/YYYY-MM-DD.log` but actual is `{ticket}.jsonl` when capture enabled
- **Session traces**: Location is correct (`.tf/ralph/sessions/`), but notes automatic capture which is opt-in

#### 3. docs/commands.md
- **Command name mismatch**: Documents `/tf-priority-reclassify` prompt but actual CLI uses `tf new priority-reclassify`
- Examples correctly show `tf new priority-reclassify` but header is inconsistent

#### 4. README.md
- Shows `tf priority-reclassify` but actual is `tf new priority-reclassify`
- References `/simplify` command that doesn't exist in codebase

### Implementation Verified

The actual implementation in `tf_cli/` matches these behaviors:
- `ralph_new.py`: Uses `captureJson`, `logLevel` config keys
- `logger.py`: Uses pipe-delimited format with lowercase levels
- `new_cli.py`: Routes `tf new priority-reclassify` correctly

## Sources
- `.tf/config/settings.json` (actual config)
- `tf_cli/ralph_new.py` (actual Ralph implementation)
- `tf_cli/logger.py` (actual logging format)
- `docs/configuration.md`, `docs/ralph-logging.md`, `docs/commands.md` (to be fixed)
