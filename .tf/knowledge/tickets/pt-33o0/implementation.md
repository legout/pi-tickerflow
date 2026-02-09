# Implementation: pt-33o0

## Summary
Extracted inline CSS from templates (`base.html` and `index.html`) into a dedicated stylesheet served by Sanic. This enables easier CSS iteration, eliminates duplication across pages, and sets up future theming capabilities.

## Files Changed
- `tf_cli/static/web-ui.css` (new) - Contains all custom CSS previously inline in templates:
  - CSS design tokens (colors, spacing, shadows)
  - App header and navigation styles
  - Priority badge styles (.priority-p0 through .priority-pnone)
  - Status indicator styles (.status-open, .status-closed, .status-blocked)
  - Kanban board styles (columns, ticket cards, responsive grid)
- `tf_cli/web_ui.py` - Added static file serving:
  - Added `_STATIC_DIR` variable pointing to `tf_cli/static/`
  - Added `app.static("/static", ...)` route for serving CSS files
- `tf_cli/templates/base.html` - Replaced inline `<style>` block with:
  - External stylesheet link: `<link rel="stylesheet" href="/static/web-ui.css">`
  - Minimal inline style block kept only for `extra_styles` Jinja block
- `tf_cli/templates/index.html` - Removed entire `extra_styles` block (CSS now in external file)

## Key Decisions
- Kept the `extra_styles` block in base.html for future page-specific styles, but made it empty by default
- Used Sanic's built-in `app.static()` for robust static file serving
- Used `str(_STATIC_DIR)` to ensure Path object is converted to string for Sanic compatibility
- Maintained CSS variable naming and structure exactly as before to ensure no visual regression

## Tests Run
- Python syntax check: `python -m py_compile tf_cli/web_ui.py` - OK
- Verified template syntax is valid Jinja2

## Verification
1. Run `tf web` to start the Sanic server
2. Navigate to http://127.0.0.1:8000/
3. Verify CSS loads correctly (check browser dev tools Network tab for `/static/web-ui.css`)
4. Verify kanban board displays correctly with all styling
5. Verify responsive breakpoints work (resize browser to <1024px and <640px)
