# Implementation: pt-i7hx

## Summary
Updated `/tf-followups` prompt files to specify a stable `followups.md` artifact format and document behavior for edge cases (missing review.md or no Warnings/Suggestions).

## Files Changed
- `.pi/prompts/tf-followups.md` - Added stable followups.md template and "no follow-ups needed" documentation
- `prompts/tf-followups.md` - Added stable followups.md template and "no follow-ups needed" documentation

## Key Decisions
- Template includes origin ticket ID, review path, and structured sections for Warnings/Suggestions
- Added explicit "No Follow-ups Needed" section for cases where review.md is missing or has no actionable items
- Template is consistent with existing followups.md files in the knowledge base
- Maintained backward compatibility with existing ticket creation semantics

## Template Structure
The new template includes:
1. Origin metadata (ticket ID, review path)
2. Created tickets table with IDs, titles, severity, and source file/line
3. Summary statistics
4. Idempotency marker for scan command compatibility

## Edge Case Handling
- Missing review.md: Write "No Follow-ups Needed" with explanation
- No Warnings/Suggestions: Write "No Follow-ups Needed" with explicit "(none)" lists
- Empty review sections: Same as no Warnings/Suggestions

## Tests Run
- Verified template consistency with existing followups.md files
- Confirmed prompt syntax is valid markdown with YAML frontmatter

## Verification
1. Check `.pi/prompts/tf-followups.md` for updated template
2. Check `prompts/tf-followups.md` for updated template
3. Template includes all required fields per acceptance criteria
