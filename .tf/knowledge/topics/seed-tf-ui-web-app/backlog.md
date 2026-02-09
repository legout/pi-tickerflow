# Backlog: seed-tf-ui-web-app

| ID | Title | Score | Est. Hours | Depends On | Links |
|----|-------|-------|------------|------------|-------|
| pt-7t1n | Spike: Evaluate textual-web vs FastAPI+HTMX for tf ui web | 0 | 1-2 | - | - |
| pt-sd01 | **DECISION**: Switch to Sanic+Datastar stack | 0 | 1 | pt-7t1n | Supersedes pt-aoq0 |
| pt-fo58 | Implement web server CLI command for tf ui (Sanic) | 3 | 1-2 | pt-sd01 | - |
| pt-1d6c | Implement kanban board view in web UI (Datastar) | 3 | 1-2 | pt-fo58 | - |
| pt-ba0n | Implement topic browser in web UI (Datastar) | 3 | 1-2 | pt-1d6c | - |
| pt-c4lo | Implement ticket detail view in web UI (Datastar) | 3 | 1-2 | pt-ba0n | - |
| pt-n2dw | Handle document viewing in web UI (Datastar) | 3 | 1-2 | pt-c4lo | - |

## Stack Decision

**Selected: Sanic + Datastar** (see pt-sd01)

- **Sanic**: Python async web framework, native async/await, lightweight
- **Datastar**: 11KB hypermedia framework, SSE-first, signals-based reactivity

## Closed/Duplicate Tickets

| ID | Reason | Consolidated Into |
|----|--------|-------------------|
| pt-aoq0 | Superseded by pt-sd01 | - |
| pt-1x64 | Duplicate | pt-fo58 |
| pt-znph | Duplicate | pt-1d6c |
| pt-pdha | Duplicate | pt-ba0n |
| pt-tpz9 | Duplicate | pt-c4lo |
| pt-p2dq | Duplicate | pt-n2dw |
