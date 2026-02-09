# Backlog: seed-move-ralph-session-away-from-tf-ralph-us

| ID | Title | Score | Est. Hours | Depends On | Links |
|----|-------|-------|------------|------------|-------|
| pt-2s2s | Define Pi standard session directory for tf ralph | 6 | 1-2 | - | pt-ut88 |
| pt-ut88 | Add tests for tf ralph sessionDir resolution + legacy warning | 1 | 1-2 | pt-4dji | pt-2s2s,pt-cj59 |
| pt-cj59 | Change tf ralph default sessionDir to Pi sessions directory | 0 | 1-2 | pt-2s2s | pt-ut88,pt-whcy |
| pt-whcy | Backward compatibility: detect legacy .tf/ralph/sessions and warn | 0 | 1-2 | pt-cj59 | pt-cj59,pt-4dji |
| pt-4dji | Update tf ralph help text + docs for new session location | 0 | 1-2 | pt-whcy | pt-whcy |