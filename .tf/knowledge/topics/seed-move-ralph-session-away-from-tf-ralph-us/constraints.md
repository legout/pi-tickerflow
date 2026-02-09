# Constraints

- Must not break existing `tf ralph` workflows that rely on `.tf/ralph/sessions`.
- Must remain configurable via config/env/flags.
- Must work in offline environments.
- Prefer minimal changes to existing session semantics (per-ticket vs loop sessions).
