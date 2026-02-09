# Constraints

- Keep MVP small: browsing + search + open details first.
- Must not corrupt terminal state on crash; ensure clean exit.
- Prefer read-only MVP (avoid risky ticket mutations) unless clearly safe.
- Performance: indexing/search should be fast for ~100s of tickets.
- Should work without network access.
