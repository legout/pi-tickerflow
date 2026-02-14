# Review: pt-9yjn

## Overall Assessment
The new dispatch launcher does not satisfy the ticket/plan requirements because `run_ticket_dispatch` never invokes the `interactive_shell` dispatch API. Instead it still spawns `pi -p ...` via `subprocess.Popen` and invents a UUID for a session identifier, so we do not actually create the isolated interactive-shell background sessions the spec promises.

## Critical (must fix)
- `tf/ralph.py:793-834` - The specification (`tk show pt-9yjn` acceptance #1 and `plan-ralph-background-interactive-shell/plan.md` requirement #1) explicitly requires each ticket to run inside a background `interactive_shell` dispatch session so that Ralph can create a fresh Pi context, report the session ID, and allow attachment/completion tracking. `run_ticket_dispatch` never touches the `interactive_shell` tool; it simply calls `subprocess.Popen(["pi", "-p", cmd])`. That means no interactive shell session actually exists, so the ticket is not implemented and later work (pt-7jzy) cannot attach to or monitor the sessions as promised.

## Major (should fix)
- `tf/ralph.py:764-833` - `session_id` is generated with `uuid.uuid4()` and returned in `DispatchResult`, but because there is no `interactive_shell` dispatch involved, this ID is just a synthetic UUID unrelated to any real background session. The ticket/plan acceptance #2 expects the actual dispatch session ID to be captured for tracking/attachment, but nothing in the code provides a session identifier that can be used by pt-7jzy or users to interact with the running Pi session.

## Minor (nice to fix)
- None

## Warnings (follow-up ticket)
- None

## Suggestions (follow-up ticket)
- None

## Positive Notes
- `tf/ralph.py:689-697` introduces the `DispatchResult` dataclass, so once the backend is wired to the real dispatch API we already have a structured place to return session metadata and errors.

## Summary Statistics
- Critical: 1
- Major: 1
- Minor: 0
- Warnings: 0
- Suggestions: 0
