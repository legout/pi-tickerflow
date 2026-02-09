# Review (Second Opinion): pt-az2p

## Overall Assessment
The deprecation policy document is comprehensive and well-structured, covering all three legacy artifact categories with clear timelines, migration paths, and removal criteria. The three-phase approach (Notice → Soft Deprecation → Hard Removal) is sensible and follows industry best practices. The document successfully satisfies all acceptance criteria from the ticket.

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `docs/deprecation-policy.md:78` - **Incorrect file entry in table**: `project_bundle_new.py` is listed as having a `_new.py` suffix, but the file already exists as `tf_cli/project_bundle.py` (no `_new` suffix). This creates confusion about whether this file still needs migration. Either remove this entry from the table or clarify that it has already been renamed.

- `docs/deprecation-policy.md:328-330` - **sed pattern may be too broad**: The suggested `sed -i 's/from tf_cli\.\([a-z_]*\)_new import/from tf_cli.\1 import/g'` command uses a character class `[a-z_]*` that won't match module names containing numbers (e.g., `tf_cli/v2_doctor_new.py` if such existed). Consider `[a-z0-9_]*` for future-proofing, though this is unlikely to affect current codebase.

## Warnings (follow-up ticket)
- `docs/deprecation-policy.md:54` - **Unchecked milestone items**: Many Phase 1 and Phase 2 milestone checkboxes are unchecked. These represent actual work items (adding deprecation warnings, updating CLI help text) that need to be completed before the timeline proceeds. Consider creating a tracking ticket for these implementation tasks.

- `tf_cli/cli.py:177` - **Hard-coded module imports**: The main CLI imports all `*_new` modules directly. When the `_new.py` suffix is removed, these imports will need to be updated. This should be included in the removal criteria checklist explicitly.

- `tf_cli/new_cli.py` - **Dual command namespace maintenance burden**: The `new_cli.py` module duplicates the entire command routing logic. During the soft deprecation phase, both `cli.py` and `new_cli.py` must be kept in sync when adding new commands. This maintenance overhead should be noted in the policy.

## Suggestions (follow-up ticket)
- `docs/deprecation-policy.md` - **Add version tagging**: Consider adding semantic version tags to the deprecation timeline (e.g., "Deprecated in v1.2.0, removal in v2.0.0") to help users track deprecations via changelog rather than calendar dates.

- `docs/deprecation-policy.md` - **Add deprecation warning examples**: Include example code showing what the deprecation warnings should look like when implemented, helping ensure consistency across the codebase.

- `docs/deprecation-policy.md` - **Consider feature flags**: For the hard removal phase, suggest using feature flags or environment variables (e.g., `TF_ENABLE_LEGACY=1`) as an additional safety net before complete deletion, allowing emergency rollback without git operations.

## Positive Notes
- **Excellent structure**: The document follows a logical progression from executive summary → timeline → detailed policies → migration guide → removal criteria, making it easy to navigate.

- **Concrete migration examples**: The quick reference table (Section 5.1) and automated sed commands (Section 5.2) provide actionable guidance that reduces friction for users during migration.

- **Rollback plan included**: Section 7 provides both immediate (< 24 hours) and extended rollback procedures, showing foresight for operational issues.

- **Related tickets properly linked**: The document correctly references pt-g42s (CLN-10) as the follow-up removal ticket and pt-ynqf as a dependency, maintaining traceability in the ticket graph.

- **Verification appendix**: Appendix A provides practical grep commands for checking legacy usage, which will be valuable for both users and the team during the migration period.

- **Acceptance criteria met**: All three criteria from pt-az2p (policy doc, communication notes, removal criteria) are satisfied by the created document.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 2
- Warnings: 3
- Suggestions: 3
