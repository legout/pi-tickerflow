# Spike: Kanban-style TUI in Python

## Summary

A Kanban-style TUI needs:
- multi-column layout (lists of cards)
- keyboard navigation + keybindings (move card left/right, open details, edit)
- incremental rendering without flicker
- optional mouse support

The strongest “build a real app” option in Python today is **Textual** (from Textualize). It’s explicitly designed for full-screen TUIs with widgets, layout, events, and styling, and there is at least one published Kanban TUI (`kanban-cli`) demonstrating feasibility.

## Key Findings

1. **Textual is the modern, high-level framework** for full-screen TUIs (widgets, CSS-like styling, event model) and has strong docs + examples.
2. **Textual-based Kanban exists**: `kanban-cli` on PyPI provides a terminal Kanban board with commands for add/move/edit/filter/sort.
3. **Urwid is mature and stable**, good if you want a curses-style widget library and don’t need modern styling.
4. **prompt_toolkit excels at interaction** (input editing, keybindings) and can support full-screen apps, but you build more of the layout/widgets yourself.
5. **pyTermTk / PyTermGUI** are viable middle-ground toolkits (widget-based, more “GUI-like”) worth considering if Textual is too heavy.

## Options Considered

### Option A — Textual (Recommended)

**Why it fits Kanban**
- Containers/layouts can naturally express 3–5 columns.
- Event model makes “move card left/right” straightforward.
- Styling makes it easier to keep the board readable.

**Evidence / references**
- Official docs: https://textual.textualize.io/getting_started/
- Kanban example app: https://pypi.org/project/kanban-cli/

**Pros**
- Most productive for app-like TUIs
- Active ecosystem and documentation
- Good-looking UIs without bespoke ANSI hacks

**Cons**
- Adds a framework dependency
- Learning curve vs simple curses

### Option B — Urwid

**What it is**
- Curses-style, widget-based framework with a main loop.

**Pros**
- Mature and widely packaged
- Good for classic terminal UI patterns

**Cons**
- Less “modern” styling ergonomics than Textual
- More manual work to make it feel polished

Reference: https://archlinux.org/packages/extra/any/python-urwid/

### Option C — prompt_toolkit

**What it is**
- Great for prompt-heavy apps and rich keybindings; supports full-screen apps.

**Pros**
- Best-in-class input editing + keybindings
- Lightweight building block if your UI is mostly “lists + prompts”

**Cons**
- More DIY for complex widgets / kanban board layout

Reference (docs example page): https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_a_choice.html

### Option D — pyTermTk / PyTermGUI

**pyTermTk**
- Qt-like terminal widget toolkit with designer tooling.
- Ref: https://pypi.org/project/pyTermTk/

**PyTermGUI**
- Widget framework + markup/styling focus.
- Ref: https://bczsalba.com/post/the-tui-commandments

**Pros**
- Widget toolkits that may feel more familiar to GUI developers

**Cons**
- Smaller ecosystem than Textual
- Need to validate maintenance cadence and fit for a kanban board

### Option E — Blessed + custom rendering

**What it is**
- Terminal capability wrapper (cursor movement, colors, key reads).

**Pros**
- Very low-level control
- Good if you want to implement a minimal bespoke renderer

**Cons**
- You will reinvent widgets/layout/focus management

Reference: https://blessed.readthedocs.io/en/latest/api/terminal.html

## Recommendation

Use **Textual** unless you have a strong reason not to.

Suggested MVP scope for a Kanban TUI:
- 3 columns (TODO / DOING / DONE)
- list navigation (up/down), move card (left/right), open details (enter), quit (q)
- persistent storage in a simple file (JSON/CSV)

## Risks & Unknowns

- Terminal UI frameworks differ in licensing and dependency footprint; confirm constraints for your project.
- Mouse support and advanced interactions (drag/drop) can add complexity; prefer keyboard-first.
- If integrating with an existing CLI (like `tf`), decide whether the TUI is a separate command (`tf ui`) or a mode of an existing command.

## Next Steps

- Prototype a 3-column board using Textual and a tiny in-memory task model.
- Validate keybindings and performance on large lists.
- If needed, evaluate Urwid as a fallback (smaller surface area) before committing to a full framework.
