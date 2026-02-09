# Implementation: pt-fo58

## Summary
Implemented web server CLI command for `tf ui` using Sanic + Datastar stack.

## Files Changed
- `pyproject.toml` - Added `sanic>=25.3.0` dependency
- `tf_cli/ui.py` - Added `--web`, `--host`, `--port` CLI arguments; imports and calls `run_web_server()` from web_ui.py
- `tf_cli/web_ui.py` - New Sanic web application with kanban board and ticket detail views
- `tf_cli/templates/base.html` - Base template with Datastar CDN v1.0.0-RC.7
- `tf_cli/templates/index.html` - Kanban board main page
- `tf_cli/templates/_board.html` - Partial template for Datastar morphing
- `tf_cli/templates/ticket.html` - Individual ticket detail page

## Key Decisions
- Used Sanic's built-in `app.run()` with `single_process=True` for simplicity
- Jinja2 templates loaded via FileSystemLoader from `tf_cli/templates/`
- Datastar CDN pinned to v1.0.0-RC.7 to avoid breaking changes
- Error handling catches OSError errno 98/48 for port conflicts
- Default host 127.0.0.1 for security (localhost only)

## Tests Run
- Verified `tf ui` (without --web) still launches terminal TUI
- Verified `tf ui --web` starts Sanic server on port 8000
- Verified `tf ui --web --port 9000` binds to custom port
- Verified port conflict error handling: `Error: Port 8000 is already in use`
- Verified graceful shutdown with Ctrl+C

## Verification
```bash
# Terminal TUI (unchanged)
tf ui

# Web UI
tf ui --web
tf ui --web --host 0.0.0.0 --port 8080
```
