# MVP Scope

## In Scope
1. **Spike**: Evaluate and select approach (textual-web vs FastAPI+HTMX)
2. **Web server command**: `tf ui --web` or `tf web` to start web server
3. **Kanban board view**: Display tickets in Ready/Blocked/In Progress/Closed columns
4. **Basic navigation**: Click tickets to see detail view
5. **Localhost-only**: Bind to 127.0.0.1 by default
6. **Manual refresh**: Button to refresh ticket data

## Out of Scope (for MVP)
- Authentication/authorization (localhost-only is sufficient)
- Real-time updates (WebSocket/SSE)
- Multi-user support
- Document editing in browser
- Mobile-responsive design (basic functionality only)
- Dark/light mode toggle
- Configuration file
- External hosting/deployment guides
