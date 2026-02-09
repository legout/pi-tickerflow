# Spike: Modern but simple CSS for dashboard/kanban web apps

## Summary

For internal dashboards/kanban boards, the “modern but simple” sweet spot is usually **semantic HTML + CSS variables + Grid/Flexbox**, optionally layered with a small **classless CSS framework**.

In practice you have three good levels of complexity:

1) **Pure custom CSS** (smallest, best control): add a reset + a handful of tokens + 5–8 component rules (card/column/button/badge).
2) **Classless framework** (fastest to ship): Pico.css / Water.css / MVP.css give you clean typography, buttons, and forms with nearly zero classes.
3) **Tokens + light components**: Open Props provides a modern palette/shadows/radii/spacing tokens; you write small component CSS on top.

Given Ticketflow’s current server-rendered templates, (2) or (3) are the most pragmatic.

## Key Findings

1. **Classless frameworks are great for internal tools**
   - You write semantic HTML and get reasonable typography/forms/buttons immediately.
   - Pico.css offers a “classless” variant and dark-mode support; MVP.css and Water.css are extremely small.

2. **Open Props is a strong middle ground**
   - It’s not a component framework; it’s a **token library**: colors, shadows, spacing, radii, etc.
   - Works well when you already have basic HTML structure and just want consistent visual language.

3. **Fluid spacing with `clamp()` reduces breakpoint bloat**
   - Use `clamp(min, preferred, max)` for padding, gaps, and container widths.
   - Utopia.fyi calculators make it easy to generate coherent fluid scales.

4. **Layout patterns matter more than visual polish for kanban**
   - Kanban wants: fixed column headers, scrollable column bodies, clear card affordances.
   - “Every Layout” patterns (like Switcher) are useful for responsive column switching without lots of media queries.

## Options Considered

### Option A — Pico.css (classless) + tiny overrides

**Pros**
- Very fast to implement (1 `<link>`).
- Great default typography/forms/buttons.
- Simple overrides via CSS variables.

**Cons**
- You’ll still write custom layout CSS for kanban columns/cards.
- Visual style is somewhat recognizable unless customized.

**Best fit**: internal tool/dashboard where speed > bespoke branding.

### Option B — Water.css / MVP.css (ultra-minimal)

**Pros**
- Extremely small.
- Great for prototypes.

**Cons**
- Less “app/dashboard” feel; you’ll override more for kanban.
- Some projects are “good enough” but not as actively “design-system-ish”.

**Best fit**: prototypes and POCs.

### Option C — Open Props tokens + your own components

**Pros**
- Still simple, but much more “modern product UI” look.
- Encourages consistent spacing/shadows/colors.

**Cons**
- Requires writing component CSS (card/button/badge/etc).

**Best fit**: you want a custom-ish look without Tailwind/Bootstrap.

### Option D — Web Awesome (web components)

**Pros**
- A lot of UI components, themed via CSS variables.
- Framework-agnostic.

**Cons**
- Heavier than “simple CSS”; introduces custom elements/JS.

**Best fit**: when you need many interactive components fast.

## Recommendation (for Ticketflow kanban UI)

- Start with **Pico.css classless** for baseline typography/buttons/forms.
- Add a small **kanban.css** layer with:
  - app shell grid (header + main)
  - board grid (4 columns desktop → stack on mobile)
  - card styling and status/priority badges
  - fluid spacing with `clamp()` and a few CSS variables

If you later want a more bespoke look, keep the layout CSS and swap Pico for **Open Props** tokens.

## Practical CSS snippets (minimal, modern)

### 1) Token baseline

```css
:root {
  --radius: 10px;
  --surface: #fff;
  --surface-2: #f6f7f9;
  --border: #e6e8ee;
  --shadow: 0 1px 3px rgba(0,0,0,.08);
  --gap: clamp(.75rem, 1.2vw, 1.25rem);
}
```

### 2) Board layout

```css
.board {
  display: grid;
  grid-template-columns: repeat(4, minmax(240px, 1fr));
  gap: var(--gap);
}
@media (max-width: 1024px) {
  .board { grid-template-columns: repeat(2, minmax(240px, 1fr)); }
}
@media (max-width: 640px) {
  .board { grid-template-columns: 1fr; }
}
```

### 3) Column + cards

```css
.column {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--gap);
}
.ticket-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: calc(var(--radius) - 2px);
  box-shadow: var(--shadow);
  padding: .75rem;
}
```

## Risks & Unknowns

- Classless frameworks sometimes fight with app-like layouts (you may need to neutralize some defaults).
- If you need a lot of bespoke components (menus, dialogs), a component library may become attractive.

## Next Steps

1. Decide baseline: **Pico classless** vs **Open Props**.
2. Extract Ticketflow’s existing inline styles into a dedicated CSS file and add tokens.
3. Add a responsive “board shell” CSS (grid + clamp gaps).
4. Iterate on accessibility: focus-visible outlines, contrast, reduced motion.
