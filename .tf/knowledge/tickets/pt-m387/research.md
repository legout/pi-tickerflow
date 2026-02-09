# Research: pt-m387

## Status
Research enabled. Using existing spike knowledge from `spike-datastar-py-sanic-datastar-tf-web-ui`.

## Context Reviewed

### Ticket Requirements
- Add `GET /api/stream` SSE endpoint using datastar-py's Sanic helpers
- Stream `patch_elements` events periodically for live board updates
- Client subscribes on page load via `data-init="@get('/api/stream')"`
- Handle client disconnects without crashing
- Keep update frequency conservative (1-2s)

### Existing Knowledge

**From spike: spike-datastar-py-sanic-datastar-tf-web-ui**

The spike documents the correct pattern for Sanic SSE streaming:

```python
import asyncio
from datastar_py.sanic import datastar_respond, ServerSentEventGenerator as SSE

@app.get("/api/stream")
async def stream(request):
    resp = await datastar_respond(request)
    while True:
        board_html = env.get_template("_board.html").render(columns=columns)
        await resp.send(SSE.patch_elements(board_html, selector="#board"))
        await asyncio.sleep(2)
```

Key implementation details:
1. Use `datastar_respond(request)` to get a response object for streaming
2. Use `await resp.send()` in a loop to send SSE events
3. `ServerSentEventGenerator.patch_elements()` creates properly formatted SSE events
4. Sanic requires slightly different pattern than ASGI frameworks
5. datastar-py sets `X-Accel-Buffering: no` by default for SSE headers

### Dependency Status
- datastar-py>=0.7.0,<0.8.0 is in pyproject.toml
- Available in .venv (verified)
- Pinned to match Datastar JS v1.0.0-RC.7

### Current Web UI Structure
- Main file: `tf_cli/web_ui.py`
- Templates in: `tf_cli/templates/`
- Board fragment: `_board.html` (includes #board and #board-stats)
- Base template: `base.html` with Datastar CDN

### Related Tickets
- pt-4y31 [closed]: Already implemented DatastarResponse for /api/refresh in examples POC
- pt-za25 [open]: Server-side search/filter (depends on this ticket)

## Implementation Plan

1. Add imports for `datastar_respond` and `ServerSentEventGenerator` to web_ui.py
2. Create `/api/stream` endpoint that:
   - Calls `datastar_respond(request)` to get streaming response
   - Loops with `asyncio.sleep(2)` for conservative updates
   - Sends `patch_elements` events to update #board
   - Handles client disconnects via try/except on send
3. Add `data-init="@get('/api/stream')"` to the board container in index.html

## Sources
- Spike: `.tf/knowledge/topics/spike-datastar-py-sanic-datastar-tf-web-ui/spike.md`
- datastar-py Sanic module: GitHub starfederation/datastar-python
- Current web UI: `tf_cli/web_ui.py`
