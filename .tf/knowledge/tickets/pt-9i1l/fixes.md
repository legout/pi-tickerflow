# Fixes: pt-9i1l

## Summary
Addressed 2 Critical and 6 Major issues identified in review.

## Critical Issues Fixed

### 1. Mismatched "implemented ticket" heuristic
**Problem**: Used `implementation.md` AND `review.md` instead of `close-summary.md` as specified in plan.

**Fix**: Updated the heuristic definition:
- Changed from requiring `implementation.md` AND `review.md`
- Now uses `close-summary.md` existence as the MVP heuristic
- Added note about future `--implemented-heuristic` flag support

**Location**: SKILL.md, Step 2 of Follow-ups Scan procedure

### 2. Command naming mismatch
**Problem**: Documented `/tf-followups-scan` but settings.json had no such prompt entry.

**Fix**: Added `"tf-followups-scan": "planning"` to settings.json prompts section.

**Location**: `.tf/config/settings.json`, prompts map

## Major Issues Fixed

### 3. Missing `--json` flag
**Fix**: Added `--json` flag for structured output (CI/automation friendly).

### 4. Missing `--stop-on-error` flag
**Fix**: Added `--stop-on-error` flag to abort on `tk create` failures (default: continue with logging).

### 5. Missing `followups.md` artifact format
**Fix**: Updated apply mode to document exact format:
- Frontmatter with Generated timestamp and Source reference
- ## Created Tickets section
- ## Skipped Items section
- Special handling for "no review.md" and "no follow-ups needed" cases

### 6. Missing idempotency documentation
**Fix**: Added explicit step for idempotency check:
- Skip tickets that already have `followups.md`
- Added to Safety Defaults section

### 7. `--since` flag frontmatter issue
**Fix**: Changed to check `close-summary.md` timestamp instead of `implementation.md` frontmatter.

### 8. `scan-followups.md` location issue
**Fix**: Changed scan log to use timestamped filename `{ticketsDir}/followups-scan-{timestamp}.md` for historical tracking.

## Additional Improvements

- Added **atomic writes** documentation (temp + rename)
- Added **graceful degradation** documentation (continue on errors)
- Updated **example usage** section to include new flags
- Added note about future `--implemented-heuristic` flag extensibility

## Files Changed
1. `.pi/skills/tf-planning/SKILL.md` - Updated Follow-ups Scan procedure
2. `.tf/config/settings.json` - Added `tf-followups-scan` prompt entry

## Verification
- Reviewed changes against `plan-implement-auto-followups` requirements
- Confirmed all Critical and Major issues from review are addressed
- Minor issues (2), Warnings (4), and Suggestions (4) remain as non-blocking follow-up items
