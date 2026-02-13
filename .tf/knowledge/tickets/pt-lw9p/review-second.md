# Review: pt-lw9p

## Overall Assessment
The ticket pt-lw9p successfully defines and documents the fixer meta-model selection rules, producing a comprehensive design document and updated code comments. However, there are notable content inaccuracies in the tf-workflow skill documentation and a subtle bug in the `resolve_meta_model` fallback logic that could cause incorrect model resolution in edge cases.

## Critical (must fix)
No critical issues found; the system functions correctly for standard configurations where `metaModels.fixer` is defined and `agents.fixer="fixer"`.

## Major (should fix)
- `skills/tf-workflow/SKILL.md:424` (and `.pi/skills/tf-workflow/SKILL.md:424`): The line "Look up `agents.fixer` → `metaModels.general.model`" is **incorrect**. The correct resolution is: look up the meta-model key from `agents.fixer`, then retrieve the model from `metaModels` using that key. This misinformation could mislead users and lead to faulty manual configuration.
- `tf/frontmatter.py:45`: The fallback for missing meta-models returns `{"model": name, "thinking": "medium"}` which uses the **agent name** (`name`) instead of the **meta-model key** (`meta_key`). This contradicts the accompanying comment and would produce an unexpected model ID if an agent's mapping value differs from its name (e.g., `agents.fixer="custom-fixer"` with no `metaModels.custom-fixer` would fall back to model `"fixer"` instead of `"custom-fixer"`). This is a latent bug that may cause confusion in atypical setups.

## Minor (nice to fix)
None.

## Warnings (follow-up ticket)
No warnings.

## Suggestions (follow-up ticket)
- Add configuration validation (e.g., during `tf sync` or `tf init`) to warn when an agent's `agents.<name>` mapping points to a non-existent `metaModels` key, except for the special case of `fixer` which may intentionally rely on a future auto-fallback. Early warning would prevent misconfigurations from causing runtime failures.

## Positive Notes
- The design document `design-fixer-model-selection.md` is thorough, with clear resolution order, practical configuration examples, and a well-structured test plan.
- Code comments in `tf/frontmatter.py` were updated to explain the current fallback behavior, improving code maintainability.
- Backward compatibility considerations are clearly documented; the existing pattern of setting `agents.fixer="general"` continues to work without requiring `metaModels.fixer`.

## Summary Statistics
- Critical: 0
- Major: 2
- Minor: 0
- Warnings: 0
- Suggestions: 1
