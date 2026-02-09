# MVP Scope

## In Scope

- Remove `--session` forwarding from the Pi subcommand invocation in:
  - `tf ralph start`
  - `tf ralph run`
- Update help text/docs accordingly.
- Add a small test/smoke check verifying the constructed command line does not include `--session`.

## Out of Scope (for MVP)

- Any large refactor of session management beyond what is needed to preserve behavior.
- Redesign of Ralph persistence formats.
- New configuration surfaces unless required for parity.
