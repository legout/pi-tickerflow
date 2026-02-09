# Spike: What is datastar-py and how to use it in the Sanic+Datastar Ticketflow web UI

## Summary

**datastar-py** is the official **Python SDK** for the Datastar hypermedia framework. It focuses on the server side of Datastar’s model: generating correctly-formatted **SSE (Server-Sent Events)** messages ("patch elements", "patch signals", "execute script"), providing **framework-specific response helpers** (including Sanic), and helpers to **read client signals** from requests. Source: PyPI + official repo. (See sources.)

Ticketflow already uses Datastar on the frontend (pinned to `v1.0.0-RC.7`) and currently returns **plain `text/html` fragments** from Sanic endpoints (e.g. `/api/refresh`). That’s valid because Datastar accepts both `text/html` and `text/event-stream`. However, adopting datastar-py becomes attractive when you need:

- **Multi-target updates** in one action (e.g. update board _and_ counts)
- **Real-time streaming** (SSE push) such as auto-refresh, background job progress, or live updates during Ralph runs
- Safer/typed generation of Datastar attributes and SSE events (less “stringly-typed” HTML + event formatting)

## Key Findings

1. **datastar-py provides Sanic helpers out of the box**
   - PyPI explicitly lists **Sanic** among supported frameworks and documents a Sanic-specific streaming pattern.
   - In the official repo, `datastar_py.sanic.DatastarResponse` is an `HTTPResponse` with default SSE headers, plus a `datastar_response` decorator that supports regular functions and generator / async-generator handlers.

2. **SSE event generation is standardized**
   - `ServerSentEventGenerator.patch_elements(...)` and `.patch_signals(...)` build properly-formatted SSE events (including `event: ...` and multiple `data:` lines), which is easy to get wrong by hand.

3. **Sanic needs a slightly different streaming pattern than ASGI frameworks**
   - The docs and examples show that for long-lived streams in Sanic you typically:
     - call `response = await datastar_respond(request)` (or `await request.respond(DatastarResponse())`)
     - then `await response.send(event)` in a loop
   - datastar-py’s Sanic module wraps these details.

4. **Ticketflow’s current Sanic+Datastar UI is “HTML fragment only”**
   - `/api/refresh` returns `_board.html` as plain HTML. This works well for a manual refresh button.
   - But it only refreshes `#board`; the counts shown above the board are rendered server-side on initial load and remain stale after refresh.

## Options Considered (for Ticketflow)

### Option A — Keep current approach (plain HTML fragments)

**How it works now**
- Templates use Datastar attributes like `data-on:click="@get('/api/refresh')"`
- Backend returns `text/html` fragments; Datastar morphs them into DOM based on element IDs.

**Pros**
- Minimal dependencies
- Simple mental model

**Cons**
- Harder to do multi-target updates in a single action (without returning larger fragments)
- If/when you add SSE streaming, you’ll have to handcraft event formatting and streaming semantics

### Option B — Adopt datastar-py just for “action responses”

Change endpoints like `/api/refresh` to return a `DatastarResponse(...)` containing one or more SSE events:
- patch the board HTML into `#board`
- patch counts into a `#board-stats` element

**Pros**
- Multi-target update in one action is straightforward
- Event formatting is handled by the SDK

**Cons**
- Adds a dependency (`datastar-py`) and some new concepts (events vs HTML fragments)

### Option C — Adopt datastar-py for streaming (SSE push)

Add an endpoint like `/api/stream` and start it on page load (e.g. `data-init="@get('/api/stream')"`). Stream `patch_elements` / `patch_signals` events periodically or in response to file changes.

**Pros**
- Enables “live” kanban updates and long-running progress UIs
- Cleanest implementation path for server push in Sanic

**Cons**
- Requires thinking about reconnects, polling frequency, and load (even locally)

## Recommendation

- **If you only need manual refresh**: keep the current `text/html` fragment approach for now.
- **If you want correct counts + multi-target updates** (board + counts) or plan to add SSE push soon: adopt **datastar-py**.

A pragmatic hybrid is to keep most endpoints returning HTML, and introduce datastar-py only for:
- `/api/refresh` (so you can patch multiple targets)
- `/api/stream` (server-push updates)

## How to Use datastar-py in Ticketflow’s Sanic+Datastar UI (concrete steps)

### 1) Add dependency

Add `datastar-py` to `pyproject.toml` dependencies.

### 2) Patch `/api/refresh` via SSE events (multi-target)

Change `tf_cli/web_ui.py` to use the Sanic helper module:

```python
from datastar_py.consts import ElementPatchMode
from datastar_py.sanic import DatastarResponse, ServerSentEventGenerator as SSE

@app.get("/api/refresh")
async def refresh_board(request):
    board_view = get_board_data()
    if not board_view:
        # Can return HTML or a DatastarResponse; keep it simple
        return response.html("<p class='error'>Error loading tickets</p>")

    # Render both board and counts (recommend adding ids in the template)
    board_html = env.get_template("_board.html").render(columns=columns)
    counts_html = env.get_template("_counts.html").render(counts=board_view.counts)

    return DatastarResponse([
        SSE.patch_elements(board_html, selector="#board", mode=ElementPatchMode.OUTER),
        SSE.patch_elements(counts_html, selector="#board-stats", mode=ElementPatchMode.OUTER),
    ])
```

This removes the “stale counts” problem without requiring a full page refresh.

### 3) Add a streaming endpoint for real-time updates

Add a stream endpoint and start it on load (e.g. on `<div id="board" data-init="@get('/api/stream')">`).

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

Later, replace the periodic sleep loop with “send only when tickets change” (file watcher) or “send when Ralph emits progress”.

### 4) Use `read_signals()` to implement filters/search

Datastar automatically sends the current signal state back on requests. With `read_signals(request)` you can implement server-side filtering (e.g. search string) without building a separate API.

### 5) (Optional) Use `attribute_generator` to avoid attribute typos

If you ever generate HTML in Python (not Jinja), datastar-py includes a typed `attribute_generator` to build `data-*` attributes with IDE completion.

## Risks & Unknowns

- **Version pinning**: Ticketflow currently pins Datastar JS to `v1.0.0-RC.7`. If you add datastar-py, pin that too and keep versions compatible.
- **SSE operational behavior**: if you stream in production, proxy buffering/timeouts and reconnect semantics matter. datastar-py sets `X-Accel-Buffering: no` by default in SSE headers for this reason.
- **Sanic response model**: streaming uses `request.respond()` + `response.send()` loops; make sure to handle disconnects and cancellation cleanly (datastar-py’s decorator helps).

## Next Steps

1. Decide whether you want **(A) manual refresh** only, or **(B/C) multi-target updates + SSE streaming**.
2. If B/C: implement a small migration:
   - add `datastar-py`
   - modify `/api/refresh` to return `DatastarResponse([...])`
   - add ids to the template for elements you want to patch (counts/stats)
3. Add a follow-up spike: “file watcher for `.tf/tickets/**` to trigger SSE patches” if you want real-time board updates.
