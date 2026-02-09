# Seed: Serve tf ui as a web application

## Vision
Run `tf ui --web` (or a separate `tf web` command) to serve the Ticketflow TUI as a web application accessible via browser. This enables remote access, better integration with cloud development environments, and eliminates terminal compatibility issues.

## Core Concept
Extend the existing Textual-based TUI to support web serving mode, or create a web-native interface that provides the same functionality (Kanban board, topic browser, ticket detail) through a browser.

## Key Features

### Option A: Textual Web (textual-web)
- Use Textual's built-in `textual-web` export to serve the existing TUI in a browser
- Minimal code changes required
- Terminal-like experience in browser
- Single-user, local access by default

### Option B: FastAPI + HTMX Web Interface
- Full web-native implementation with FastAPI backend
- HTMX for dynamic, server-rendered UI updates
- Better accessibility and mobile support
- Easier to extend with multi-user features later

### Option C: Hybrid Approach
- Start with textual-web for rapid deployment
- Gradually build FastAPI+HTMX alternative for advanced features

## Technical Considerations

### Authentication & Security
- Local development: no auth needed (localhost only)
- Remote/team access: simple token-based auth or OAuth
- CORS configuration for browser access

### State Management
- Web mode requires server-side state or session storage
- Ticket data still sourced from `tk` CLI and knowledge base
- Real-time updates via WebSocket or Server-Sent Events

### URL Routing
- `/` - Kanban board (default view)
- `/topics` - Topic browser
- `/topics/<id>` - Topic detail
- `/tickets/<id>` - Ticket detail view

## Open Questions
- Which approach (A, B, or C) balances speed and long-term value?
- Should web mode support multiple concurrent users?
- How to handle the external pager/editor (`less`, `vim`) in web mode?
- Should we support file uploads for document editing?
- What's the deployment target (local dev, self-hosted, cloud)?

## References
- Textual Web: https://textual.textualize.io/blog/2023/09/06/textual-web/
- HTMX: https://htmx.org/
- FastAPI: https://fastapi.tiangolo.com/
