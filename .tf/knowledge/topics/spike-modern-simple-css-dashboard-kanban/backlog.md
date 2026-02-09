# Backlog: spike-modern-simple-css-dashboard-kanban

| ID | Title | Score | Est. Hours | Depends On | Links |
|----|-------|-------|------------|------------|-------|
| pt-bsuf | Integrate Pico.css (classless) into Sanic+Datastar web UI templates | 0 | 1-2 | - | pt-7p2i,pt-33o0 |
| pt-7p2i | Add a small design-token layer (CSS variables) + fluid spacing via clamp() | 11 | 1-2 | pt-bsuf | pt-bsuf |
| pt-33o0 | Extract inline web UI CSS into a dedicated stylesheet served by Sanic | 0 | 1-2 | pt-7p2i | pt-bsuf,pt-gnhr |
| pt-gnhr | Improve Kanban board layout CSS (grid minmax/auto-fit, better responsiveness) | 0 | 1-2 | pt-33o0 | pt-33o0 |
| pt-q2og | Accessibility pass for web UI styling (focus-visible, contrast, reduced motion) | 0 | 1-2 | pt-gnhr | pt-2xr4 |
| pt-2xr4 | Add dark-mode toggle (or auto dark mode) for web UI | 0 | 1-2 | pt-q2og | pt-q2og |
