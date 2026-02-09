# Success Metrics

- A user can run `tf ralph start` and `tf ralph run` successfully without any session-related flags.
- No regression in Ralph’s ability to resume/continue work across invocations (where applicable).
- No regression in artifact organization (ticket artifacts still land in the expected `.tf/knowledge/tickets/...` structure).
- Documentation reflects the new behavior and does not mention `--session` forwarding to `pi`.
