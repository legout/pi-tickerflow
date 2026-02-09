# Backlog: plan-allow-to-serve-the-textual-app-as-a-web

| ID | Title | Score | Est. Hours | Depends On | Links |
|----|-------|-------|------------|------------|-------|
| pt-sf9w | Verify Ticketflow UI runs via `textual serve` | 0 | 1-2 | - | pt-ls9y |
| pt-ls9y | Document web mode: `textual serve` for `tf ui` | 0 | 1-2 | pt-sf9w | pt-sf9w,pt-uo1b |
| pt-uo1b | Add CI smoke test: headless import of `tf_cli.ui` | 0 | 1-2 | pt-ls9y | pt-ls9y,pt-et1v |
| pt-et1v | Audit web-served UI styling/assets (CSS/themes) | 0 | 1-2 | pt-uo1b | pt-uo1b,pt-fpz7 |
| pt-fpz7 | Optional: add `tf ui --web` helper (prints serve command) | 0 | 1-2 | pt-et1v | pt-et1v |