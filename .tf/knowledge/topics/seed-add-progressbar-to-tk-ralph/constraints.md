# Constraints

- Must be **optional** and not change default behavior unless a flag is provided.
- Must not corrupt output when stdout is not a TTY (CI logs, piping to file).
- Error messages and final summaries must remain visible even in “quiet/progress” mode.
- Avoid heavy dependencies if possible (prefer lightweight progress rendering).
- “Suppress Pi output” must not hide critical failures; ensure failures still surface.
