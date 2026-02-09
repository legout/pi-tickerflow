# Backlog: seed-add-ralph-loop-timeout-restarts

| ID | Title | Score | Est. Hours | Depends On | Links |
|----|-------|-------|------------|------------|-------|
| pt-4qvw | Define Ralph timeout + restart configuration surface | 9 | 1-2 | - | pt-hstd |
| pt-hstd | Implement subprocess timeout + safe termination for pi run | 3 | 1-2 | pt-4qvw | pt-4qvw,pt-hfqc |
| pt-hfqc | Add bounded restart loop for timed-out ticket attempts (serial mode) | 3 | 1-2 | pt-hstd | pt-hstd,pt-c2b0 |
| pt-c2b0 | Add tests for timeout + restart behavior in tf ralph | 1 | 1-2 | pt-hfqc | pt-hfqc,pt-j485 |
| pt-j485 | Ensure cleanup semantics after timeout (worktrees/lock/progress) | 0 | 1-2 | pt-c2b0 | pt-c2b0 |