# Implementation: pt-m387

## Summary
Added `/api/stream` SSE endpoint to `tf_cli/web_ui.py` for live board updates using datastar-py's Sanic streaming helpers. The endpoint streams `patch_elements` events every 2 seconds to update the kanban board without requiring manual refresh.

## Files Changed

### `tf_cli/web_ui.py`
- Added imports for `datastar_respond` and `ServerSentEventGenerator` from datastar-py
- Added graceful fallback when datastar-py is not available (`DATASTAR_AVAILABLE` flag)
- Implemented `/api/stream` endpoint with:
  - SSE streaming using `datastar_respond(request)` pattern
  - 2-second update interval (conservative, as specified)
  - Proper client disconnect handling via `asyncio.CancelledError`
  - Error handling to prevent server crashes
  - `patch_elements` events targeting `#board` selector

### `tf_cli/templates/index.html`
- Added wrapper div with `data-init="@get('/api/stream')"` to subscribe to SSE stream on page load
- This triggers the stream connection when the kanban board page loads

## Key Decisions

1. **Graceful degradation**: Added `DATASTAR_AVAILABLE` flag so the code works even if datastar-py is not installed (returns 503 error)

2. **Error handling**: Wrapped the streaming loop in try/except to handle:
   - `asyncio.CancelledError`: Client disconnected - clean exit without error
   - General exceptions: Logged to stderr, attempt to send error event if connection open

3. **Update frequency**: Used 2-second interval as specified in constraints to avoid busy loops

4. **Selector choice**: Used `#board` as the patch target since `_board.html` renders the complete board fragment including stats and columns

## Tests Run
- Module import test: `from tf_cli.web_ui import app` - SUCCESS
- Import verification: DATASTAR_AVAILABLE=True, all imports resolved correctly

## Verification
To verify the implementation:

1. Start the web server: `tf web` or `python -m tf_cli.web_ui`
2. Open http://127.0.0.1:8000/ in a browser
3. Open browser DevTools → Network tab → Filter by "stream"
4. You should see a request to `/api/stream` with type "eventsource"
5. The connection should stay open and show periodic updates every 2 seconds
6. Check that the board updates automatically when tickets change
7. Verify that disconnecting (closing the tab) doesn't crash the server
