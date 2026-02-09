# Research: pt-bsuf

## Status
Research completed. Pico.css classless variant identified and documented.

## Findings

### Pico.css Classless CDN (Pinned)
```html
<!-- Centered viewport (good for our use case) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">

<!-- Fluid viewport (full-width) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.fluid.classless.min.css">
```

### Key Characteristics
- **Classless variant**: Styles semantic HTML elements without requiring CSS classes
- **Semantic containers**: `<header>`, `<main>`, `<footer>` inside `<body>` automatically act as containers
- **Major version pinned**: `@2` allows minor/patch updates but not breaking changes
- **CDN**: jsDelivr provides reliable hosting with version pinning

### Current State Analysis

**base.html** contains:
1. Datastar CDN (keep)
2. Custom CSS for:
   - Reset styles (* box-sizing)
   - Body typography
   - Header styling (dark blue background #2c3e50)
   - Navigation styling
   - Button classes (.btn, .btn-secondary)
   - Priority badges (.priority-p0 through .priority-pnone)
   - Status indicators (.status-open, .status-closed, .status-blocked)

**Dependent templates**:
- `_board.html` - Kanban board with ticket cards, columns
- `ticket.html` - Ticket detail page with custom styling
- `topics.html`, `topic_detail.html`, `_topics_list.html` - Topic pages
- `index.html` - Main page

### Integration Strategy
1. Add Pico.css classless CDN link BEFORE custom styles
2. Keep custom CSS but reduce/scope to avoid conflicts:
   - Keep priority badge colors (Pico doesn't provide these semantics)
   - Keep status indicators (custom semantic meaning)
   - Keep board/card layout styles (Pico classless doesn't provide Kanban layouts)
   - Remove basic typography resets (handled by Pico)
3. Verify board and ticket pages render correctly

## Sources
- https://picocss.com/docs/classless - Pico classless documentation
- https://picocss.com/docs - General Pico documentation
