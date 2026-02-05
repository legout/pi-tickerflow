# Implementation: ptw-f3

## Summary
Enhanced the tf-planning skill with a keyword-based scoring system for smarter ticket ordering during backlog generation.

## Files Changed
- `/home/volker/.pi/agent/skills/tf-planning/SKILL.md` - Added keyword scoring step and examples

## Key Changes

### 1. Added Step 7: Score and Order Tickets
Inserted a new step in the Backlog Generation procedure that:
- Assigns weights to keywords based on foundational impact:
  - setup = 10 (foundational infrastructure)
  - configure = 8 (environment/configuration)
  - define = 6 (API contracts, interfaces)
  - design = 5 (architecture and patterns)
  - implement = 3 (core feature development)
  - test = 1 (verification and validation)
- Calculates cumulative scores for tickets with multiple keywords
- Sorts tickets by score descending (higher score = higher priority)

### 2. Renumbered Subsequent Steps
- Step 7 → Step 8 (Create tickets)
- Step 8 → Step 9 (Create via tk)
- Step 9 → Step 10 (Infer dependencies)
- Step 10 → Step 11 (Write backlog.md)

### 3. Updated backlog.md Format
Added "Score" column to the backlog table for reference:
```
| ID | Title | Score | Est. Hours | Depends On |
```

### 4. Added Keyword Scoring Examples Section
Comprehensive examples showing:
- Basic scoring with single keywords
- Cumulative scoring with multiple keywords
- Comparison of design vs implementation ordering

## Key Decisions
- **Weight rationale**: Higher weights for foundational work (setup, configure) ensure infrastructure is built before features
- **Cumulative scoring**: Tickets with multiple keywords get higher priority, recognizing complex foundational tasks
- **Tie-breaking**: Equal scores maintain original derivation order for predictability

## Tests Run
- Verified markdown formatting
- Confirmed all step renumbering is consistent
- Checked table alignment in backlog.md format

## Verification
To verify the implementation:
1. Read the updated SKILL.md at `/home/volker/.pi/agent/skills/tf-planning/SKILL.md`
2. Locate the "Backlog Generation" procedure
3. Confirm Step 7 contains the keyword scoring logic
4. Verify the "Keyword Scoring Examples" section is present
