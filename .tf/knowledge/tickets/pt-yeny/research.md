# Research: pt-yeny

## Status
Research not required - this is an internal implementation task.

## Rationale
- The task is to implement a ticket loader module for the UI
- The format of `.tickets/*.md` files is well-defined (YAML frontmatter + markdown body)
- No external libraries or APIs need to be researched
- The existing `tf_cli/frontmatter.py` and `tf_cli/ui.py` provide patterns to follow

## Context Reviewed
- `tk show pt-yeny` - ticket requirements
- `.tickets/*.md` file format (YAML frontmatter + markdown)
- `tf_cli/frontmatter.py` - existing frontmatter utilities
- `tf_cli/ui.py` - Topic loader patterns to follow
- `tests/test_topic_loader.py` - test patterns

## Implementation Approach
- Create `tf_cli/ticket_loader.py` following the same patterns as `TopicIndexLoader`
- Use `yaml` module for frontmatter parsing (standard library or PyYAML)
- Implement lazy loading by storing file path and reading body on demand
- Add comprehensive tests in `tests/test_ticket_loader.py`

## Sources
- (none - internal implementation)
