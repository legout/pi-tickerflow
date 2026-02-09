# Review: pt-whcy

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf_cli/ralph.py:682` - **Inconsistent warning formatting**: When `logger` is available, `warning_msg.strip()` removes the intentional leading newline, but when falling back to `print()`, the leading newline is preserved. This creates inconsistent output formatting between the two code paths. Consider using consistent formatting.

- `tf_cli/ralph.py:143` - **Thread-safety concern**: The global `_legacy_warning_emitted` flag is not thread-safe. In parallel mode, multiple workers could theoretically emit duplicate warnings before the flag is set. While this is a low-impact issue (duplicate warnings), using `threading.Lock()` would ensure the "warn once" guarantee is honored in all execution modes.

- `tf_cli/ralph.py:705` - Consider adding `path = path.resolve()` after `path.mkdir()` to ensure consistent absolute path handling. The function returns paths in different states (expanded but potentially relative vs absolute) depending on code path taken.

## Warnings (follow-up ticket)
- `tf_cli/ralph.py:499` - **Empty directory edge case**: The `legacy_exists` check requires the directory to have content (`any(legacy_path.iterdir())`). If a user created the legacy directory but hasn't run ralph yet, they won't receive the warning. Consider whether an empty legacy directory should also trigger the warning to prevent confusion when they later start using sessions.

## Suggestions (follow-up ticket)
- `tf_cli/ralph.py:519-521` - **Early return path skips new directory creation**: When `force_legacy` is set, the function returns early using the legacy path. This is correct behavior, but there's a subtle inconsistency: the new default directory (`~/.pi/agent/sessions`) is never created in this path, which might be surprising if the user later removes the env var. Consider documenting this behavior or ensuring both directories exist.

- `tf_cli/ralph.py:674-677` - Consider adding a debug log entry when `RALPH_FORCE_LEGACY_SESSIONS` is active to aid troubleshooting in support scenarios.

- `tf_cli/ralph.py:680` - The docstring could explicitly mention that `raw_config` should be the user config without defaults merged, to prevent future developers from passing the wrong config.

- Consider adding a `--migrate-sessions` CLI flag in a future ticket to provide an on-demand migration path for users who want to move sessions from the legacy location to the new default.

## Positive Notes
- ✅ The warning message is well-written with clear next steps and two escape hatches (env var and config)
- ✅ The `user_explicitly_set` detection correctly distinguishes between user configuration and defaults, preventing warning spam for users who have intentionally chosen a location
- ✅ The implementation correctly uses the global flag to ensure "warn once per run" behavior
- ✅ The `usage()` documentation includes the new environment variable
- ✅ The change is non-breaking and follows the principle of least surprise
- ✅ Good separation of concerns with `raw_config` parameter to detect explicit vs default settings
- ✅ Correctly detects legacy directory existence by checking both `is_dir()` and non-empty via `any(legacy_path.iterdir())`
- ✅ Two escape hatches implemented: `RALPH_FORCE_LEGACY_SESSIONS` env var and explicit `sessionDir` in config
- ✅ Clean separation of concerns: raw config detection logic is explicit and well-commented
- ✅ Logger integration follows existing codebase patterns with graceful fallback to stderr

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 3
- Warnings: 1
- Suggestions: 4

## Review Sources
- reviewer-general: Minor formatting inconsistency, thread-safety concern, empty directory edge case
- reviewer-spec-audit: Minor formatting issue, suggestion for migrate flag
- reviewer-second-opinion: Path resolution suggestion, suggestions for debug logging and docstring improvement
