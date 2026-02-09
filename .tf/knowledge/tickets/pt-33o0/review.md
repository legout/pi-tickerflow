# Review: pt-33o0

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf_cli/web_ui.py:27` - No error handling if static directory doesn't exist at startup. If `tf_cli/static/` is deleted, Sanic will return 404s for CSS requests, potentially causing confusion. Consider adding a check like:
  ```python
  if not _STATIC_DIR.exists():
      print(f"Warning: Static directory does not exist: {_STATIC_DIR}", file=sys.stderr)
  ```
- `tf_cli/templates/base.html:16-18` - Empty `<style>` tag is always rendered even when `extra_styles` block is empty. Consider conditionally including or adding explanatory comment.
- No cache-busting mechanism for CSS file. The CSS is served as `/static/web-ui.css` without versioning or content hash. In production, users may see stale CSS after updates.
- `tf_cli/static/web-ui.css:69-74` - Priority badge classes use `!important`. While justified to override conflicting rules, consider using more specific selectors if possible.
- `tf_cli/templates/ticket.html:26-28` - Page-specific styles duplicate color values that match design tokens. Could reference CSS custom properties from `web-ui.css` instead.

## Warnings (follow-up ticket)
- Consider adding CSS minification for production deployment to reduce payload size
- Consider adding CSP header configuration for static files to enhance security
- Consider adding automatic cache-control headers for static assets (e.g., `max-age=86400` for CSS)
- `tf_cli/static/web-ui.css:4-37` - Consider adding more semantic color tokens for status colors and topic type colors to support theming
- Consider setting up CSS linting configuration (e.g., Stylelint) to catch issues and ensure consistent patterns

## Suggestions (follow-up ticket)
- Consider splitting the CSS into multiple files (e.g., `base.css`, `kanban.css`, `ticket.css`) for better organization as the codebase grows
- Consider adding a CSS preprocessor (like Sass or PostCSS) if the stylesheets become complex
- Consider adding CSS source maps in development mode for easier debugging
- Consider adding automated tests to verify CSS loads correctly and styles are applied (e.g., using Playwright)
- For larger codebases, consider using a CSS framework's breakpoint system or establishing a formal breakpoint design token system

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 5
- Warnings: 5
- Suggestions: 5

## Reviewers
- reviewer-general (completed)
- reviewer-second-opinion (completed)
- reviewer-spec-audit (skipped/not available)
