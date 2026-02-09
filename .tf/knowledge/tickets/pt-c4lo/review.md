# Review: pt-c4lo

## Critical (must fix)
- (none)

## Major (should fix)
- (none)

## Minor (nice to fix)

### XSS Risk with `| safe` Filter
**File**: `templates/ticket.html`
**Line**: Body rendering uses `{{ ticket.body_html | safe }}`

The markdown HTML is rendered with Jinja2's `| safe` filter without sanitization. While acceptable for a POC with trusted ticket sources, consider using a library like `bleach` or `nh3` to sanitize HTML in production to prevent XSS attacks from malicious markdown content.

### Markdown Instance Thread Safety
**File**: `web_app.py`
**Line**: Module-level `md = markdown.Markdown(...)` with `md.reset()` per request

The markdown converter is instantiated at module level but reset/used per request. In high-concurrency scenarios with Sanic's async handlers, this could cause race conditions. Consider creating a new `Markdown()` instance per request or using a thread-local/pool pattern.

**Suggested fix**:
```python
# Instead of module-level instance:
md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])

# Create per-request:
md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
body_html = md.convert(ticket.body) if ticket.body else ""
```

## Warnings (follow-up ticket)

### External Link Placeholder
**File**: `templates/ticket.html`
The "Open in tk web" link points to `/ticket/{id}/web` which doesn't exist. This is acceptable as a placeholder, but should be implemented or removed before production.

## Suggestions (follow-up ticket)

### Add Code Syntax Highlighting
Consider adding a code highlighting library (like highlight.js) to the base template for better code block rendering.

### Add Updated Timestamp
The template shows `created` but many tickets also have an `updated` field. Displaying both would be useful.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 2
- Warnings: 1
- Suggestions: 2

## Review Notes

The implementation successfully meets all acceptance criteria:
- Ticket metadata (ID, title, status, priority) is displayed
- Markdown is rendered server-side with proper extensions
- Tags and external refs are shown
- Created timestamp is displayed
- Back button uses correct Datastar navigation `@get('/board')`
- External link placeholder is present

The code follows existing patterns in the codebase and integrates well with the Sanic+Datastar architecture.
