# Review: pt-tpwl

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf_cli/ralph.py:1015-1020` - Race condition: The file is read and written in separate operations without file locking. If two ralph processes complete simultaneously, one update could be lost. Consider using file locking (e.g., `filelock` library or atomic write pattern with temp file + rename).
- `tf_cli/ralph.py:1015-1019` - Missing error handling: If `agents_path.read_text()` or `agents_path.write_text()` fails (permissions, disk full), the exception propagates and may leave progress.md in an inconsistent state. Consider wrapping in try/except and logging the error.
- `tf_cli/ralph.py:1012` - Template doesn't end with a newline before the first lesson header is appended, resulting in `## Gotchas\n## Lesson from...` instead of `## Gotchas\n\n## Lesson from...`. The header includes a leading `\n` but the template ends without one, which is slightly inconsistent formatting.

## Warnings (follow-up ticket)
- `tf_cli/ralph.py:1008-1020` - No maximum file size check for AGENTS.md. Over time, this file could grow unbounded. Consider adding a rotation/truncation mechanism when file exceeds a threshold (e.g., config `lessonsMaxCount` exists but isn't enforced here).

## Suggestions (follow-up ticket)
- `tf_cli/ralph.py:1008-1020` - Consider appending lessons atomically using a file append mode instead of read-then-write. This would be more efficient for large files and reduce race condition window.
- `tf_cli/ralph.py:1012` - The template could include a brief comment explaining the file's purpose for users who open it directly.
- `tf_cli/ralph.py:1029` - Consider adding error handling for file I/O operations (read/write) when creating/appending to AGENTS.md. While unlikely, disk permission issues or concurrent writes could cause silent failures.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 3
- Warnings: 1
- Suggestions: 3

## Spec Coverage
✅ Acceptance criterion met: When a ticket close-summary contains a "Lessons Learned" section and AGENTS.md doesn't exist, the file is created
✅ Acceptance criterion met: New file starts with the exact minimal template specified in the spec
✅ Acceptance criterion met: Lesson is appended under header `## Lesson from <ticket> (<timestamp>)`
✅ Acceptance criterion met: If no lesson block exists, AGENTS.md is not created or modified
✅ Constraint met: Minimal change with no new dependencies
✅ Constraint met: UTF-8 encoding used consistently with codebase

## Reviewers
- reviewer-general
- reviewer-spec-audit
