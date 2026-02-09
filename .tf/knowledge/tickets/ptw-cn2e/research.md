# Research: ptw-cn2e

## Task
Add support in /tf-backlog to link tightly-related tickets using `tk link`.

## Context Reviewed
- Ticket: ptw-cn2e - Add ticket linking in tf-backlog using tk link
- Seed: seed-backlog-deps-and-tags - Parent topic for this work
- Existing backlog.md shows 8 tickets in this seed
- Current tf-planning skill has backlog generation procedure

## Key Findings

### tk link Command
```
tk link <id> <id> [id...]   Link tickets together (symmetric)
```
- Links are symmetric (unlike dependencies which are directional)
- Multiple tickets can be linked at once
- Links are advisory for discoverability, not blocking

### Linking Criteria (from ticket acceptance criteria)
- Same component + adjacent in creation order
- Title similarity (e.g., similar words/phrases)
- Conservative approach: under-linking preferred to over-linking

### Current Backlog.md Format
Already has Links column defined in skill:
```markdown
| ID | Title | Est. Hours | Depends On | Components | Links |
```

### Implementation Plan
1. Update /tf-backlog prompt to add `--no-links` flag
2. Update tf-planning skill "Backlog Generation" procedure:
   - Add linking step after ticket creation
   - Implement linking criteria logic
   - Apply links via `tk link <id> <id>`
3. Update backlog.md generation to populate Links column

## Sources
- /Users/volker/coding/libs/pi-tk-workflow/prompts/tf-backlog.md
- /Users/volker/coding/libs/pi-tk-workflow/skills/tf-planning/SKILL.md
- /Users/volker/coding/libs/pi-tk-workflow/.tf/knowledge/topics/seed-backlog-deps-and-tags/
