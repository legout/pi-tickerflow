# Fixer Meta-Model Selection Rules

## Overview
This document defines how the workflow selects the model for the **fixer** step, including precedence rules, fallback behavior, and escalation integration.

## Resolution Order

The fixer model is resolved through the following precedence chain:

### 1. Escalation Override (Retry Attempts 2+)
When `workflow.escalation.enabled` is `true` and the ticket has been blocked by the quality gate:

| Attempt | Fixer Model Source |
|---------|-------------------|
| 1 | Base model (from `agents.fixer` → `metaModels`) |
| 2 | `workflow.escalation.models.fixer` or base model |
| 3+ | `workflow.escalation.models.fixer` or base model |

**Escalation precedence:**
1. If `workflow.escalation.models.fixer` is non-null, use that model ID directly
2. Otherwise, fall back to the base model resolved from `agents.fixer`

### 2. Base Model Resolution (Normal Flow)
When escalation is disabled or on attempt 1:

**Step 1:** Look up `agents.fixer` to get the meta-model key
```json
"agents": {
  "fixer": "fixer"  // meta-model key
}
```

**Step 2:** Resolve the meta-model key to actual model settings
```json
"metaModels": {
  "fixer": {
    "model": "chutes/zai-org/GLM-4.7-Flash",
    "thinking": "medium",
    "description": "..."
  }
}
```

### 3. Fallback Behavior

When `metaModels.fixer` is **not defined** but `agents.fixer` is set to `"fixer"`:

**Current behavior (tf/frontmatter.py:41):**
```python
return meta_models.get(meta_key, {"model": name, "thinking": "medium"})
```

The system treats the meta-model key (`"fixer"`) as a direct model ID. This will likely fail at runtime unless a model named exactly "fixer" exists.

**Implication:** Users MUST define both:
- `metaModels.fixer` with valid model configuration
- `agents.fixer` pointing to `"fixer"`

Or, to use the `general` model for fixes:
- Set `agents.fixer` to `"general"` (no `metaModels.fixer` needed)

## Configuration Examples

### Example 1: Dedicated Fixer Model (Recommended)
```json
{
  "metaModels": {
    "fixer": {
      "model": "chutes/zai-org/GLM-4.7-Flash",
      "thinking": "medium",
      "description": "Fast, cheap model for fix iterations"
    }
  },
  "agents": {
    "fixer": "fixer"
  },
  "workflow": {
    "escalation": {
      "enabled": true,
      "maxRetries": 3,
      "models": {
        "fixer": "openai-codex/gpt-5.3-codex"
      }
    }
  }
}
```

### Example 2: Use General Model for Fixes
```json
{
  "agents": {
    "fixer": "general"
  }
}
```

### Example 3: Disable Escalation
```json
{
  "metaModels": {
    "fixer": {
      "model": "chutes/zai-org/GLM-4.7-Flash",
      "thinking": "medium"
    }
  },
  "agents": {
    "fixer": "fixer"
  },
  "workflow": {
    "escalation": {
      "enabled": false
    }
  }
}
```

## Backward Compatibility

### Existing Configurations (Pre-fixer Meta-Model)
- `agents.fixer` defaults to `"general"` in template configs
- No `metaModels.fixer` defined
- **Behavior:** Fixer uses `metaModels.general` (unchanged from before)

### Migration Path
To adopt the new fixer meta-model:
1. Add `metaModels.fixer` with desired model
2. Change `agents.fixer` from `"general"` to `"fixer"`
3. Run `tf sync` to update agent frontmatter

## Escalation Integration

### Escalation Model Selection Logic (tf/retry_state.py)

```python
def resolve_escalation(self, escalation_config, base_models, next_attempt_number):
    if not escalation_config.get("enabled", False):
        return EscalatedModels()  # No escalation

    if next_attempt_number <= 1:
        return EscalatedModels()  # First attempt uses base

    # Attempt 2+: Check for escalation override
    if next_attempt_number >= 2:
        result.fixer = (
            escalation_config.get("models", {}).get("fixer")  # Explicit override
            or base_models.get("fixer")  # Fallback to base
        )
```

### Base Model Resolution for Escalation

The "base model" for escalation purposes is resolved as:
1. Look up `agents.fixer` → get meta-model key
2. Look up `metaModels.{key}` → get model ID
3. If meta-model missing, the base model becomes the meta-model key itself (literal model ID)

## Test Plan

### Unit Tests Required

1. **Base Resolution Tests**
   - [ ] `agents.fixer: "fixer"` + `metaModels.fixer` defined → uses that model
   - [ ] `agents.fixer: "general"` → uses `metaModels.general`
   - [ ] `agents.fixer: "fixer"` + `metaModels.fixer` missing → falls back to literal "fixer" (documented behavior)

2. **Escalation Tests**
   - [ ] Escalation disabled → always uses base model
   - [ ] Attempt 1 → uses base model
   - [ ] Attempt 2 with `escalation.models.fixer` set → uses escalation model
   - [ ] Attempt 2 without escalation override → uses base model
   - [ ] Attempt 3+ → same as attempt 2

3. **Integration Tests**
   - [ ] End-to-end: Config → sync → agent frontmatter has correct model
   - [ ] Retry scenario: Blocked ticket gets escalation model on retry

### Test Cases Table

| Scenario | agents.fixer | metaModels.fixer | escalation.enabled | escalation.models.fixer | Attempt | Expected Model |
|----------|-------------|------------------|-------------------|------------------------|---------|----------------|
| Basic | "fixer" | defined | false | N/A | 1 | metaModels.fixer.model |
| Use general | "general" | N/A | false | N/A | 1 | metaModels.general.model |
| Missing meta-model | "fixer" | missing | false | N/A | 1 | "fixer" (literal) |
| Escalation attempt 1 | "fixer" | defined | true | set | 1 | metaModels.fixer.model |
| Escalation attempt 2 | "fixer" | defined | true | set | 2 | escalation.models.fixer |
| Escalation no override | "fixer" | defined | true | null | 2 | metaModels.fixer.model |

## Related Code

- `tf/frontmatter.py:resolve_meta_model()` - Base model resolution
- `tf/retry_state.py:RetryState.resolve_escalation()` - Escalation model selection
- `tf/retry_state.py:DEFAULT_ESCALATION_CONFIG` - Default escalation settings

## Open Questions / Future Improvements

1. **Better fallback behavior:** Consider implementing automatic fallback to `general` when `metaModels.fixer` is missing, rather than treating the key as a literal model ID.

2. **Validation:** Add config validation to warn when `agents.fixer` points to a non-existent meta-model key.

3. **Documentation:** Keep this design doc synchronized with user-facing docs in `docs/configuration.md`.
