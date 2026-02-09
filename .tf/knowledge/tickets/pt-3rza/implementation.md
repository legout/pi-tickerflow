# Implementation: pt-3rza

## Summary

Implemented knowledge topic index loader for the UI, enabling topic browsing by type (seed/spike/plan/baseline) with resolved documentation paths. Extended the Textual TUI with a Topics browser tab.

## Files Changed

- `tf_cli/ui.py` - Major rewrite adding:
  - `TopicIndexLoader` class for loading and querying topics from `index.json`
  - `Topic` and `TopicDoc` dataclasses for representing topics
  - `get_topic_type()` for deriving type from topic ID prefix
  - `resolve_knowledge_dir()` for finding the knowledge directory
  - `TopicBrowser` Textual widget for interactive topic browsing
  - Full TUI implementation with tabbed interface (Topics + Tickets)

- `tests/test_topic_loader.py` - New comprehensive test suite (38 tests) covering:
  - Topic type detection from ID prefixes
  - Topic loading and parsing
  - Filtering by type
  - Search functionality
  - Error handling for missing/invalid index
  - Document existence checking

## Key Decisions

1. **Reused existing patterns**: Leveraged `kb_helpers.py` patterns for knowledge directory resolution and topic type detection.

2. **Document existence checking**: The loader checks if referenced docs actually exist on disk, providing `exists: bool` flag. This allows the UI to show only available documents.

3. **Graceful error handling**: Missing or invalid `index.json` raises `TopicIndexLoadError` with helpful messages suggesting `tf kb rebuild-index`.

4. **Legacy format support**: Handles both dict format `{"topics": [...]}` and legacy list format `[...]`.

5. **Search scope**: Search matches title, keywords, or ID (case-insensitive substring).

## Acceptance Criteria Coverage

- [x] Topics can be listed and filtered by type
  - `TopicIndexLoader.get_by_type(type)` returns filtered list
  - UI groups topics by type in sidebar
  
- [x] For a topic, resolve doc paths (overview/sources/plan/backlog) when present
  - `Topic.available_docs` property returns only existing docs
  - Each doc has `path` and `exists` fields
  
- [x] Missing/invalid index.json yields a friendly UI message
  - `TopicIndexLoadError` with clear message and remediation hint
  - UI catches error and displays in detail panel

## UI Features Implemented

- Tabbed interface with "Topics" and "Tickets" tabs
- Topics sidebar with:
  - Real-time search input
  - Grouped by type (PLAN, SPIKE, SEED, BASELINE)
  - Scrollable list
- Topic detail panel showing:
  - Title, ID, type
  - Keywords
  - Available documents with paths
- Keyboard shortcuts: `q` to quit, `r` to refresh

## Tests

38 unit tests covering all functionality:
- Topic type derivation
- Topic dataclass behavior
- Loader initialization and loading
- Filtering and search
- Error conditions
- Formatting utilities

All tests pass: `pytest tests/test_topic_loader.py -v`

## Verification

Run the TUI:
```bash
tf ui
```

Or test the loader programmatically:
```python
from tf_cli.ui import TopicIndexLoader
loader = TopicIndexLoader()
topics = loader.load()
print(f"Loaded {len(topics)} topics")
print(f"Seeds: {len(loader.get_by_type('seed'))}")
```
