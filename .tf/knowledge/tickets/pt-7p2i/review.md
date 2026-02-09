# Review: pt-7p2i

## Critical (must fix)
No issues found.

## Major (should fix)
1. `tf_cli/templates/topic_detail.html` - **Not migrated to design tokens**. This file still uses hardcoded color values and does not use any CSS variables, creating visual inconsistency.

2. `.tf/knowledge/tickets/pt-7p2i/implementation.md` - Documentation inaccuracy: claims "15 variables" but actually defines **18 CSS variables**. The spacing section lists 5 variables but the summary says 2.

## Minor (nice to fix)
1. `implementation.md:33-37` - Documentation inconsistency: states "Fluid spacing with clamp() (2)" but lists 5 variables. Update count for accuracy.

2. `base.html:69-72` - Priority badge colors use hardcoded hex values with `!important` instead of design tokens.

3. `index.html:36-37` - `.board-stats` uses hardcoded color `#7f8c8d` instead of a design token.

4. `index.html:71-72` - `.ticket-id` uses hardcoded color `#7f8c8d` instead of a design token.

5. `index.html:82-83` - `.ticket-meta` uses hardcoded color `#95a5a6` instead of a design token.

6. `index.html:85-88` - `.empty-state` uses hardcoded color `#95a5a6` instead of a design token.

7. `ticket.html:30-31` - `.back-link` uses hardcoded color `#3498db` instead of a design token.

8. `ticket.html:35-36` - `.ticket-id-large` uses hardcoded color `#7f8c8d` instead of a design token.

9. `ticket.html:43-46` - Status badges use hardcoded background/text colors instead of semantic tokens.

10. `ticket.html:52-54` - `.tag` uses hardcoded colors instead of design tokens.

11. `ticket.html:63-67` - Code blocks use hardcoded background `#f8f9fa` instead of a surface token.

12. `ticket.html:74-77` - `.ticket-links h3` uses hardcoded color `#7f8c8d` instead of a design token.

13. `ticket.html:80-83` - `.external-link` uses hardcoded color `#3498db` instead of a design token.

14. `topics.html:44-46` - `.search-input` uses hardcoded border color instead of `--border-strong`.

15. `topics.html:49` - `.search-input:focus` uses hardcoded color instead of a design token.

16. `topics.html:109-110` - `.empty-state` and `.no-topics` use hardcoded color instead of a design token.

## Warnings (follow-up ticket)
1. `base.html:29-33` - Design tokens are hardcoded in base template. Consider extracting to separate CSS file for theme switching.

2. `topic_detail.html` - Complete migration to design tokens needed (20+ hardcoded color values).

3. Color consistency - Hardcoded color palette appears to be a separate "Flat UI" scheme. Document if intentional, otherwise consolidate.

## Suggestions (follow-up ticket)
1. Consider leveraging CSS custom property cascading to override Pico's defaults directly rather than maintaining parallel custom styles.

2. Some hardcoded spacing values remain (e.g., `1rem`, `0.5rem`). Could migrate to token system for full consistency.

3. Add semantic color tokens for common UI patterns: `--color-text-secondary`, `--color-text-muted`, `--color-accent`, etc.

4. Consider adding typography tokens (`--font-size-sm`, `--font-size-base`, `--font-size-lg`).

5. Consider creating `--breakpoint-md` and `--breakpoint-sm` tokens for consistency.

## Summary Statistics
- Critical: 0
- Major: 2
- Minor: 16
- Warnings: 3
- Suggestions: 5

## Reviewer Sources
- reviewer-general: review-general.md
- reviewer-spec-audit: review-spec.md
- reviewer-second-opinion: review-second.md
