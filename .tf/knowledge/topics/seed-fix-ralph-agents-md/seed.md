# Seed: Fix Ralph AGENTS.md Lessons Learned

## Vision

The Ralph loop is designed to capture and persist lessons learned across ticket processing iterations, storing them in `.tf/ralph/AGENTS.md`. However, due to implementation bugs, this feature is completely non-functional - lessons are extracted but never persisted, and the file is never read during re-anchoring.

## Core Concept

Fix three related issues in `tf_cli/ralph.py`:

1. **Missing file creation**: `AGENTS.md` is never created during Ralph initialization
2. **Conditional write bug**: `update_state()` only writes lessons if `AGENTS.md` already exists (chicken-egg problem)
3. **Missing read during re-anchoring**: Lessons are never injected into the workflow context as documented

The fix ensures lessons are:
- Created with a default template when first needed
- Written after each completed ticket
- (Optional) Read and injected during re-anchoring

## Key Features

1. Create AGENTS.md with default template on first lesson
2. Remove the `.exists()` guard that prevents lesson persistence
3. Add defensive file creation with proper template
4. (Future) Read and inject lessons during re-anchoring phase

## Open Questions

- Should we also fix the re-anchoring read, or just the write path?
- What is the priority: minimal fix vs. complete feature implementation?
