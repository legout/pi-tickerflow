# Fixes: pt-gmpy

## Issues Fixed

### Major (2 occurrences)

#### 1. Archived session JSON example missing `inputs_used`
**Location**: `prompts/tf-backlog.md` step 11 (archived session)
**Fix**: Added `inputs_used` object to the `backlog` property:
```json
"inputs_used": {
  "seed": "{topic-id}",
  "plan": "{plan-id or null}",
  "plan_status": "{approved|draft|missing}",
  "spikes": ["{spike-id-1}", "{spike-id-2}"],
  "spikes_read": 2,
  "spikes_missing": []
}
```

#### 2. Error session JSON example missing `inputs_used`
**Location**: `prompts/tf-backlog.md` step 11 (error session)
**Fix**: Added same `inputs_used` object to the `backlog` property in error state example.

### Minor (1 occurrence)

#### 3. Inputs Used Summary timing clarification
**Location**: `prompts/tf-backlog.md` Output section
**Fix**: Changed "(emit at start when session is active)" to "(emit after Phase B input resolution when session is active)" for clarity.

## Summary
- Major fixes: 2 (both JSON examples updated)
- Minor fixes: 1 (timing clarification)
- Warnings/Suggestions: 0 (none required fixes)

All Major issues from review have been resolved. The implementation now matches the specification.
