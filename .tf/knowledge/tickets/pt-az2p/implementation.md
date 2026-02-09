# Implementation: pt-az2p

## Summary
Created comprehensive deprecation policy document for TF legacy namespaces and artifacts. The policy defines clear timelines, migration paths, and removal criteria for:
1. `scripts/tf_legacy.sh` - Legacy bash implementation
2. `*_new.py` module suffix naming convention
3. `tf new` command prefix

## Files Changed
- `docs/deprecation-policy.md` (NEW) - Complete deprecation policy with timeline, migration guide, and removal criteria

## Key Decisions
1. **Three-phase deprecation approach**: Notice (3 weeks) → Soft deprecation (4 weeks) → Hard removal
2. **April 1, 2026 target** for final removal of legacy bash script
3. **March 15, 2026 target** for `_new.py` suffix removal
4. **March 1, 2026 target** for `tf new` prefix removal
5. **Rollback plan included** for safety
6. **Acceptance criteria mapped** to removal criteria checklist

## Timeline Summary

| Phase | Start | End | Focus |
|-------|-------|-----|-------|
| Notice | 2026-02-07 | 2026-02-28 | Documentation, warnings, migration guide |
| Soft Deprecation | 2026-03-01 | 2026-03-31 | Warnings emitted, CI/CD migration |
| Hard Removal | 2026-04-01 | - | Complete removal |

## Acceptance Criteria Status
- [x] Policy doc with timeline and milestones → Created `docs/deprecation-policy.md`
- [x] Communication notes for users → Section 4: Communication Strategy
- [x] Clear criteria for final removal → Section 6: Removal Criteria Checklist

## Migration Guide Provided
- Quick reference table for common substitutions
- Automated migration commands (sed)
- Verification checklist

## Tests Run
- N/A (Documentation-only change)

## Verification
- Review policy document for completeness
- Verify timeline aligns with dependent ticket pt-g42s (CLN-10)
- Confirm policy satisfies all acceptance criteria
