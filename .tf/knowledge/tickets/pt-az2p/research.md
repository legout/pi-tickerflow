# Research: pt-az2p

## Status
Research enabled. No additional external research was performed - sufficient context available from existing project documentation.

## Rationale
The ticket scope is well-defined through existing project audit documents:
- CRITICAL_REVIEW_AND_CLEANUP_PLAN.md - comprehensive audit of legacy code
- CLEANUP_PLAN.md - detailed cleanup recommendations

## Context Reviewed
- `tk show pt-az2p` - Ticket description and acceptance criteria
- CRITICAL_REVIEW_AND_CLEANUP_PLAN.md - Legacy bash script findings
- CLEANUP_PLAN.md - Consolidation plan for _new.py modules
- docs/commands.md - Command reference (shows `tf new` usage)

## Key Findings

### Legacy Bash Script (`scripts/tf_legacy.sh`)
- 4,078 lines of bash implementing: ralph, agentsmd, seed, track, next, backlog-ls, login, sync, update, doctor
- Superseded by Python CLI in `tf_cli/` directory
- Current `cli.py` has `find_legacy_script()` that returns None (code path already disabled)
- **Risk Level: LOW** - Not currently invoked by any code path

### _new.py Naming Convention
Files with `_new` suffix (indicating incomplete migration):
- ralph_new.py (1,200 lines)
- doctor_new.py
- sync_new.py
- init_new.py
- setup_new.py
- login_new.py
- next_new.py
- track_new.py
- backlog_ls_new.py
- agentsmd_new.py
- priority_reclassify_new.py
- tags_suggest_new.py
- project_bundle_new.py

## Sources
- CRITICAL_REVIEW_AND_CLEANUP_PLAN.md (project audit)
- CLEANUP_PLAN.md (consolidated cleanup plan)
