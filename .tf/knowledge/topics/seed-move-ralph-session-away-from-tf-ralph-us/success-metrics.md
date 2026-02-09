# Success Metrics

- `tf ralph` writes sessions to the Pi standard directory by default.
- Users can still find session artifacts easily (printed paths / docs).
- Existing projects with `.tf/ralph/sessions` do not break.
- No sensitive data leaks into unexpected locations (paths are predictable and documented).
