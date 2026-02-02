# Workflow Guides

Step-by-step guides for common development scenarios.

---

## Greenfield Development

Starting a new project or feature from scratch.

### 1. Capture Your Idea

```
/irf-seed "Build a CLI tool for managing database migrations"
```

This creates structured artifacts in `.pi/knowledge/topics/seed-build-a-cli/`:
- `seed.md` - Your vision and core concept
- `mvp-scope.md` - What's in/out of the first version
- `success-metrics.md` - How you'll measure success
- `assumptions.md` - What you're assuming
- `constraints.md` - Limitations to work within

### 2. (Optional) Research First

If you need to research technical approaches:

```
/irf-spike "Database migration tools in Python"
```

Creates `.pi/knowledge/topics/spike-database-migration-tools/` with:
- `spike.md` - Analysis of options with recommendations
- `sources.md` - URLs and references

### 3. Create Tickets

```
/irf-backlog seed-build-a-cli
```

Generates 5-15 small tickets in `tk`, each:
- 30 lines or less
- 1-2 hours of work
- Self-contained with context from seed
- Linked via `external-ref`

### 4. Implement

```
/irf TICKET-123
```

Runs the full IRF cycle on each ticket.

### 5. Autonomous Processing (Optional)

```
/ralph-start --max-iterations 20
```

Processes remaining tickets automatically.

---

## Brownfield Development

Working with an existing codebase.

### 1. Capture Baseline

Document the current state before making changes:

```
/irf-baseline
```

Or focus on a specific area:

```
/irf-baseline "authentication system"
```

Creates `.pi/knowledge/topics/baseline-myapp/` with:
- `baseline.md` - Architecture and components
- `risk-map.md` - Technical risks and fragile areas
- `test-inventory.md` - Test coverage gaps
- `dependency-map.md` - External dependencies

### 2. Create Improvement Tickets

```
/irf-backlog baseline-myapp
```

Generates tickets from:
- Risk map items (high priority)
- Test coverage gaps
- Dependency issues
- Architectural hotspots

### 3. Implement

```
/irf TICKET-123
```

Each ticket includes baseline context so you understand the existing code.

---

## Structured Planning

For complex features requiring careful design.

### 1. Create Initial Plan

```
/irf-plan "Refactor auth flow to support OAuth + magic links"
```

Creates `.pi/knowledge/topics/plan-auth-refactor/plan.md` with:
- Summary and requirements
- Constraints and assumptions
- Risks and gaps
- Work plan with phases
- Acceptance criteria

Status: `draft`

### 2. Consult for Gaps

```
/irf-plan-consult plan-auth-refactor
```

Identifies:
- Missing requirements
- Ambiguous specifications
- Over-engineering
- Hidden risks

Updates plan.md with Consultant Notes. Status: `consulted`

### 3. Revise Based on Feedback

```
/irf-plan-revise plan-auth-refactor
```

Applies changes to address consultant findings.

Status: `revised`

### 4. High-Accuracy Review

```
/irf-plan-review plan-auth-refactor --high-accuracy
```

Validates:
- Completeness of requirements
- Clear scope boundaries
- Feasible work plan
- Testable acceptance criteria

Status: `approved` or `blocked`

### 5. Create Tickets

Only proceed if plan is approved:

```
/irf-backlog plan-auth-refactor
```

Generates tickets from the work plan, each referencing the approved plan.

### 6. Implement

```
/irf TICKET-123
```

---

## Research-Driven Development

When you need to evaluate options before deciding.

### 1. Research Spike

```
/irf-spike "React Server Components vs Next.js App Router" --parallel
```

Uses parallel subagents for faster research. Creates:
- `overview.md` - Quick summary
- `spike.md` - Detailed analysis with pros/cons/recommendations

### 2. Capture Decision as Seed

```
/irf-seed "Migrate to Next.js App Router based on spike findings"
```

References the spike in your seed.

### 3. Create and Implement Tickets

```
/irf-backlog seed-migrate-nextjs
/irf TICKET-123
```

---

## Review-Driven Improvements

Addressing issues found during code review.

### 1. Normal Implementation

```
/irf TICKET-123
```

Produces `review.md` with findings.

### 2. Create Follow-up Tickets

For warnings and suggestions that are out of scope:

```
/irf-followups ./review.md
```

Creates tickets tagged with `followup` and priority 3 (lower than implementation).

### 3. Process Follow-ups

```
/irf FOLLOWUP-456
```

---

## OpenSpec Integration

Working with external specifications.

### 1. Create Tickets from OpenSpec

```
/irf-from-openspec auth-pkce-support
```

Reads from `openspec/changes/auth-pkce-support/`:
- `tasks.md` for task list
- `proposal.md` and `design.md` for context

Creates tickets tagged with `openspec` and linked to the change.

### 2. Implement

```
/irf TICKET-123
```

Each ticket includes relevant technical details from the OpenSpec.

---

## Autonomous Processing with Ralph

Running batches of tickets without manual intervention.

### 1. Initialize Ralph

```bash
./bin/irf ralph init
```

Creates `.pi/ralph/` directory with:
- `AGENTS.md` - Lessons learned
- `progress.md` - Loop state
- `config.json` - Configuration

### 2. (Optional) Prime with Known Patterns

Edit `.pi/ralph/AGENTS.md`:

```markdown
## Gotchas
- Always use safeParse() for user input
- The cache module needs explicit TTL

## Patterns
- Use the Result type for error handling
```

### 3. Start the Loop

```
/ralph-start --max-iterations 20
```

Or with CLI:

```bash
./bin/irf ralph init
# Then in pi:
/ralph-start
```

### 4. Monitor Progress

```bash
./bin/irf ralph status
./bin/irf ralph lessons
```

### 5. Review and Prune

```bash
# Remove outdated lessons
./bin/irf ralph lessons prune 30
```

---

## Ticket Guidelines

All ticket creation follows these principles:

| Attribute | Target |
|-----------|--------|
| Description | 30 lines or less |
| Work time | 1-2 hours |
| Context | Self-contained (no need to load planning docs) |
| Scope | Single responsibility |
| Linking | Via `external-ref` to source topic |

---

## Knowledge Base Organization

```
.pi/knowledge/
├── index.json                    # Registry
├── tickets/
│   └── TICKET-123.md            # Per-ticket research
└── topics/
    ├── seed-my-feature/         # Greenfield ideas
    ├── baseline-myapp/          # Brownfield analysis
    ├── plan-auth-refactor/      # Structured plans
    └── spike-technology/        # Research findings
```

Topics are automatically created and linked. You rarely need to manage them manually.
