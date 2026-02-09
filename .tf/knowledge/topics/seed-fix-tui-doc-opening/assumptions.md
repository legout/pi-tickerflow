# Assumptions

- The fix should maintain backward compatibility with existing document paths
- Users have `$PAGER` or `$EDITOR` environment variables set
- The TUI is running in a proper terminal (TTY) that supports suspend/resume
- Textual framework version supports `app.suspend()` context manager
