# Review (Second Opinion): pt-igly

## Overall Assessment
The workflow status utility is a useful addition for quick project overview, but contains several correctness and maintainability issues. Most critically, it looks for tickets in the wrong directory, making it non-functional for the intended use case. The implementation also bypasses established codebase patterns for ticket parsing.

## Critical (must fix)
- `tf_cli/workflow_status.py:59` - **Wrong tickets directory path**: The code uses `tf_dir / "tickets"` but tickets are stored in `.tickets/` at the project root (see `ticket_loader.py:105`). This causes the utility to always report 0 tickets. Fix: Use `project_root / ".tickets"` or leverage `TicketLoader._resolve_tickets_dir()`.

## Major (should fix)
- `tf_cli/workflow_status.py:45-52` - **Fragile frontmatter parsing**: Uses simple substring matching (`"status: open" in content`) which can match body text, not just frontmatter. Should use `FRONTMATTER_PATTERN` from `ticket_loader.py` or call `TicketLoader` directly. This is a maintenance risk as the format evolves.
- `tf_cli/workflow_status.py:47-49` - **Incorrect "ready" logic**: A ticket with `deps: []` is counted as ready, but the code also treats missing `deps:` as ready. More importantly, "ready" semantically means "unblocked" (dependencies satisfied), not "no dependencies". This misrepresents the workflow state.

## Minor (nice to fix)
- `tf_cli/workflow_status.py:5` - **Unused import**: `subprocess` is imported but never used. Remove to clean up dependencies.
- `tf_cli/workflow_status.py:67-71` - **Inconsistent root detection pattern**: Uses `while project_root != project_root.parent` loop, but codebase convention in `ticket_loader.py:103` uses `for parent in [cwd, *cwd.parents]` which is cleaner and more Pythonic.
- `tf_cli/workflow_status.py:15-24` - **Over-engineered data structures**: `WorkflowStats` as NamedTuple and `WorkflowStatus` as dataclass adds complexity without benefit. A simple dataclass or dict would suffice for a status display utility.

## Warnings (follow-up ticket)
- `tf_cli/workflow_status.py:1` - **Duplication of ticket loading logic**: The module reimplements ticket parsing that's already solved by `TicketLoader`. This creates maintenance burden when ticket format changes. Consider refactoring to use `TicketLoader` or extract shared parsing utilities.

## Suggestions (follow-up ticket)
- `tf_cli/workflow_status.py:1` - **Add CLI integration**: The module has `print_status()` but isn't integrated into the main CLI. Consider adding a `tf status` command that calls this utility.
- `tf_cli/workflow_status.py:1` - **Add filtering options**: Future enhancement could add `--component` or `--tag` filters to show status for specific subsets of tickets.

## Positive Notes
- Clean separation between data gathering (`get_workflow_status()`) and presentation (`print_status()`)
- Good use of type hints throughout
- Self-contained module with no external dependencies beyond stdlib (appropriate for a simple utility)
- Includes `__main__` guard for direct execution, useful for quick checks

## Summary Statistics
- Critical: 1
- Major: 2
- Minor: 3
- Warnings: 1
- Suggestions: 2
