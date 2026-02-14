# Review: pt-9yjn

## Critical (must fix)
- `tf/ralph.py:799-824` - Dispatch launches with `stdout=PIPE` but parent does not consume output; long-running/high-output tasks can block on a full pipe and hang the ticket run. _(sources: reviewer-general)_
- `tf/ralph.py:793-834` - Acceptance criteria require launching real `interactive_shell` dispatch sessions, but implementation uses `subprocess.Popen(["pi", "-p", ...])` instead; this breaks the intended execution transport and attachable session semantics. _(sources: reviewer-spec-audit)_
- `tf/ralph.py:804-820` - Output file handles (`pi_output=file` and `pi_output=discard`) are opened but not closed on launcher paths, causing FD leaks across repeated dispatches. _(sources: reviewer-general, reviewer-second-opinion)_
- `tf/ralph.py:2188-2206` - Successful dispatch leaves worktrees unmerged/uncleaned with only deferred handling notes; without guaranteed completion integration this risks stranded worktrees and unfinished lifecycle state. _(sources: reviewer-second-opinion, reviewer-general)_

## Major (should fix)
- `tf/ralph.py:2565-2606` - `ralph_start` still routes parts of dispatch backend through `run_ticket()` paths, creating inconsistent behavior and skipping expected dispatch/session tracking in that flow. _(sources: reviewer-general)_
- `tf/ralph.py:708-713,779,795` - `capture_json` is accepted but not applied in dispatch execution, causing behavior drift from non-dispatch runner semantics. _(sources: reviewer-general)_
- `tf/ralph.py:749-765` - Session IDs are short/truncated UUID fragments; collision risk is low but grows with throughput and long-lived tracking. _(sources: reviewer-general, reviewer-second-opinion)_
- `tf/ralph.py:807` - `start_new_session=True` creates separate process groups without demonstrated cleanup/orphan handling in this phase. _(sources: reviewer-second-opinion)_
- `tf/ralph.py:823-831` - No immediate post-launch health check (`poll`) to catch startup failures; launcher may report success for processes that die right away. _(sources: reviewer-second-opinion)_

## Minor (nice to fix)
- `tf/ralph.py:715-719,793-795` - Docs/comments describe `interactive_shell` dispatch while implementation uses subprocess launch, increasing maintenance confusion. _(sources: reviewer-general)_
- `tf/ralph.py:793-797` - `--auto` flag insertion relies on substring matching; argument-token parsing would be more robust. _(sources: reviewer-second-opinion)_
- `tf/ralph.py:741` - Validate/guarantee safe command construction in `build_cmd()` for ticket IDs and flags. _(sources: reviewer-second-opinion)_

## Warnings (follow-up ticket)
- `tf/ralph.py:713,813-833` - `timeout_ms` is accepted but unused in dispatch launch path.
- `tf/ralph.py:2199` - Introduced `DISPATCHED` lifecycle state needs explicit downstream state-machine handling/documentation.
- `tf/ralph.py:815` - Cross-platform handle inheritance semantics (especially Windows) are unverified for output redirection.

## Suggestions (follow-up ticket)
- `tests/test_json_capture.py`, `tests/test_pi_output.py` - Add dedicated tests for `run_ticket_dispatch()` (dispatch transport, output routing, pipe safety, FD closure).
- `tf/ralph.py` - Add explicit dispatch tracking artifact/mechanism (e.g., `dispatch_info.json` or callback) to support completion handling and cleanup handoff.

## Summary Statistics
- Critical: 4
- Major: 5
- Minor: 3
- Warnings: 3
- Suggestions: 2
