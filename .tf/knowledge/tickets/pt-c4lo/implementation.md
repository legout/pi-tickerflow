# Implementation: pt-c4lo

## Summary
Implemented ticket detail view in the web UI using Datastar with server-side markdown rendering and proper navigation.

## Files Changed

### 1. `examples/web-ui-poc/sanic-datastar/requirements.txt` (new file)
- Added dependencies: sanic>=23.0, jinja2>=3.0, markdown>=3.0

### 2. `examples/web-ui-poc/sanic-datastar/web_app.py`
- Added `import markdown` for server-side markdown rendering
- Created markdown converter instance with extensions: fenced_code, tables, toc
- Added `/board` route for Datastar navigation (returns same as `/`)
- Updated `/ticket/<ticket_id>` route to:
  - Render ticket body to HTML using markdown
  - Pass `body_html` to template for safe rendering

### 3. `examples/web-ui-poc/sanic-datastar/templates/ticket.html`
- Changed back button to use `data-on:click="@get('/board')"` per acceptance criteria
- Updated body display to use `{{ ticket.body_html | safe }}` for rendered markdown
- Added "Linked Tickets" section (was missing)
- Reordered sections: Linked Tickets before Dependencies
- Updated external link to point to `/ticket/{id}/web` for tk web integration

## Key Decisions

1. **Server-side markdown rendering**: Used Python `markdown` library to render markdown to HTML server-side, passing the HTML to the template with `| safe` filter. This keeps the client simple and avoids JavaScript markdown parsers.

2. **Datastar navigation**: Used `@get('/board')` for back navigation as specified. Added a `/board` route that renders the same content as `/` to support this.

3. **Markdown extensions**: Enabled `fenced_code`, `tables`, and `toc` extensions for rich markdown support.

4. **External link**: Used `/ticket/{id}/web` as the URL for "Open in tk web" - this is a placeholder for future tk web integration.

## Acceptance Criteria Status

- [x] Display ticket ID, title, status, priority
- [x] Render ticket description as formatted markdown (server-side)
- [x] Show ticket tags and external references
- [x] Display created timestamp
- [x] Add button/link to open ticket in external system (tk web)
- [x] Add back button to return to previous view using `data-on:click="@get('/board')"`

## Verification

To test the implementation:
1. Install dependencies: `pip install -r examples/web-ui-poc/sanic-datastar/requirements.txt`
2. Run the server: `python examples/web-ui-poc/sanic-datastar/web_app.py`
3. Navigate to http://127.0.0.1:8080/
4. Click any ticket to view the detail page
5. Verify markdown rendering, Datastar navigation, and all metadata display
