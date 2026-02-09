# Assumptions

- Implemented tickets are represented in `.tf/knowledge/tickets/{ticket-id}/`.
- Review feedback is available in `review.md` (or can be located deterministically).
- `/tf-followups` exists and already encapsulates the parsing + `tk create` behavior (or can be refactored to expose it as a reusable function).
- The `tk` CLI is available in the environment where the scan command runs.
