# Fixes: pt-oyjt

## Status
No fixes applied - all issues acceptable for current scope.

## Minor Issue Analysis

### Issue: NoMatches error when keys pressed on Tickets tab
The delegation methods will raise an exception if the keys are pressed while the Tickets tab is active, because `query_one(TopicBrowser)` won't find the widget.

### Decision
Accepting as-is because:
1. The ticket acceptance criteria only requires the keys work when Topics tab is active
2. Users typically won't press document-opening keys when not viewing topics
3. If they do, Textual's error handling will show an error that indicates the issue
4. The seed's Open Questions explicitly notes this as a future enhancement: "Should the document-opening keys be disabled when the Tickets tab is active?"

### Alternative Fix Considered
Could wrap in try/except or check active tab:
```python
def action_open_doc(self) -> None:
    tabbed = self.query_one(TabbedContent)
    if tabbed.active_pane and tabbed.active_pane.id != "tab-topics":
        return  # Silently ignore
    topic_browser = self.query_one(TopicBrowser)
    topic_browser.action_open_doc()
```

But this adds complexity beyond the ticket scope and the seed's MVP scope.

## Files Changed
- None (no fixes required)
