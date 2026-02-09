# Success Metrics

- 100% of “implemented/closed” ticket directories in `.tf/knowledge/tickets/` have a `followups.md` artifact.
- Running the scan command is **idempotent** (second run produces 0 changes).
- Follow-up tickets created from reviews have:
  - Clear origin (ticket id + review path)
  - `tf,followup` tags
  - Concise descriptions (≤30 lines)
