# Fixes: pt-c4lo

## Issues Fixed

### Minor: Markdown Instance Thread Safety
**Fixed in**: `web_app.py`

Changed from module-level Markdown instance to per-request instance creation for thread safety in async Sanic handlers.

**Before**:
```python
md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
# ... later ...
md.reset()
body_html = md.convert(ticket.body)
```

**After**:
```python
MD_EXTENSIONS = ["fenced_code", "tables", "toc"]
# ... later ...
md = markdown.Markdown(extensions=MD_EXTENSIONS)
body_html = md.convert(ticket.body)
```

## Issues Skipped

### Minor: XSS Risk with `| safe` Filter
**Reason**: This is a proof-of-concept for internal use with trusted ticket content. Adding HTML sanitization would require a new dependency (bleach/nh3). Marked for future enhancement if the POC moves to production.

## Verification
- Python syntax check passed
- Implementation maintains all acceptance criteria
- No behavioral changes, only improved thread safety
