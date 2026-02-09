# Review: pt-az2p

## Critical (must fix)
No issues found.

## Major (should fix)
- `docs/deprecation-policy.md:1` - **Header format inconsistency with project conventions**: The document uses H1 format `# Deprecation Policy: TF Legacy Namespaces` while other docs (e.g., `artifact-policy.md`) use simpler title format `# Runtime Artifact Policy`. Consider removing the `:` subtitle format for consistency. *(from reviewer-general)*

## Minor (nice to fix)
- `docs/deprecation-policy.md:26` - **Date format consistency**: The dates use ISO format (good) but consider adding day-of-week for human readability, e.g., "2026-02-07 (Saturday)" in the Executive Summary table. *(from reviewer-general)*
- `docs/deprecation-policy.md:49` - **Unchecked milestone items**: Milestone checkboxes under Phase 1 show `[x]` for the policy publication but unchecked items for warnings/CLI updates. These represent follow-up work - consider adding ticket references (e.g., `See pt-g42s`) to link these items to actual work tickets. *(from reviewer-general)*
- `docs/deprecation-policy.md:128` - **Broken relative path in example**: The sed command shows `*.py` which may not target the correct `tf_cli/` directory. Consider using `sed -i 's/from tf_cli\.\([a-z_]*\)_new import/from tf_cli.\1 import/g' tf_cli/*.py` for accuracy. *(from reviewer-general)*
- `docs/deprecation-policy.md:203` - **Missing file count**: The table lists 13 `_new.py` files but only shows 12 in the detailed list. Review and correct the file count. *(from reviewer-general)*
- `docs/deprecation-policy.md:78` - **Incorrect file entry in table**: `project_bundle_new.py` is listed as having a `_new.py` suffix, but the file already exists as `tf_cli/project_bundle.py` (no `_new` suffix). Remove this entry or clarify that it has already been renamed. *(from reviewer-second-opinion)*
- `docs/deprecation-policy.md:328-330` - **sed pattern may be too broad**: The suggested sed command uses character class `[a-z_]*` that won't match module names containing numbers. Consider `[a-z0-9_]*` for future-proofing. *(from reviewer-second-opinion)*

## Warnings (follow-up ticket)
- `docs/deprecation-policy.md:39-43` - **Hard-coded dates may become stale**: The phase dates are hard-coded. Create follow-up ticket to update status fields as phases transition. *(from reviewer-general)*
- `docs/deprecation-policy.md:302-307` - **Rollback plan lacks owner**: The rollback plan doesn't specify who has authority to execute rollback or how to decide between immediate vs extended rollback. Add to operational runbook ticket. *(from reviewer-general)*
- `docs/deprecation-policy.md:54` - **Unchecked milestone items**: Many Phase 1 and Phase 2 milestone checkboxes are unchecked. These represent actual work items that need tracking tickets. *(from reviewer-second-opinion)*
- `tf_cli/cli.py:177` - **Hard-coded module imports**: The main CLI imports all `*_new` modules directly. When the `_new.py` suffix is removed, these imports will need to be updated. Include in removal criteria checklist. *(from reviewer-second-opinion)*
- `tf_cli/new_cli.py` - **Dual command namespace maintenance burden**: The `new_cli.py` module duplicates command routing logic. During soft deprecation, both must be kept in sync. Note this maintenance overhead in the policy. *(from reviewer-second-opinion)*

## Suggestions (follow-up ticket)
- `docs/deprecation-policy.md` - **Add document to index**: Consider adding this document to `docs/README.md` or creating a docs index. *(from reviewer-general)*
- `docs/deprecation-policy.md:335` - **Metrics tracking**: Section 8 defines success metrics but doesn't specify how they'll be measured. Create monitoring/alerting ticket for tracking. *(from reviewer-general)*
- `docs/deprecation-policy.md:349-354` - **Related tickets table**: The table shows pt-g42s as "Blocked" but doesn't indicate what it's blocked on. Clarify that it's blocked on this policy document. *(from reviewer-general)*
- `docs/deprecation-policy.md` - **Add FAQ section**: Consider adding a "Frequently Asked Questions" section to proactively address common migration concerns. *(from reviewer-spec-audit)*
- `docs/deprecation-policy.md` - **Add version tagging**: Consider adding semantic version tags to the deprecation timeline to help users track deprecations via changelog. *(from reviewer-second-opinion)*
- `docs/deprecation-policy.md` - **Add deprecation warning examples**: Include example code showing what the deprecation warnings should look like when implemented. *(from reviewer-second-opinion)*
- `docs/deprecation-policy.md` - **Consider feature flags**: For the hard removal phase, suggest using feature flags or environment variables (e.g., `TF_ENABLE_LEGACY=1`) as an additional safety net. *(from reviewer-second-opinion)*

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 6
- Warnings: 5
- Suggestions: 7

## Spec Compliance
✓ All acceptance criteria from ticket pt-az2p satisfied:
- Policy doc with timeline and milestones → Section 1-3
- Communication notes for users → Section 4
- Clear criteria for final removal → Section 6

## Reviewers
- reviewer-general (gpt-5.1-codex-mini)
- reviewer-spec-audit (gpt-5.3-codex)
- reviewer-second-opinion (gemini-3-flash)
