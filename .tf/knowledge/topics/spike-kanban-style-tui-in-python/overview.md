# spike-kanban-style-tui-in-python

Research spike: Python libraries suitable for building a **Kanban-style** terminal UI (multi-column board with interactive navigation, moving cards, filtering, etc.).

## Quick Answer

If you want a modern, full-screen, widget-based Kanban TUI in Python, **Textual** is the best default choice today (active ecosystem, rich widgets/layout, styling, and proven Kanban-like apps exist).

For a more “classic”/minimal approach or stricter dependency needs, consider **Urwid** (mature curses-style widgets) or **prompt_toolkit** (excellent input/keybindings + can build full-screen apps, but more DIY for layout).

## Recommended Starting Point

- Build the board with **Textual** (3 columns: TODO / DOING / DONE), model tasks as records, and implement move actions via keyboard shortcuts.
- Use an existing Textual Kanban app as inspiration (e.g. `kanban-cli`).
