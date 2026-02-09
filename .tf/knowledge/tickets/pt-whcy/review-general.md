# Review: pt-whcy

## Overall Assessment
The implementation adds backward compatibility detection for legacy session directories with clear warning messages and escape hatches. The code is well-structured and follows existing patterns in the codebase. The logic correctly detects legacy sessions, emits warnings only when appropriate, and provides two documented escape hatches (env var and config setting).

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf_cli/ralph.py:537` - **Inconsistent warning formatting**: When `logger` is available, `warning_msg.strip()` removes the intentional leading newline, but when falling back to `print()`, the leading newline is preserved. This creates inconsistent output formatting between the two code paths. Consider using consistent formatting or removing the leading `\n` from the message template.

- `tf_cli/ralph.py:493` - **Thread-safety concern**: The global `_legacy_warning_emitted` flag is not thread-safe. In parallel mode, multiple workers could theoretically emit duplicate warnings before the flag is set. While this is a low-impact issue (duplicate warnings), using `threading.Lock()` would ensure the "warn once" guarantee is honored in all execution modes.

## Warnings (follow-up ticket)
- `tf_cli/ralph.py:499` - **Empty directory edge case**: The `legacy_exists` check requires the directory to have content (`any(legacy_path.iterdir())`). If a user created the legacy directory but hasn't run ralph yet, they won't receive the warning. Consider whether an empty legacy directory should also trigger the warning to prevent confusion when they later start using sessions.

## Suggestions (follow-up ticket)
- `tf_cli/ralph.py:499` - **Consider adding migration helper**: The warning message tells users to manually move files. A follow-up could add a `tf ralph migrate-sessions` command that automates this migration safely.

- `tf_cli/ralph.py:519-521` - **Early return path skips new directory creation**: When `force_legacy` is set, the function returns early using the legacy path. This is correct behavior, but there's a subtle inconsistency: the new default directory (`~/.pi/agent/sessions`) is never created in this path, which might be surprising if the user later removes the env var. Consider documenting this behavior or ensuring both directories exist.

## Positive Notes
- The warning message is well-written with clear next steps and two escape hatches (env var and config)
- The `user_explicitly_set` detection correctly distinguishes between user configuration and defaults, preventing warning spam for users who have intentionally chosen a location
- The implementation correctly uses the global flag to ensure "warn once per run" behavior
- The `usage()` documentation includes the new environment variable
- The change is non-breaking and follows the principle of least surprise
- Good separation of concerns with `raw_config` parameter to detect explicit vs default settings

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 2
- Warnings: 1
- Suggestions: 2
