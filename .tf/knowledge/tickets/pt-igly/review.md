# Review: pt-igly

## Critical (must fix)
- `tf_cli/workflow_status.py:59` - **Wrong tickets directory path**: Uses `tf_dir / "tickets"` but tickets are stored in `.tickets/` at project root per `ticket_loader.py:105`. This causes utility to always report 0 tickets. Fix: Use `project_root / ".tickets"` or leverage `TicketLoader`.

## Major (should fix)
- `tf_cli/workflow_status.py:6` - **Unused import**: `subprocess` is imported but never used. Remove it.
- `tf_cli/workflow_status.py:37-54` - **Fragile frontmatter parsing**: Uses substring matching (`"status: open" in content`) which matches body text, not just frontmatter. Also doesn't handle different YAML formats. Should use existing `FRONTMATTER_PATTERN` from `ticket_loader.py` or call `TicketLoader` directly.
- `tf_cli/workflow_status.py:47-49` - **Incorrect "ready" logic**: Treats missing `deps:` as ready, but "ready" semantically means "unblocked" (dependencies satisfied), not "no dependencies". Also misrepresents workflow state.

## Minor (nice to fix)
- `tf_cli/workflow_status.py:45-46` - **Inefficient I/O**: Reads entire file with `read_text()` when only frontmatter (~20 lines) is needed.
- `tf_cli/workflow_status.py:37-54` - **No tests**: Module lacks unit tests for `count_tickets_by_status()` logic.
- `tf_cli/workflow_status.py:51` - **Silent errors**: `except Exception: continue` hides permission denied, malformed files, etc. Consider logging.
- `tf_cli/workflow_status.py:67-71` - **Inconsistent root detection**: Uses while-loop pattern; codebase convention uses `for parent in [cwd, *cwd.parents]` per `ticket_loader.py:103`.
- `tf_cli/workflow_status.py:15-24` - **Over-engineered structures**: NamedTuple + dataclass adds complexity; simple dataclass or dict would suffice.

## Warnings (follow-up ticket)
- Consider integrating as `tf status` subcommand in main CLI for discoverability.
- Duplication of ticket loading logic creates maintenance burden when format changes. Refactor to use `TicketLoader`.

## Suggestions (follow-up ticket)
- Add CLI arguments (`--json`, `--watch`, `--component`, `--tag` filters).
- Add real-time Ralph loop status detection (pid file check).
- Consider caching ticket counts for performance.

## Positive Notes
- Clean separation between data gathering and presentation.
- Good use of type hints throughout.
- Self-contained with no external dependencies (stdlib only).
- Auto-discovers project root by finding `.tf` directory.
- Defensive programming: handles missing directories gracefully.

## Summary Statistics
- Critical: 1
- Major: 3
- Minor: 5
- Warnings: 2
- Suggestions: 3

## Review Sources
- reviewer-general: Found unused import, fragile parsing, inefficient I/O, missing tests
- reviewer-spec-audit: Confirmed fragile parsing, noted spec is minimal (demo ticket)
- reviewer-second-opinion: Found critical path bug, incorrect ready logic, pattern inconsistency
