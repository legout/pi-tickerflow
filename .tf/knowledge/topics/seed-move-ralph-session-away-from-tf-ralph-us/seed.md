# Seed: Move Ralph session storage away from .tf/ralph (use Pi standard dir)

## Vision

Ralph currently writes session artifacts under `.tf/ralph` (e.g., `.tf/ralph/sessions/<ticket>.jsonl`). This couples Ralph's runtime files to the project directory and diverges from Pi's standard session storage expectations.

## Core Concept

Change `tf ralph` session storage to use Pi's standard session directory by default (while keeping backward compatibility / migration where needed).

## Key Features

1. **New default session dir** aligned with Pi conventions (configurable).
2. **Backward compatibility**: existing `.tf/ralph/sessions` artifacts continue to work or are migrated.
3. **Clear UX**: `tf ralph --help` documents where sessions/logs are written.

## Open Questions

- What is Pi's canonical session directory on this system? (e.g., `~/.pi/sessions`, `~/.pi/agent/sessions`, or passed via `pi --session`?)
- Should we support per-project override (keep `.tf/ralph/sessions`) while defaulting to global?
- Should we migrate existing files automatically or only on demand?
