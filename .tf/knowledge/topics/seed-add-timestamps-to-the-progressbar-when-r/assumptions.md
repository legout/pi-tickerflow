# Assumptions

- The progress display is centralized (e.g., `ProgressDisplay` in `tf_cli/ralph.py`) and can be updated without touching the core loop logic too much.
- Adding a timestamp prefix won’t break downstream consumers (but we should keep it conservative and consistent).
- We can determine “current time” without expensive calls (use `datetime.now()` / `time.time()`).
