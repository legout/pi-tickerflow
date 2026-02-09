# Implementation: pt-cc9t

## Summary
Added `tf ui` CLI subcommand that launches a minimal Textual TUI application.

## Files Changed
- `tf_cli/ui.py` - New module with Textual app skeleton and TTY detection
- `tf_cli/cli.py` - Added `ui` command to help text and routing

## Key Decisions
1. **TTY Detection**: Added check using `sys.stdin.isatty()` and `sys.stdout.isatty()` to ensure the UI only runs in interactive terminals. Exits with clear error message if not a TTY.

2. **Graceful Degradation**: Textual is imported inside the main function so the CLI doesn't fail if Textual isn't installed. Shows helpful error message if import fails.

3. **Minimal Skeleton**: Created a placeholder app with centered text, Header, Footer, and 'q' to quit binding. This provides the foundation for future Kanban board implementation.

4. **Module Structure**: Followed existing patterns in tf_cli - each command is a separate module with a `main(argv)` function.

## Acceptance Criteria
- [x] `tf ui` is routed from `tf_cli/cli.py` to new `tf_cli/ui.py` module
- [x] Running `tf ui` in a TTY opens a minimal Textual app (placeholder screen)
- [x] Running `tf ui` without a TTY exits with clear message: "Error: tf ui requires an interactive terminal (TTY)"

## Tests Run
- Syntax validation: `python -m py_compile tf_cli/ui.py tf_cli/cli.py` - OK
- Import test: `from tf_cli import ui` - OK
- Help text: `tf --help` shows `tf ui` - OK
- TTY detection: `tf ui` from non-TTY exits with error - OK

## Verification
```bash
# Check help includes ui
tf --help

# Try running without TTY (should fail with clear message)
echo "test" | tf ui
```
