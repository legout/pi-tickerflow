# Review: pt-7cri

## Overall Assessment
The verbosity control logic is clearly organized: `LogLevel`, `resolve_log_level`, and `log_level_to_flag` lay out CLI/env/config priority while consistently pushing the resulting flag into the workflow invocation. Argument parsing for `ralph run`/`ralph start` was extended in-place so that CLI users can request verbosity changes up front without any additional plumbing. However, the new surface area still lacks automated coverage and the user-facing help message is misleading.

## Critical (must fix)
- None.

## Major (should fix)
- `tf_cli/ralph_new.py:287-807` - The new verbosity controls (argument parsing in `parse_run_args`/`parse_start_args`, the `resolve_log_level` utility, and the addition of the level flag to `workflow_flags`) are untested. There are no new unit or regression tests exercising the CLI flag combinations, the environment-variable shortcuts, or the propagation of the resulting flag into the workflow invocation, so regressions in the newly added priority order (CLI > env > config > default) could easily slip in. Please add focused tests that cover the parse-and-resolve logic plus flag formatting so we can guard these interactions.

## Minor (nice to fix)
- `tf_cli/ralph_new.py:65-88` - The `usage()` text still advertises `tf new ralph run/start`, even though the CLI entrypoint is `tf ralph ...` (`tf_cli/cli.py` routes the `ralph` command to this module). This mismatch will confuse users consulting `--help`; updating the usage text to reference the actual command name (and/or explaining the alias) would keep the documentation accurate.

## Warnings (follow-up ticket)
- None.

## Suggestions (follow-up ticket)
- None.

## Positive Notes
- The introduction of the `LogLevel` enum plus `resolve_log_level` and `log_level_to_flag` (lines 16‑333) documents the CLI/env/config precedence explicitly and keeps the verbosity decision centralized before the workflow is invoked.

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 1
- Warnings: 0
- Suggestions: 0