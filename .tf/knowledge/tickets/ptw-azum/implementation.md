# Implementation: ptw-azum

## Summary

Implemented a conservative component classifier for the Ticketflow CLI that uses keyword mapping to suggest component tags (`component:cli`, `component:api`, `component:docs`, `component:tests`, `component:config`, `component:workflow`, `component:agents`) based on ticket titles and descriptions.

## Files Changed

### New Files

- `tf_cli/component_classifier.py` - Core classifier module with:
  - `DEFAULT_KEYWORD_MAP` - Documented mapping of keywords to component tags
  - `classify_components()` - Main classification function
  - `ClassificationResult` - Result dataclass with tags, rationale, and matched keywords
  - `suggest_tags_for_ticket()` - Fetch and classify existing tickets via `tk show`
  - `get_keyword_map_documentation()` - Generate markdown documentation
  - CLI interface for testing (`python -m tf_cli.component_classifier "text"`)

- `tf_cli/tags_suggest_new.py` - CLI commands:
  - `tf new tags-suggest [--ticket <id>] [title] [--json] [--rationale]`
  - `tf new tags-classify <text> [--json] [--rationale]`
  - `tf new tags-keywords` - Show keyword mapping documentation

- `tests/test_component_classifier.py` - Comprehensive tests covering:
  - All component keyword matching
  - Custom keyword support
  - Edge cases and formatting

### Modified Files

- `tf_cli/new_cli.py` - Added imports and command routing for new `tags-*` commands

## Key Decisions

1. **Keyword Matching Strategy**: Used case-insensitive matching with word boundaries for longer terms (>4 chars) and substring matching for short terms. Multi-word keywords are matched as substrings.

2. **Conservative Classification**: Only assigns tags when keywords explicitly match. No ML or fuzzy matching to maintain explainability.

3. **Extensibility**: 
   - `custom_keywords` parameter merges with defaults
   - `keyword_map` parameter completely replaces defaults
   - Easy to add new components without touching core logic

4. **Rationale for Debug**: Each tag includes rationale showing which keywords matched, useful for debugging and transparency.

5. **Component Taxonomy**: Based on the seed-backlog-deps-and-tags MVP scope:
   - `component:cli` - Command-line interface features
   - `component:api` - API/REST/GraphQL endpoints
   - `component:docs` - Documentation, README, guides
   - `component:tests` - Testing, pytest, coverage
   - `component:config` - Configuration, settings, dotfiles
   - `component:workflow` - IRF workflow, Ralph, tickets
   - `component:agents` - Agents, subagents, prompts, skills

## Tests Run

```bash
python3 -m pytest tests/test_component_classifier.py -v
# 24 tests passed

python3 -m pytest tests/ -v
# 62 tests passed (including existing)
```

## Verification

```bash
# Test CLI
python3 -m tf_cli.cli new tags-classify "Add --version flag to CLI" --rationale
# Output: component:cli with rationale

python3 -m tf_cli.cli new tags-suggest --ticket ptw-azum --rationale
# Output: component:workflow with rationale

python3 -m tf_cli.cli new tags-keywords
# Output: Full keyword mapping documentation
```

## Future Work

- Integrate classifier into `tf new backlog-generate` (ticket ptw-xwlc)
- Update `tf-tags-suggest` legacy command to use this classifier (ticket ptw-ztdh)
- Add configuration option for project-specific keyword mappings
- Support regex patterns in keyword map for advanced matching
