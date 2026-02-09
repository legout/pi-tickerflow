# Seed: Remove `--session` parameter from pi invocation in `tf ralph start/run`

## Vision

Using Ralph should not require users to understand (or manually pass through) Pi session wiring.
`tf ralph start` and `tf ralph run` should “just work” with session state managed by ticketflow itself.

## Core Concept

Update the Ralph CLI commands so that they no longer pass a `--session <...>` argument to the underlying `pi` subcommand.
Instead, session selection/creation should be handled internally (or via default behavior), keeping the same functional outcomes.

## Key Features

1. `tf ralph start` no longer includes `--session ...` when calling `pi ...`.
2. `tf ralph run` no longer includes `--session ...` when calling `pi ...`.
3. Clear behavior definition for how sessions are chosen/created without `--session`.
4. Documentation updates and a small regression test or CLI smoke test.

## Open Questions

- Why was `--session` being passed previously (what behavior does it enforce)?
- Does removing `--session` change where artifacts/logs are written or how multi-run isolation works?
- Should we keep backward compatibility (e.g., still accept a `--session` flag on `tf ralph ...` even if it’s not forwarded to `pi`)?
- Are there edge cases around concurrent runs or parallel worktrees?
