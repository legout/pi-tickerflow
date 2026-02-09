# Fixes: pt-m2qh

## Major Fix Applied

### Step Numbering Clarity
**Issue**: The "Session-Aware Topic Resolution" subsection used steps 1-3, then the main procedure restarted at "1. Locate topic directory". This created ambiguous step references in the "Session Handling" section which refers to "steps 5-7".

**Fix**: Changed the Session-Aware Topic Resolution steps from numeric (1, 2, 3) to alphanumeric (A.1, A.2, A.3) to clearly distinguish them from the main procedure steps.

**File**: `prompts/tf-backlog.md`

**Before**:
```markdown
1. **Check for active session**: ...
2. **Resolve the topic argument**: ...
3. **Proceed with resolved topic**: ...
```

**After**:
```markdown
A.1 **Check for active session**: ...
A.2 **Resolve the topic argument**: ...
A.3 **Proceed with resolved topic**: ...
```

## Verification
- All 561 tests pass
- Frontmatter is valid
- Session store module functions correctly
