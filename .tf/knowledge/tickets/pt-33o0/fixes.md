# Fixes: pt-33o0

## Issues Fixed

### Minor Issues Addressed

1. **Static directory error handling** (`tf_cli/web_ui.py`)
   - Added check to verify `_STATIC_DIR.exists()` at startup
   - Prints warning to stderr if static directory is missing
   - Helps diagnose 404 errors early rather than at request time

2. **Empty style tag documentation** (`tf_cli/templates/base.html`)
   - Added clearer comment explaining why the inline style block exists
   - Documents that page-specific styles can be added via `extra_styles` block
   - Clarifies that default styles come from external CSS file

## Issues Deferred

The following Minor issues were intentionally not fixed as they are acceptable trade-offs or out of scope:

- **No cache-busting mechanism** - Would require build pipeline changes, acceptable for current use case
- **Priority badges use `!important`** - Intentional design choice to ensure override capability
- **ticket.html duplicate color values** - Page-specific styles, not shared CSS (out of scope for this ticket)

## Verification

- Python syntax check passed
- Templates remain valid Jinja2 syntax
