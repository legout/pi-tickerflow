# Implementation: pt-li6a

## Summary
Created the `/tf-followups-scan` Pi prompt command that scans ticket artifact directories for missing `followups.md` files and optionally creates follow-up tickets.

## Files Changed
- `.pi/prompts/tf-followups-scan.md` - Main prompt file (new)
- `prompts/tf-followups-scan.md` - Root-level copy (new)

## Implementation Details

### Prompt Structure
The prompt follows the established pattern from `tf-followups.md`:
- YAML frontmatter with model, thinking level, and skill reference
- Clear usage documentation with examples
- Step-by-step execution procedures
- Flag handling (`--apply` for non-dry-run mode)

### Key Features
1. **Dry-run by default** - No changes made unless `--apply` flag is used
2. **Safe/idempotent** - Skips directories already containing `followups.md`
3. **Config-aware** - Reads `workflow.knowledgeDir` from settings.json
4. **Comprehensive output** - Per-ticket actions + final summary statistics

### Scan Logic
- Scans `{knowledgeDir}/tickets/*/` directories
- Eligible tickets: have `review.md` but missing `followups.md`
- Creates follow-up tickets for Warnings/Sections in review
- Marks tickets with no warnings/suggestions as "none needed"

## Verification

```bash
# Verify files created
ls -la .pi/prompts/tf-followups-scan.md prompts/tf-followups-scan.md

# Verify content structure
head -10 .pi/prompts/tf-followups-scan.md
```

## Acceptance Criteria Status

- [x] Create `.pi/prompts/tf-followups-scan.md` with usage + flags
- [x] Create `prompts/tf-followups-scan.md` (root level)
- [x] Default behavior is dry-run (no `tk create`, no file writes)
- [x] `--apply` flag performs changes
- [x] Scan uses `workflow.knowledgeDir` config
- [x] Prints per-ticket actions + final summary
- [x] Safe/idempotent: skips dirs with existing `followups.md`
