# Research: pt-li6a

## Status
Research enabled. No additional external research was performed - this is an internal workflow tool.

## Rationale
- The task is to create a Pi prompt command for scanning ticket artifacts
- All necessary context is available in the existing codebase patterns
- Similar prompt `tf-followups.md` already exists as reference

## Context Reviewed
- `tk show pt-li6a` - Ticket requirements
- `.pi/prompts/tf-followups.md` - Reference implementation pattern
- `.tf/config/settings.json` - Workflow configuration (knowledgeDir path)
- Existing ticket artifact structure in `.tf/knowledge/tickets/`

## Key Findings
- Knowledge directory: `.tf/knowledge` (from config)
- Ticket artifacts stored in: `{knowledgeDir}/tickets/{ticket-id}/`
- Need to check for `review.md` existence and `followups.md` absence
- Dry-run by default, `--apply` for actual changes

## Sources
- (none - internal implementation)
