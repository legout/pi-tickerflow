# Review: pt-igly

## Overall Assessment
A clean, well-structured utility module that provides useful workflow status information. The code follows good Python practices with type hints, dataclasses, and clear function separation. However, it has one unused import and uses fragile string-based frontmatter parsing instead of leveraging the project's existing frontmatter utilities.

## Critical (must fix)
No issues found

## Major (should fix)
- `tf_cli/workflow_status.py:6` - **Unused import**: `subprocess` is imported but never used. Should be removed.
- `tf_cli/workflow_status.py:37-54` - **Fragile frontmatter parsing**: Uses simple string matching (`"status: open" in content`) instead of proper YAML frontmatter parsing. The project already has `tf_cli/ticket_loader.py` with robust frontmatter parsing (including regex patterns and YAML fallback). This approach will fail if:
  - Status appears in the body text
  - Frontmatter has different formatting (e.g., `status:"open"` without space)
  - Status value has different casing
  Consider using the existing `FRONTMATTER_PATTERN` from `ticket_loader.py` or importing a parsing function.

## Minor (nice to fix)
- `tf_cli/workflow_status.py:45-46` - **Inefficient file I/O**: Reads entire file content with `read_text()` when only the frontmatter (first ~20 lines) is needed. For large ticket files, this wastes memory. Use `read_text()` with size limit or line-by-line reading.
- `tf_cli/workflow_status.py:37-54` - **No tests**: Module has no unit tests. At minimum, add tests for `count_tickets_by_status()` with mock ticket files to verify status detection logic.
- `tf_cli/workflow_status.py:51` - **Silent exception swallowing**: `except Exception: continue` hides all errors including permission denied, malformed files, etc. Consider logging warnings at minimum.
- `tf_cli/workflow_status.py:42` - **"ready" logic incomplete**: The logic `if "deps: []" in content or "deps:" not in content` is fragile. If deps field exists but is on a different line than searched, this fails. Also doesn't handle multi-line yaml arrays.

## Warnings (follow-up ticket)
- Consider integrating this utility into the main CLI (`tf_cli/cli.py`) as a proper subcommand rather than a standalone script. A `tf status` command would be more discoverable than `python tf_cli/workflow_status.py`.

## Suggestions (follow-up ticket)
- Add real-time Ralph loop status detection (check if Ralph is currently running via pid file or process check) instead of just checking directory existence.
- Consider caching ticket counts for performance on large repositories.
- Add option to output as JSON for scripting/integration purposes.
- Show breakdown of tickets by component tag in addition to status counts.

## Positive Notes
- **Clean architecture**: Excellent separation between data models (`WorkflowStats`, `WorkflowStatus`), logic functions (`get_workflow_status`), and presentation (`print_status`).
- **Good type safety**: Consistent use of type hints throughout, proper use of `NamedTuple` for immutable stats and `dataclass` for the report.
- **Auto-discovery**: Smart project root detection by walking up directory tree looking for `.tf` directory.
- **Defensive programming**: Handles missing directories gracefully without crashing.
- **Zero external dependencies**: Uses only stdlib, making it lightweight and portable.

## Summary Statistics
- Critical: 0
- Major: 2
- Minor: 4
- Warnings: 1
- Suggestions: 4
