# Assumptions

- `tk ralph` can estimate “total work” at the start (e.g., number of ready tickets, or planned work items).
- The CLI can detect whether stdout/stderr is a TTY and choose an appropriate rendering strategy.
- Users want a low-noise mode for interactive use, but still need full logs occasionally.
