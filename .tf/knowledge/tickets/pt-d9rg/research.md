# Research: pt-d9rg

## Status
Research enabled. Minimal research performed - context is clear from ticket and Textual docs.

## Context Reviewed
- `tk show pt-d9rg` - Ticket requirements
- Textual documentation on `app.suspend()` context manager
- Current `_open_doc` implementation in `tf_cli/ui.py` (lines 588-634)

## Key Findings

### Textual's `suspend()` Context Manager
- Added in Textual v0.48.0
- Temporarily suspends the TUI app to allow external terminal programs
- Works by stopping application mode (exits raw/cooked mode), executes code, then restarts
- Syntax: `with self.app.suspend():`

### Current Implementation Location
- File: `tf_cli/ui.py`
- Method: `_open_doc()` (around line 588)
- Currently calls `os.system(cmd)` directly without suspending

## Implementation Approach
Wrap the `os.system(cmd)` call with `with self.app.suspend():` context manager to ensure terminal is in normal mode before launching pagers/editors.

## Sources
- https://textual.textualize.io/guide/app/#suspending-the-app
- https://textual.textualize.io/api/app/
