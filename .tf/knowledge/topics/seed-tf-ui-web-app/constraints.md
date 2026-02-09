# Constraints

- Must not break existing terminal TUI (`tf ui` without --web flag must still work)
- Must not require changes to ticket storage format or `tk` CLI
- Must work on standard development machines (no GPU or special hardware)
- Web dependencies should be minimal (avoid heavy frontend frameworks if possible)
- Port binding must be configurable to avoid conflicts
- Must handle graceful degradation if JavaScript is disabled (HTMX approach)
- File system access limited to knowledge base directory (security sandbox)
- No database required (continue using file-based storage)
