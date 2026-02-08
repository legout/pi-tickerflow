---
id: pt-whcy
status: closed
deps: [pt-cj59]
links: [pt-cj59, pt-4dji]
created: 2026-02-08T18:41:27Z
type: task
priority: 2
assignee: legout
external-ref: seed-move-ralph-session-away-from-tf-ralph-us
tags: [tf, backlog, component:config, component:docs, component:workflow]
---
# Backward compatibility: detect legacy .tf/ralph/sessions and warn

## Task
Add backward compatibility behavior for projects that already have `.tf/ralph/sessions` session files.

## Context
Changing the default location may surprise users. A safe approach is to warn and/or prefer the legacy directory when it exists, unless explicitly overridden.

## Acceptance Criteria
- [ ] If legacy `.tf/ralph/sessions` exists and user did not set `sessionDir`, emit a clear warning with next steps
- [ ] Provide a documented way to force legacy behavior (config or env var)
- [ ] No automatic bulk migration required for MVP

## Constraints
- Avoid noisy warnings on every loop iteration (warn once per run)

## References
- Seed: seed-move-ralph-session-away-from-tf-ralph-us



## Notes

**2026-02-08T23:03:36Z**


## Implementation Complete

**Summary**: Added backward compatibility warning for legacy `.tf/ralph/sessions` directory.

**Changes**:
- Modified `tf_cli/ralph.py` with:
  - Constants for legacy session directory detection
  - Enhanced `resolve_session_dir()` with warning logic
  - Support for `RALPH_FORCE_LEGACY_SESSIONS` env var
  - Updated usage docs

**Commit**: 4acc7f8

**Review Results**:
- Critical: 0
- Major: 0
- Minor: 3 (cosmetic/formatting - acceptable)
- Warnings: 1
- Suggestions: 4

**Acceptance Criteria**: All met ✓
- ✅ Detects legacy directory and warns
- ✅ Provides escape hatches (env var + config)
- ✅ No automatic migration (MVP constraint met)
- ✅ Warns once per run

