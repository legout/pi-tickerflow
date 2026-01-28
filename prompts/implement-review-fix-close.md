---
description: Full workflow - implement ticket, review with fresh eyes, fix issues, and close. Use --auto/--no-clarify for non-interactive mode.
---

# Implement → Review → Fix → Close Workflow

Execute the complete ticket implementation workflow using the `subagent` chain tool.

## Invocation arguments (IMPORTANT)

This prompt template is invoked as:

```
/implement-review-fix-close <ticket-id> [flags...]
```

Pi passes the arguments to this template as:

- First arg: `$1`
- All args (space-joined): `$@`

Use **`$@` as the raw task input** for parsing ticket + flags.

If `$1` is empty (no args provided), ask the user for the ticket ID (and optional flags) and stop.

## Workflow Config (optional)

Look for workflow config files (project overrides global):
- `.pi/workflows/implement-review-fix-close/config.json` (project)
- `~/.pi/agent/workflows/implement-review-fix-close/config.json` (global)

If present, merge them with project settings taking precedence.

Use config values if provided:
- `workflow.clarifyDefault`: default clarify value when no flags are passed (fallback: true)
- `workflow.enableResearcher`: enable/disable research step (default true)
- `workflow.knowledgeDir`: knowledge directory for research (default `.pi/knowledge`)
- `workflow.enableReviewers`: list of reviewer agent names for parallel review step (fallback: reviewer-general, reviewer-spec-audit, reviewer-second-opinion)
- `workflow.enableFixer`: include/exclude fixer step (default true)
- `workflow.enableCloser`: include/exclude closer step (default true)
- `workflow.researchParallelAgents`: minimum parallel research agents when fetching (default 3)

If you update model settings in the config, run `/irfc-sync` to apply models to agent files.

## Parse Task Flags

From `$@` determine flags:

- `--auto` or `--no-clarify` → set `clarify: false` (headless mode)
- `--simplify-tickets` → after closing the ticket, run: `/simplify --create-tickets --last-implementation`
- `--final-review-loop` → after the chain completes, start review loop: `/review-start`
- `--with-research` → force enable research step
- `--no-research` → force disable research step
- No flags → set `clarify` to `workflow.clarifyDefault` if configured, otherwise `true`

Determine `{ticket}`:

- Prefer `$1` as the ticket ID.
- If `$1` does not look like a ticket ID, scan `$@` for the first token matching `mme-...`.
- Strip/remove flags from the ticket string.

## Chain Execution

Use the subagent tool with a single chain. The fixer will **no-op** if there are no Critical/Major/Minor issues, effectively skipping itself while still producing a `fixes.md` stub for downstream steps.

### Step 0: Research (optional)
- **Agent**: `researcher`
- **Task**: `{ticket}`
- **Output**: `research.md`
- **Note**: Skip if `workflow.enableResearcher` is `false` or `--no-research` is set

### Step 1: Implement
- **Agent**: `implementer`
- **Task**: `{ticket}`
- **Output**: `implementation.md`
- **Progress**: Enabled

### Step 2: Parallel Reviews
Run reviewers in parallel (use `workflow.enableReviewers` if configured; default below):
- **General review**: `reviewer-general` → `review-general.md`
- **Spec audit**: `reviewer-spec-audit` → `review-spec.md`
- **Second opinion**: `reviewer-second-opinion` → `review-second.md`

### Step 3: Merge Reviews
- **Agent**: `review-merge`
- **Task**: `Merge review outputs for {ticket}`
- **Reads**: the three parallel review outputs
- **Output**: `review.md`

### Step 4: Fix (conditional no-op)
- **Agent**: `fixer`
- **Task**: `Fix Critical/Major/Minor issues for {ticket} from review`
- **Output**: `fixes.md`
- **Note**: If there are no Critical/Major/Minor issues, write `fixes.md` with "No fixes needed" and make no code changes. Skip Warnings/Suggestions (follow-up tickets).

### Step 5: Close
- **Agent**: `closer`
- **Task**: `Add summary comment and close ticket {ticket}`
- **Output**: `close-summary.md`
- **Note**: Skip this step if `workflow.enableCloser` is `false`

## Chain Configuration

When you call `subagent`, replace:

- `{ticket}` with the parsed ticket id
- `{determine_from_flags}` with the computed boolean for `clarify`

If `workflow.enableReviewers` is set, build the `parallel` array from that list and update the `review-merge.reads` list to match the generated review outputs. If the research step is omitted, adjust the `parallel-*` path prefix accordingly.

```json
{
  "chain": [
    {
      "agent": "researcher",
      "task": "{ticket}",
      "output": "research.md"
    },
    {
      "agent": "implementer",
      "task": "{ticket}",
      "output": "implementation.md",
      "progress": true
    },
    {
      "parallel": [
        {
          "agent": "reviewer-general",
          "task": "Review implementation for {ticket} with fresh eyes",
          "output": "review-general.md"
        },
        {
          "agent": "reviewer-spec-audit",
          "task": "Spec audit for {ticket}",
          "output": "review-spec.md"
        },
        {
          "agent": "reviewer-second-opinion",
          "task": "Second-opinion review for {ticket}",
          "output": "review-second.md"
        }
      ]
    },
    {
      "agent": "review-merge",
      "task": "Merge review outputs for {ticket}",
      "reads": [
        "parallel-2/0-reviewer-general/review-general.md",
        "parallel-2/1-reviewer-spec-audit/review-spec.md",
        "parallel-2/2-reviewer-second-opinion/review-second.md"
      ],
      "output": "review.md"
    },
    {
      "agent": "fixer",
      "task": "Fix Critical/Major/Minor issues for {ticket} from review (no-op if none)",
      "output": "fixes.md"
    },
    {
      "agent": "closer",
      "task": "Add summary comment and close ticket {ticket}",
      "output": "close-summary.md"
    }
  ],
  "clarify": "{determine_from_flags}"
}
```

If `workflow.enableFixer` is `false`, omit the fixer step. If `workflow.enableCloser` is `false`, omit the close step.

## Optional Post-Chain Steps

After the chain completes:

- If `--simplify-tickets` was set: run `/simplify --create-tickets --last-implementation`
- If `--final-review-loop` was set: run `/review-start`
