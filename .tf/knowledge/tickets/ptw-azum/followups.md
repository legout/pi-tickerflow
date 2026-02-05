# Follow-ups: ptw-azum

## Status
Follow-up tickets created from review Warnings and Suggestions.

## Warnings (Future Work)
1. **Code Quality**: Move `json` import to top-level in `component_classifier.py` for consistency.
2. **Enhancement**: Consider stemming support for keyword matching (e.g., "document" matching "documentation").

## Suggestions (Enhancement Tickets)
1. **Config Loading**: Add support for `.tf/config/component-keywords.json` for project-specific keyword mappings.
2. **Confidence Scoring**: Implement confidence thresholds requiring multiple keyword matches per tag.
3. **Batch Optimization**: Cache ticket fetches when processing multiple tickets.

## Related Tickets
- ptw-xwlc: Update tf-backlog to apply component tags by default (depends on this classifier)
- ptw-ztdh: Update tf-tags-suggest to share classifier logic (this implementation satisfies this)

## Notes
These are enhancement ideas for future iterations, not blockers for the current MVP.
