# seed-remove-session-param-from-ralph

Simplify the Ralph workflow CLI by removing the explicit `--session` parameter from the `pi` subcommand invocation inside `tf ralph start` and `tf ralph run`.

The goal is to reduce cognitive load and make session management implicit/automatic, while keeping the same behavior (session isolation, resumability, and logs).

## Keywords

- ralph
- tf
- cli
- session-management
- pi-subcommand
- ergonomics
