# Assumptions

- Primary use case is local development (localhost access)
- Single-user access for MVP (no concurrent session handling needed initially)
- Existing ticket data sources (`tk` CLI, knowledge base files) remain unchanged
- Web UI will reuse existing business logic from `tf_cli/ui.py`
- Browser support: modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- Network: localhost binding by default, configurable host/port
- Document viewing: inline markdown rendering replaces external pager (`less`, `vim`)
- Real-time updates: manual refresh acceptable for MVP, auto-refresh optional
- Security: basic localhost-only access sufficient for MVP, auth optional
