# Research: pt-gnhr

## Status
Research not required - sufficient knowledge available from completed spike.

## Context Reviewed
- Ticket `pt-gnhr`: Improve Kanban board layout CSS (grid minmax/auto-fit, better responsiveness)
- Spike: `spike-modern-simple-css-dashboard-kanban` - contains complete CSS patterns
- Completed ticket `pt-33o0` - extracted inline CSS to `tf_cli/static/web-ui.css`
- Current implementation in `tf_cli/static/web-ui.css` and `tf_cli/templates/_board.html`

## Key Findings from Spike

The spike recommends:
1. **Board grid**: `repeat(4, minmax(240px, 1fr))` or `auto-fit` for responsive columns
2. **Fluid spacing**: Use `clamp()` for responsive gaps without excessive breakpoints
3. **Responsive strategy**: 
   - Desktop: 4 columns
   - Tablet (≤1024px): 2 columns  
   - Mobile (≤640px): 1 column
4. **Column behavior**: Fixed headers, scrollable bodies for kanban columns

## Current Implementation Analysis

**Existing CSS (web-ui.css):**
- ✅ Uses CSS variables for design tokens
- ✅ Uses `clamp()` for fluid spacing
- ✅ Board grid: `repeat(4, minmax(240px, 1fr))`
- ✅ Has responsive breakpoints at 1024px and 640px
- ⚠️ Uses `overflow-x: auto` on board which may cause horizontal scrolling issues
- ⚠️ Column scroll behavior not explicitly defined
- ⚠️ Could benefit from `auto-fit` for better flexibility

## Implementation Approach

Improve the existing CSS with:
1. Better responsive grid using `auto-fit` with `minmax()`
2. Explicit column scroll behavior for long lists
3. Consistent column heights using flex/grid
4. Improved breakpoints for common device sizes

## Sources
- `/home/volker/coding/pi-ticketflow/.tf/knowledge/topics/spike-modern-simple-css-dashboard-kanban/spike.md`
- `/home/volker/coding/pi-ticketflow/tf_cli/static/web-ui.css`
- `/home/volker/coding/pi-ticketflow/tf_cli/templates/_board.html`
