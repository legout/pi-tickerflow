# Review: ptw-gbod

## Overall Assessment
The implementation adds documentation for optional flags (`--no-deps`, `--no-component-tags`, `--no-links`, `--links-only`) to disable automatic behaviors in `/tf-backlog`. While the flag descriptions are present, there's a **critical discrepancy** between what the implementation summary claims and what's actually in the files. The claimed "Phase 0: Flag Parsing" section with robust flag parsing logic is missing from the prompt file, and the ticket_factory examples don't show how to respect these flags.

## Critical (must fix)
- `prompts/tf-backlog.md` - **Missing "Phase 0: Flag Parsing" section**: The implementation.md claims this was added with "robust flag parsing logic" and code examples, but the file contains only flag descriptions in the Options section with no formal parsing code. The ticket_factory example shows `component_tags=True` hardcoded instead of respecting flags.

## Major (should fix)
- `skills/tf-planning/SKILL.md` - **Incomplete Flags section**: The "Flags" section in the Backlog Generation procedure only lists `--no-deps`, but the implementation covers four flags total. The other three (`--no-component-tags`, `--no-links`, `--links-only`) are only mentioned as notes in steps 9-11, not in a centralized Flags section. This makes it easy to miss the full flag surface.
- `skills/tf-planning/SKILL.md` - **No flag parsing example**: Unlike the claimed implementation, there's no code example showing how to parse these flags in Python for use with the ticket_factory module.
- `prompts/tf-backlog.md` - **ticket_factory example doesn't respect flags**: The example shows `component_tags=True` and doesn't show how to conditionally set `dep_mode` based on flags, making it unclear how implementers should actually use the flags.

## Minor (nice to fix)
- `prompts/tf-backlog.md:78` - The `--links-only` description says "Skip ticket creation (steps 5-7)" but step 5 says "Skip this step if `--links-only` provided" which is slightly inconsistent - one says 5-7, the other implies only 5.

## Warnings (follow-up ticket)
- None identified

## Suggestions (follow-up ticket)
- Consider adding a reusable flag parsing utility in `tf_cli` module so prompts don't need to inline the parsing logic
- Add a concrete example showing the full flag-to-behavior mapping:
  ```python
  flags = {
      'no_deps': '--no-deps' in args,
      'no_component_tags': '--no-component-tags' in args,
      'no_links': '--no-links' in args,
      'links_only': '--links-only' in args,
  }
  ```

## Positive Notes
- The four flags are well-documented with clear descriptions of their effects
- The flag defaults are sensible (all automatic behaviors ON by default)
- The `--links-only` mode has a clear use case documented (retroactive linking)
- The Options section in the prompt file is comprehensive with good examples

## Summary Statistics
- Critical: 1
- Major: 3
- Minor: 1
- Warnings: 0
- Suggestions: 2
