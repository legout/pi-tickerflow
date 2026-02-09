# Constraints

- Keep output stable in TTY and safe in non-TTY (no control characters in non-TTY).
- Avoid adding per-iteration overhead beyond cheap time formatting.
- Prefer minimal configuration surface (MVP can hardcode a sensible timestamp format).
