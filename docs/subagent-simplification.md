# IRF Workflow Simplification: Subagent Analysis

## Problem Statement

The current IRF workflows use many subagents, which introduces fragility:
- Each subagent spawn is a potential failure point
- Nested subagents (e.g., prompt → irf-planner → researcher-fetch ×3) compound the risk
- Many subagents exist only to use a different model, not for parallelism

## Key Insight

**Subagents provide two benefits:**
1. **Parallelism** - run multiple tasks simultaneously (irreplaceable)
2. **Isolation** - separate context/working directory

**If we only need a different model**, `pi-model-switch` is strictly better:
- Faster (no spawn overhead)
- More reliable (no IPC failures)
- Shared context (no file passing needed)

---

## Part 1: Implementation Workflow (`/irf`)

### Analysis

| Step | Current | Why Subagent? | Verdict |
|------|---------|---------------|---------|
| researcher | Subagent spawning 3 sub-subagents | Parallel MCP fetches | **Replace** - Sequential is acceptable |
| implementer | Subagent | Different model | **Replace** - Use model-switch |
| reviewer-general | Subagent (parallel) | **True parallelism** | **Keep** |
| reviewer-spec-audit | Subagent (parallel) | **True parallelism** | **Keep** |
| reviewer-second-opinion | Subagent (parallel) | **True parallelism** | **Keep** |
| review-merge | Subagent | Different model | **Replace** - Use model-switch |
| fixer | Subagent | Different model | **Replace** - Use model-switch |
| closer | Subagent | Different model | **Replace** - Use model-switch |

### Solution: `/irf` (Model-Switch Workflow)

- Uses `pi-model-switch` for sequential model changes
- Keeps subagents **only** for parallel reviews (3 subagents)
- Reduces subagent spawns from 6-8 to 3
- Cuts failure points by ~60%
- Legacy full-subagent workflow has been removed; `/irf-lite` is now a deprecated alias

---

## Part 2: Planning Workflows

### Analysis

| Command | Current Flow | Uses Parallelism? | Subagent Necessary? |
|---------|--------------|-------------------|---------------------|
| `/irf-seed` | prompt → irf-planner | **No** | **No** |
| `/irf-backlog` | prompt → irf-planner | **No** | **No** |
| `/irf-baseline` | prompt → irf-planner | **No** | **No** |
| `/irf-followups` | prompt → irf-planner | **No** | **No** |
| `/irf-from-openspec` | prompt → irf-planner | **No** | **No** |
| `/irf-spike` | prompt → irf-planner → 3× researcher-fetch | **Yes** (nested) | **Partially** |

### Key Finding: `irf-planner` is a "God Agent" Anti-Pattern

The `irf-planner` agent handles 6 different modes via a mode prefix. This design:
- Forces a subagent spawn just to route to the right behavior
- The subagent exists only to use a different model
- All logic could be in the prompt template with model-switch

### Solution: Inline Planning Prompts

| Command | Subagents Before | Subagents After |
|---------|------------------|-----------------|
| `/irf-seed` | 1 | 0 |
| `/irf-backlog` | 1 | 0 |
| `/irf-baseline` | 1 | 0 |
| `/irf-followups` | 1 | 0 |
| `/irf-from-openspec` | 1 | 0 |
| `/irf-spike` | 4 | 0 (or 3 with `--parallel`) |

**Total planning workflow reduction:** 9 subagents → 0-3 subagents (planning prompts run inline)

---

## Summary: Total Subagent Reduction

### Implementation Workflow

| Workflow | Subagent Spawns |
|----------|-----------------|
| `/irf` (model-switch) | 3 (parallel reviews only) |
| `/irf-lite` (deprecated alias) | 3 (parallel reviews only) |

### Planning Workflows

| Workflow | Original | Current |
|----------|----------|---------|
| `/irf-seed` | 1 | 0 |
| `/irf-backlog` | 1 | 0 |
| `/irf-baseline` | 1 | 0 |
| `/irf-followups` | 1 | 0 |
| `/irf-from-openspec` | 1 | 0 |
| `/irf-spike` | 4 | 0-3 |

### Grand Total

| Scenario | Max Subagent Spawns |
|----------|---------------------|
| Original workflows | 14-17 |
| Current workflows | 3-6 |
| **Reduction** | **~70-80%** |

---

## Files Created

### Implementation
- `prompts/irf.md` - Standard model-switch workflow
- `prompts/irf-lite.md` - Deprecated alias for `/irf`

### Planning
- `prompts/irf-seed.md`
- `prompts/irf-backlog.md`
- `prompts/irf-baseline.md`
- `prompts/irf-followups.md`
- `prompts/irf-from-openspec.md`
- `prompts/irf-spike.md`

### Config
- `config/model-aliases.json` - Example aliases for pi-model-switch

---

## Extension Requirements

### For Planning Workflows (Recommended)

```bash
pi install npm:pi-subagents      # For parallel reviews only
pi install npm:pi-model-switch   # For on-the-fly model switching
pi install npm:pi-mcp-adapter    # Optional, for research MCP tools
```

**Finding:** `pi-interactive-shell` is NOT used anywhere in the workflow. It can be removed from requirements.

---

## Migration Path

1. **Test `pi-model-switch`** - Verify it works as expected in your environment
2. **Use `/irf`** - Standard model-switch workflow for implementation tickets
3. **Update scripts** - Replace `/irf-lite` calls with `/irf` (alias remains but is deprecated)
4. **Remove legacy references** - Drop old subagent workflow assumptions

