# Research: ptw-azum

## Status
Research step skipped per workflow configuration (`enableResearcher: false`).

## Context Reviewed
- `tk show ptw-azum` - Ticket details for component classifier
- `.tf/knowledge/topics/seed-backlog-deps-and-tags/` - Seed topic with MVP scope
- Existing codebase in `tf_cli/` directory

## Design Decisions
Based on seed documentation and ticket requirements:
- Simple keyword mapping approach (not ML)
- 7 standard components: cli, api, docs, tests, config, workflow, agents
- Conservative matching (explicit keywords only)
- Extensible via custom_keywords parameter
