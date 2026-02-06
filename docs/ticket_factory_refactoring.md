# Ticket Factory Refactoring

## Summary

Created a reusable `ticket_factory.py` module to eliminate repetitive inline Python scripts when generating backlogs via `/tf-backlog`.

## Problem

Every `/tf-backlog` command required writing an inline Python script with ~100 lines of repetitive code:
- `tk create` subprocess calls
- Manual ticket scoring (keyword weights)
- Component tag classification boilerplate
- Dependency linking logic
- Backlog.md file writing

This made prompts long, hard to maintain, and difficult to test.

## Solution

Created `/home/volker/coding/pi-ticketflow/tf_cli/ticket_factory.py` with reusable functions:

### Key Functions

| Function | Purpose |
|----------|---------|
| `TicketDef` | Define tickets with title, description, optional tags |
| `score_tickets()` | Score tickets by keyword (setup=10, test=1, etc.) |
| `create_tickets()` | Create via `tk create` with auto-component-tags |
| `apply_dependencies()` | Apply `tk dep` (chain or phases mode) |
| `apply_links()` | Link related tickets via `tk link` |
| `write_backlog_md()` | Write `backlog.md` file |
| `print_created_summary()` | Print creation summary to stdout |

### Key Features

1. **Automatic keyword scoring** - Handles word variations (test/tests/testing)
2. **Auto component tagging** - Integrates with `component_classifier`
3. **Duplicate detection** - Skips tickets matching existing titles
4. **Dependency modes** - Chain, phases, or no dependencies
5. **Automatic linking** - Links by component tags and title similarity
6. **Dry run mode** - Test without creating tickets

## Files Changed

### New Files

- `tf_cli/ticket_factory.py` (18 KB) - Main module with all ticket creation logic
- `tf_cli/ticket_factory_example.py` (5 KB) - Complete example showing usage
- `tf_cli/TICKET_FACTORY.md` (6 KB) - Module documentation

### Modified Files

- `tf_cli/__init__.py` - Re-export ticket_factory for convenience
- `tf-planning/SKILL.md` - Added "Ticket Creation with ticket_factory Module" section
- `prompts/tf-backlog.md` - Added references to ticket_factory module

## Migration Guide

### Before (Inline Script)

```python
$ python - <<'PY'
 from __future__ import annotations
 import re
 import subprocess
 from dataclasses import dataclass
 from typing import List

 TOPIC_ID = 'seed-add-more-logging'
 WEIGHTS = {'setup': 10, 'configure': 8, 'define': 6, ...}

 @dataclass
 class TicketDef:
     title: str
     description: str

 def score(text: str) -> int:
     # ... 20 lines of scoring logic
     pass

 def classify_tags(title: str, description: str) -> List[str]:
     from tf_cli.component_classifier import classify_components
     return classify_components(title, description).tags

 def tk_create(title: str, description: str, tags: List[str]) -> str:
     cmd = ['tk', 'create', title, '--description', description, ...]
     out = subprocess.check_output(cmd, text=True).strip()
     return out

 # ... 50+ more lines of boilerplate
PY
```

### After (Using ticket_factory)

```python
from __future__ import annotations
from tf_cli.ticket_factory import (
    TicketDef,
    create_tickets,
    write_backlog_md,
    score_tickets,
    apply_dependencies,
    apply_links,
    print_created_summary,
)

TOPIC_ID = 'seed-add-more-logging'

tickets = [
    TicketDef(title="...", description="..."),
    TicketDef(title="...", description="..."),
]

scored = score_tickets(tickets)
created = create_tickets(scored, topic_id=TOPIC_ID, mode="seed")
created = apply_dependencies(created, mode="chain")
created = apply_links(created)
write_backlog_md(created, topic_id=TOPIC_ID)
print_created_summary(created)
```

**Result:** ~10 lines vs ~100 lines of code

## Usage in `/tf-backlog`

The tf-backlog prompt now includes instructions to use `ticket_factory`:

```python
from tf_cli.ticket_factory import (
    TicketDef,
    create_tickets,
    write_backlog_md,
    score_tickets,
    apply_dependencies,
    apply_links,
    print_created_summary,
)

# Define tickets
tickets = [TicketDef(...), ...]

# Score, create, link, write
scored = score_tickets(tickets)
created = create_tickets(scored, topic_id=TOPIC_ID, mode="seed", component_tags=True)
created = apply_dependencies(created, mode="chain")
created = apply_links(created)
write_backlog_md(created, topic_id=TOPIC_ID)
print_created_summary(created)
```

## Benefits

1. **Reduced prompt size** - Prompts are shorter and clearer
2. **Consistent behavior** - All backlogs use the same scoring/creation logic
3. **Testable** - Functions can be unit tested independently
4. **Maintainable** - Bug fixes apply to all backlogs automatically
5. **Documented** - Clear API reference and examples
6. **Extensible** - Easy to add new features (e.g., custom weight maps)

## Testing

```bash
# Test imports work
python -c "from tf_cli.ticket_factory import *; print('OK')"

# Run dry-run example
python tf_cli/ticket_factory_example.py

# Unit tests (if test_ticket_factory.py exists)
pytest tests/test_ticket_factory.py
```

## Next Steps

1. Consider adding unit tests for `ticket_factory.py`
2. Update other planning prompts (tf-seed, tf-baseline, tf-plan) to use the module
3. Consider adding a CLI wrapper: `tf tickets create-from-file tickets.json`
4. Add support for custom keyword weight maps per project
