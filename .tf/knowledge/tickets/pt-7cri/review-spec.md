# Review (Spec Audit): pt-7cri

## Overall Assessment
Verbosity flags, environment variables, and the config upgrade described in pt-7cri are wired into `tf ralph start` and `tf ralph run` and documented in `--help`, so the CLI accepts the requested options. However, the new log-level resolution is never used when emitting the CLI’s own messages, so the verbosity controls required by pt-l6yb/ralph-logging-spec are not actually filtering output.

## Critical (must fix)
- None

## Major (should fix)
- `tf_cli/ralph_new.py:197-218, 849-994` – The resolved `LogLevel` and appended workflow flag are never consulted when printing dry-run notices, `pi -p…` invocations, completion/loop-status lines, or warnings, so `tf ralph run/start` always floods stdout/stderr with the same messages regardless of whether `--quiet`, `--verbose`, or `RALPH_QUIET/RALPH_VERBOSE` are set. Section 5.1 of `pt-l6yb/ralph-logging-spec.md` says verbosity modes must gate which lifecycle events and additional diagnostics are shown; because the new flags only pass through to the workflow command and never gate the CLI’s own prints, the spec’s requirement that verbosity filters messages is not met.

## Minor (nice to fix)
- None

## Warnings (follow-up ticket)
- None

## Suggestions (follow-up ticket)
- None

## Positive Notes
- CLI help now advertises `--verbose`, `--debug`, and `--quiet` plus the relevant `RALPH_*` environment variables, so the documented interfaces from pt-l6yb §5 are exposed and easy to discover.
- Environment variables, CLI flags, and `logLevel` in `.tf/ralph/config.json` are resolved in the documented priority order, so config overrides and defaults work as expected.

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 0
- Warnings: 0
- Suggestions: 0

## Spec Coverage
- Spec/plan sources consulted: docs/ralph-logging.md, .tf/knowledge/tickets/pt-l6yb/ralph-logging-spec.md
- Missing specs: none
