# Research: pt-pje2

## Status
Research enabled. Analysis complete based on existing plan documentation.

## Context Sources
- Plan: `.tf/knowledge/topics/plan-add-progressbar-to-tk-ralph/plan.md`
- Backlog: `.tf/knowledge/topics/plan-add-progressbar-to-tk-ralph/backlog.md`
- Code: `tf_cli/ralph.py` - main CLI implementation

## Key Findings

### Current CLI Structure
- `ralph.py` contains `usage()`, `parse_run_args()`, `parse_start_args()`, `ralph_run()`, `ralph_start()`
- `parse_run_args()` returns: `(ticket_override, dry_run, flags_override, log_level, capture_json)`
- `parse_start_args()` returns a dict with: `max_iterations`, `dry_run`, `parallel_override`, `no_parallel`, `flags_override`, `log_level`, `capture_json`

### Existing Flags Pattern
- Verbosity: `--verbose`, `--debug`, `--quiet`
- Existing flags: `--dry-run`, `--capture-json`, `--flags '...'`, `--max-iterations N`, `--parallel N`, `--no-parallel`
- Help: `--help`, `-h`

### New Flags Required
1. `--progress` / `--progressbar` - Enable progress indicator
2. `--pi-output={inherit|file|discard}` - Control pi subprocess output
3. `--pi-output-file <path>` - Optional override for log file path

### Validation Rules (per plan)
- `--progress` in TTY requires `--pi-output=file` (unless user explicitly chose `discard`)
- If `--pi-output=inherit` with `--progress` in TTY, warn and override to `file`
- `--parallel > 1` + `--progress` should be rejected (MVP scope guard)

### Test Location
- Tests in `tests/test_json_capture.py` follow similar pattern for flag parsing tests

## Implementation Notes
- Keep default behavior unchanged (opt-in feature)
- Update `usage()` help text to document new flags
- Return new values from parsers, validate in caller functions
- No rendering implementation yet (that's pt-pnli)
