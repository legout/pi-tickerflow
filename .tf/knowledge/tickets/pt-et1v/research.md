# Research: pt-et1v

## Status
Research enabled. No additional external research was performed - this is an audit/fix ticket for existing functionality.

## Rationale
- Ticket is about auditing CSS/assets when served via `textual serve`
- The Textual app (`tf_cli/ui.py`) uses inline CSS (defined in the `CSS` class variable)
- No external CSS files are loaded by the Textual app itself
- Potential issue: Path resolution for knowledge directory when running under `textual serve`

## Context Reviewed
- `tf_cli/ui.py` - Textual app with inline CSS
- `tf_cli/web_ui.py` - Sanic-based web UI (separate from textual serve)
- Previous tickets pt-sf9w, pt-ls9y verified `textual serve` functionality
- Plan mentions risk: "relative paths may not resolve correctly under web serving"

## Key Findings
1. CSS is inline in `TicketflowApp.CSS` - no external CSS file to load
2. Path resolution uses `resolve_knowledge_dir()` which checks:
   - `TF_KNOWLEDGE_DIR` env var
   - `.tf/config/settings.json` workflow.knowledgeDir
   - Default: `.tf/knowledge` relative to repo root or CWD
3. The `__main__` block has a check for non-TTY environments (line ~450)

## Sources
- `tf_cli/ui.py` - Main Textual app
- `.tf/knowledge/topics/plan-allow-to-serve-the-textual-app-as-a-web/plan.md`
