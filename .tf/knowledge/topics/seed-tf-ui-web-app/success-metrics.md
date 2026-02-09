# Success Metrics

## Spike Phase
- [ ] Documented comparison of textual-web vs FastAPI+HTMX approaches
- [ ] Working proof-of-concept for recommended approach
- [ ] Clear decision on which approach to pursue for MVP

## MVP Phase
- [ ] `tf ui --web` command starts web server successfully
- [ ] Web server binds to configurable host:port (default: 127.0.0.1:8000)
- [ ] Kanban board displays tickets in correct columns
- [ ] Clicking a ticket shows detail view
- [ ] Manual refresh button updates ticket data
- [ ] Ctrl+C gracefully shuts down the server
- [ ] Existing `tf ui` (terminal mode) continues to work unchanged

## Quality Metrics
- [ ] Page load time < 2 seconds for typical ticket set (< 100 tickets)
- [ ] Server startup time < 3 seconds
- [ ] Works in Chrome, Firefox, Safari, Edge (latest 2 versions)
- [ ] No server errors under normal usage
