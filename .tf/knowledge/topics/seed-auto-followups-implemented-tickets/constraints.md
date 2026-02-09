# Constraints

- **No duplicate follow-up tickets**: re-running the command must not create duplicates.
- **Safety first**: prefer dry-run / confirmation when operating on many tickets.
- **Performance**: scanning should be fast enough for ~100s of tickets.
- **Artifact consistency**: `followups.md` should be written even when no follow-ups were created (record “none needed” / “skipped”).
- **Minimal coupling**: avoid hard-coding assumptions that break if knowledge base layout evolves; use `workflow.knowledgeDir`.
