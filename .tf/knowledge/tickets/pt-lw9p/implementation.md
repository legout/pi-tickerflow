# Implementation: pt-lw9p

## Summary
Defined and documented the fixer meta-model selection rules, including precedence, fallback behavior, and escalation integration. Updated code comments to clarify the actual fallback behavior.

## Retry Context
- Attempt: 1
- Escalated Models: fixer=base, reviewer-second=base, worker=base

## Files Changed
- `.tf/knowledge/tickets/pt-lw9p/design-fixer-model-selection.md` - Comprehensive design document
- `tf/frontmatter.py` - Added clarifying comments about fallback behavior

## Key Decisions

### 1. Documented Actual Behavior (Not Ideal Behavior)
The code currently treats the meta-model key as a literal model ID when the meta-model is missing. Rather than "fixing" this behavior (which would be a larger change), I documented the actual behavior so users understand the requirement to define both `metaModels.fixer` AND `agents.fixer` together.

### 2. Escalation Precedence Rules
Documented that escalation models override base models according to:
- Attempt 1: Base model (from `agents.fixer` → `metaModels`)
- Attempt 2+: `workflow.escalation.models.fixer` or base model

### 3. Backward Compatibility Strategy
- Existing configs with `agents.fixer: "general"` continue to work unchanged
- Migration requires explicit opt-in by adding `metaModels.fixer` and updating `agents.fixer`

## Changes Made

### 1. Design Document Created
Created `design-fixer-model-selection.md` with:
- Complete resolution order and precedence rules
- Configuration examples for common scenarios
- Comprehensive test plan with test case matrix
- Backward compatibility notes
- Open questions for future improvements

### 2. Code Comments Updated
Updated `tf/frontmatter.py:resolve_meta_model()` with clarifying comments:
```python
# If meta-model key is not found, treat the key itself as a literal model ID.
# This means if agents.fixer="fixer" but metaModels.fixer is missing,
# the system will try to use "fixer" as the model ID (which will likely fail).
# To use general model for fixes, explicitly set agents.fixer="general".
```

## Acceptance Criteria Status

- [x] Rules are written down (doc or code comments): precedence + fallback behavior
  - Documented in `design-fixer-model-selection.md`
  - Code comments added to `tf/frontmatter.py`
  
- [x] Backward compatibility decision recorded (when `metaModels.fixer` is missing)
  - Documented fallback behavior
  - Migration path provided
  
- [x] Any ambiguous behavior is covered by a test plan (what cases must be tested)
  - Comprehensive test plan with 9 test scenarios
  - Test case matrix covering base resolution and escalation

## Tests Run
- Code syntax validation passed
- Documentation structure validated

## Verification
- Design document is complete and comprehensive
- Code comments accurately describe actual behavior
- Test plan covers all scenarios mentioned in acceptance criteria
