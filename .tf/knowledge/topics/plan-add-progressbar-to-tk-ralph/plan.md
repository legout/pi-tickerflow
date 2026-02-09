---
id: plan-add-progressbar-to-tk-ralph
status: approved
last_updated: 2026-02-08
---

# Plan: Add progress bar + quiet/Pi-output suppression to `tf ralph`

## Summary

Add an **optional** progress display to `tf ralph` so interactive runs show clear high-level progress (tickets done / total, current ticket) without scrolling through verbose output.

Because `tf ralph` executes the `/tf` workflow by running `pi` as a subprocess, progress mode must ensure the terminal output is not corrupted by concurrent `pi` output. Practically this means: in progress mode, **redirect `pi` output away from the terminal** (to a file and/or JSONL capture) and keep only progress + essential errors/summaries on screen.

This must remain **opt-in**: default behavior stays unchanged unless flags are provided.

## Inputs / Related Topics

- Root Seed: [seed-add-progressbar-to-tk-ralph](topics/seed-add-progressbar-to-tk-ralph/seed.md)
- Session: seed-add-progressbar-to-tk-ralph@2026-02-08T16-20-43Z
- Related Spikes:
  - [spike-python-cli-progressbar-tools](topics/spike-python-cli-progressbar-tools/spike.md)

## Requirements

### CLI Surface

- Add a CLI flag to enable a progress indicator for **both**:
  - `tf ralph run`
  - `tf ralph start`
- Proposed flags:
  - `--progress` (alias: `--progressbar`)
  - `--pi-output=inherit|file|discard` (default: `inherit`)
  - `--pi-output-file <path>` (optional override; default derived under `.tf/ralph/logs/`)

### Progress Semantics (MVP)

- Unit of progress is **per ticket** (not per tool call / per phase inside a ticket).
- Progress display should show at minimum:
  - tickets completed / total (best-effort total)
  - current ticket id (and title if cheaply available)
  - failures count
  - mode (serial/parallel)
- Progress should be rendered to **stderr** so stdout stays scriptable.
- Rendering rules:
  - If stderr is a TTY: single-line, in-place updates are allowed.
  - If not a TTY: progress rendering must degrade to plain text (no control characters).

### Pi Output Suppression

- `--progress` in a TTY **requires** that `pi` output is not inherited by the terminal.
  - Policy: when `--progress` is set and stderr is a TTY, **force `--pi-output=file`** unless user explicitly chose `--pi-output=discard`.
  - If user explicitly sets `--pi-output=inherit` together with `--progress` in TTY, print a warning and override to `file` (do not silently render a broken progress bar).
- When `--pi-output=file` is active:
  - redirect `pi` stdout+stderr to a log file (per ticket)
  - on failure, print a clear on-screen summary including log path (and optionally last N lines)
- Existing `--capture-json` remains supported and should be compatible:
  - `--capture-json` captures `pi --mode json` output to `.tf/ralph/logs/<ticket>.jsonl` (already implemented)
  - `--pi-output=file` captures normal output to `.tf/ralph/logs/<ticket>.log`

### Interaction with Existing Verbosity Flags

- Preserve existing semantics of `--verbose|--debug|--quiet` (Ralph logger level + propagation into workflow flags).
- Suggested MVP behavior:
  - `--progress` implies a quieter on-screen experience (progress + errors), but **must not** hide failures.

## Constraints

- Must be **opt-in** (no behavior change without new flags).
- Must not emit animated control characters when output is not a TTY.
- Must preserve error reporting and a final summary.
- Avoid a full-screen TUI.
- Prefer stdlib-only progress rendering (per-ticket updates; no tight-loop rendering needed).

## Assumptions

- `tf ralph start` can compute a meaningful total as a best-effort snapshot (e.g., `len(list_ready_tickets(...))`) and may revise it over time.
- Ticket boundary events exist (start/complete/fail) and can be hooked around the existing `run_ticket()` calls.
- Output redirection is sufficient; we do **not** need to parse `pi` output to compute progress.

## Risks & Gaps

- **Progress accuracy**: In `start` mode, the ready set can change over time; total must be labeled as best-effort.
- **Parallel mode**: Multiple concurrent tickets complicate a single-line progress bar.
  - MVP decision: **support progress only in serial mode**; if `--parallel > 1` and `--progress` is set, exit non-zero with a clear message.
- **Lost diagnostics**: Redirecting output can hide actionable info unless we print explicit pointers to the captured output.
- **Dependency temptation**: External progress libs are likely unnecessary.
  - If we later choose a library, `tqdm` is permissive (MIT/MPL-2.0) and Rich is MIT.

## Work Plan (phases / tickets)

1. **Baseline audit (code touchpoints)**
   - Confirm flag parsing touchpoints: `tf_cli/ralph.py` (`parse_run_args()`, `parse_start_args()`, `usage()` text).
   - Confirm execution touchpoint: `run_ticket()` uses `subprocess.run(args, ...)`.

2. **Implement CLI parsing + help text**
   - Add `--progress/--progressbar`, `--pi-output`, `--pi-output-file` to both run + start parsers.
   - Update `tf ralph --help` output to document new flags.

3. **Implement output routing for `pi` subprocess**
   - Add an output routing layer in `run_ticket()`:
     - inherit (current)
     - discard (`stdout=DEVNULL, stderr=STDOUT` or separate DEVNULL)
     - file (open `.log` and redirect)
   - Ensure `.tf/ralph/logs/` exists when needed.

4. **Implement progress renderer (stdlib)**
   - For serial mode only:
     - compute best-effort total (initial ready snapshot)
     - update a single line on ticket start/complete/fail
     - print final summary with counts and (if used) log file locations

5. **Tests + docs**
   - Add/extend unit tests similar to existing JSON-capture tests:
     - parsing tests for new flags
     - run_ticket redirection tests (file created, inherit/discard behavior)
     - non-TTY behavior (no control chars)
   - Document behavior in help text (this is the primary UX for this feature).

## Acceptance Criteria

- [ ] `tf ralph start --progress` in a TTY shows stable per-ticket progress without interleaved `pi` output.
- [ ] `tf ralph run --progress` behaves sensibly (per-ticket progress; output captured if needed).
- [ ] In non-TTY output, `--progress` does not emit control characters; output remains readable.
- [ ] `--pi-output=file` suppresses terminal `pi` output and records it to `.tf/ralph/logs/<ticket>.log`.
- [ ] On failure, the user sees an explicit pointer to the captured output (path) and the failure is not silent.
- [ ] `--parallel > 1` + `--progress` is rejected with a clear message (MVP scope guard).
- [ ] Default behavior is unchanged when no new flags are used.

## Open Questions

- Do we want an optional "tail-on-failure" behavior (e.g., print last 20 lines) to reduce log spelunking, or keep MVP to "print path only"?

---

## Consultant Notes (Metis)

- 2026-02-08: Corrected command name to `tf ralph` (this repo has `tf ralph run/start`; `tk ralph` does not exist).
- 2026-02-08: Noted that `tf ralph` already supports `--quiet` (logger-level quiet) and `--capture-json` (redirects `pi --mode json` output to `.tf/ralph/logs/<ticket>.jsonl`), which can be leveraged for "suppress Pi output".
- 2026-02-08: Clarified that progress mode must redirect `pi` output away from the terminal to avoid corrupting the progress line.
- 2026-02-08: Updated dependency risk: `tqdm` is permissive (MIT/MPL-2.0), not GPL; however, stdlib-only progress is likely sufficient.
- 2026-02-08: **Gap identified**: The plan says "compute best-effort total" but doesn't specify the source. It should explicitly state that `total` is derived from the actual open/ready ticket count (via `list_ready_tickets()` or similar), NOT from `maxIterations` (default 50). See also `seed-fix-progressbar-counter-currently-it-sho` for related follow-up work.
- 2026-02-08: **Suggested refinement**: In ticket #4 (progress renderer), explicitly note that the counter should show `[done/total]` where `total = len(ready_tickets)` at start, not `maxIterations`. Dynamic refresh of total is a nice-to-have for later.

## Reviewer Notes (Momus)

- 2026-02-08: PASS
  - Blockers:
    - none
  - Required changes:
    - none
  - Notes:
    - MVP explicitly limits `--progress` to serial mode to keep scope small and avoid complex multi-process rendering.
