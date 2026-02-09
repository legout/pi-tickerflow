# Implementation: pt-7t1n

## Summary
Built two proof-of-concepts for serving tf UI as a web application:
1. **textual-web POC** - Serves existing TUI in browser via WebSocket
2. **FastAPI+HTMX POC** - Web-native kanban board with server-rendered updates

## Files Changed
- `.tf/knowledge/tickets/pt-7t1n/poc/textual-web/serve.toml` - textual-web configuration
- `.tf/knowledge/tickets/pt-7t1n/poc/textual-web/README.md` - POC documentation
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/web_app.py` - FastAPI application
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/templates/base.html` - Base layout
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/templates/index.html` - Kanban board
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/templates/_board.html` - Board fragment
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/templates/ticket.html` - Ticket detail
- `.tf/knowledge/tickets/pt-7t1n/poc/fastapi-htmx/README.md` - POC documentation

## Key Decisions
1. Kept POCs minimal but functional - kanban board is minimum viable feature
2. Used existing ticket loading infrastructure (`TicketLoader`, `BoardClassifier`)
3. HTMX chosen over React/Vue for simplicity and server-rendered approach
4. Both POCs are standalone and don't modify existing tf_cli code

## Tests Run
- Syntax validation: `python -m py_compile web_app.py` - PASSED
- No existing tests affected (POCs are in knowledge directory)

## Verification
1. textual-web POC: Run `textual-web --config serve.toml` from textual-web directory
2. FastAPI POC: Run `python web_app.py` from fastapi-htmx directory, open http://127.0.0.1:8080
