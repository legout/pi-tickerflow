# Review: pt-7t1n

## Overall Assessment
Well-executed spike that delivers both POCs with clear documentation and a reasoned recommendation. The FastAPI POC code is clean and functional. Minor improvements suggested for error handling and HTML escaping.

## Critical (must fix)
No critical issues found.

## Major (should fix)
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/web_app.py:132` - HTML escaping vulnerability: `ticket.body | replace('\n', '<br>') | safe` in template bypasses autoescaping. Use a proper markdown-to-HTML filter or sanitize input.
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/web_app.py:76-85` - No error handling if `get_board_data()` returns None - will cause 500 error instead of graceful degradation.

## Minor (nice to fix)
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/web_app.py:12-13` - Path manipulation with `parent.parent.parent...` is fragile. Consider using a more robust repo root detection (similar to `resolve_knowledge_dir()` in ui.py).
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/templates/ticket.html:67` - Very basic body formatting - markdown headers and lists won't render properly. Consider adding a simple markdown parser.
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/web_app.py:96-102` - Loading all tickets into memory then linear searching is O(n). Use a dictionary lookup or add `load_by_id()` to TicketLoader.

## Warnings (follow-up ticket)
- No tests included for the FastAPI POC. Consider adding basic smoke tests.
- No requirements.txt or dependency pinning for POC dependencies (fastapi, uvicorn, jinja2).
- Static type checking would benefit the FastAPI routes (many `Any` types inferred).

## Suggestions (follow-up ticket)
- Add Server-Sent Events (SSE) endpoint for real-time ticket updates.
- Consider adding a simple caching layer for `get_board_data()` since ticket data changes infrequently.
- Add OpenAPI schema generation for API documentation.

## Positive Notes
- Excellent research documentation with clear sources and citations.
- Well-structured comparison document that objectively evaluates both approaches.
- POCs are appropriately scoped - minimal but functional.
- FastAPI POC correctly reuses existing `TicketLoader` and `BoardClassifier` infrastructure.
- Good separation of concerns with HTMX fragments (`_board.html`).
- Responsive CSS design works on mobile devices.
- Clear recommendation with justified rationale.

## Summary Statistics
- Critical: 0
- Major: 2
- Minor: 3
- Warnings: 3
- Suggestions: 3
