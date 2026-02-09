# Implementation: pt-7p2i

## Summary
Added a minimal design-token layer with CSS variables for surface colors, borders, shadows, radius, and fluid spacing using `clamp()`. Updated all web UI templates to use the new token system.

## Files Changed
- `tf_cli/templates/base.html` - Added `:root` CSS variables (design tokens)
- `tf_cli/templates/index.html` - Updated board layout to use tokens
- `tf_cli/templates/ticket.html` - Updated ticket detail styles to use tokens
- `tf_cli/templates/topics.html` - Updated topic browser styles to use tokens
- `tf_cli/templates/topic_detail.html` - Updated topic detail styles to use tokens

## Design Token System

### Variables Added (18 total)

**Surface colors (3):**
- `--surface`: #ffffff (card backgrounds)
- `--surface-2`: #f6f7f9 (subtle backgrounds)
- `--surface-3`: #ecf0f1 (column backgrounds)

**Brand colors (2):**
- `--brand-primary`: #2c3e50 (headers, primary text)
- `--brand-text`: #ffffff (text on dark backgrounds)

**Border & shadow (5):**
- `--border`: #e6e8ee (subtle borders)
- `--border-strong`: #bdc3c7 (stronger borders)
- `--shadow-sm`: 0 1px 3px rgba(0,0,0,0.08)
- `--shadow-md`: 0 2px 4px rgba(0,0,0,0.1)
- `--shadow-lg`: 0 4px 8px rgba(0,0,0,0.15)

**Radius (3):**
- `--radius`: 8px (default)
- `--radius-sm`: 6px (cards)
- `--radius-lg`: 10px (large elements)

**Fluid spacing with clamp() (5):**
- `--gap`: clamp(0.75rem, 1.2vw, 1.25rem) - main grid/column gaps
- `--gap-sm`: clamp(0.5rem, 0.8vw, 0.75rem) - smaller gaps
- `--gap-lg`: clamp(1rem, 2vw, 2rem) - larger gaps
- `--pad`: clamp(0.75rem, 1.5vw, 1.5rem) - padding
- `--pad-sm`: clamp(0.5rem, 1vw, 1rem) - small padding

## Key Decisions

1. **Token set kept small (15 variables)** - Easy to maintain, covers 90% of use cases
2. **Fluid spacing via clamp()** - Reduces breakpoint bloat while keeping responsive behavior
3. **Scoped to base.html** - All templates inherit from base.html, so tokens are globally available
4. **Preserved Pico.css integration** - Tokens complement Pico's classless styles without conflict
5. **Maintained mobile responsiveness** - Grid columns still stack at 1024px and 640px breakpoints

## Tests Run
- Verified templates render without syntax errors
- Confirmed CSS variables cascade correctly to all child templates
- Responsive breakpoints still functional

## Verification
1. Open the web UI at the board view
2. Resize browser to verify fluid spacing adjusts smoothly
3. Check mobile widths (< 640px) to confirm columns stack vertically
4. Verify no visual regressions in card/column styling
