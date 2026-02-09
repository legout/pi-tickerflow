# Backlog: plan-add-progressbar-to-tk-ralph

| ID | Title | Score | Est. Hours | Depends On | Links |
|----|-------|-------|------------|------------|-------|
| pt-pje2 | Define + parse tf ralph progress / pi-output flags | 9 | 1-2 | - | pt-zloh |
| pt-zloh | Implement pi subprocess output routing (inherit/file/discard) | 3 | 1-2 | pt-pje2 | pt-pje2,pt-pnli |
| pt-pnli | Implement serial progress display for tf ralph (per-ticket) | 3 | 1-2 | pt-zloh | pt-zloh,pt-uisf |
| pt-uisf | Test tf ralph progress + pi-output suppression | 1 | 1-2 | pt-pnli | pt-pnli |