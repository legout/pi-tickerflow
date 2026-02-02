# pi-tk-workflow

A comprehensive Pi workflow package for ticket-based development using the **Implement → Review → Fix → Close** cycle.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Implement│ → │  Review  │ → │   Fix    │ → │  Close   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

**Features:** Planning → Research → Ticket Creation → Implementation → Review → Autonomous Processing

---

## Installation

### Prerequisites

- [Pi](https://github.com/mariozechner/pi) installed and configured
- `tk` CLI in your PATH (ticket management)
- Language tools for your project

### Required Pi Extensions

```bash
pi install npm:pi-prompt-template-model  # Entry model switch via frontmatter
pi install npm:pi-model-switch           # Runtime model switching
pi install npm:pi-subagents              # Parallel reviewer subagents
```

### Interactive Setup (Recommended)

```bash
./bin/irf setup
```

This guides you through global vs project install, optional extensions, and MCP configuration.

### Manual Install

```bash
# Global install (recommended)
./install.sh --global

# Project install
./install.sh --project /path/to/project
```

Files are installed to:
- **Global**: `~/.pi/agent/{agents,skills,prompts,workflows}/`
- **Project**: `.pi/{agents,skills,prompts,workflows}/`

---

## Quick Start

### 1. Capture an Idea

```bash
/irf-seed "Build a CLI tool for managing database migrations"
```

Creates structured artifacts in `.pi/knowledge/topics/seed-build-a-cli/`.

### 2. Create Tickets

```bash
/irf-backlog seed-build-a-cli
```

Generates 5-15 small, actionable tickets (1-2 hours each) linked to your seed.

### 3. Run the IRF Workflow

```
/irf TICKET-123
```

Executes the full cycle: Research → Implement → Review → Fix → Close.

### 4. Run Autonomously (Optional)

```
/ralph-start --max-iterations 10
```

Processes tickets in a loop until backlog is empty.

---

## Workflows

### Greenfield Development

```
/irf-seed "Your idea" → /irf-backlog seed-* → /irf <ticket>
```

### Brownfield Development

```
/irf-baseline [focus] → /irf-backlog baseline-* → /irf <ticket>
```

### Structured Planning

```
/irf-plan "Feature description" → /irf-plan-consult → /irf-plan-revise → /irf-plan-review → /irf-backlog plan-*
```

### Research First

```
/irf-spike "Technical topic" [--parallel] → /irf-seed → /irf-backlog → /irf <ticket>
```

---

## Commands Overview

### Implementation

| Command | Purpose |
|---------|---------|
| `/irf <ticket>` | Execute IRF workflow on a ticket |
| `/ralph-start` | Start autonomous processing loop |

### Planning & Design

| Command | Purpose |
|---------|---------|
| `/irf-plan <request>` | Create implementation plan |
| `/irf-plan-consult <plan>` | Gap detection and edits |
| `/irf-plan-revise <plan>` | Apply feedback to plan |
| `/irf-plan-review <plan>` | Validate plan (high-accuracy) |

### Research & Discovery

| Command | Purpose |
|---------|---------|
| `/irf-seed <idea>` | Capture idea into structured artifacts |
| `/irf-spike <topic>` | Research spike (sequential or parallel) |
| `/irf-baseline [focus]` | Capture project baseline/status-quo |

### Ticket Creation

| Command | Purpose |
|---------|---------|
| `/irf-backlog <topic>` | Create tickets from seed/baseline/plan |
| `/irf-backlog-ls [topic]` | List backlog status and tickets |
| `/irf-followups <review>` | Create tickets from review warnings |
| `/irf-from-openspec <change>` | Create tickets from OpenSpec |

### Configuration

| Command | Purpose |
|---------|---------|
| `/irf-sync` | Sync models from config to agents |

See [docs/commands.md](docs/commands.md) for complete reference with all flags.

---

## Architecture

This package uses a **skill-centric** architecture:

```
skills/              # Domain expertise (reusable)
  irf-workflow/      # Core implementation workflow
  irf-planning/      # Research & planning activities
  irf-config/        # Setup & configuration
  ralph/             # Autonomous loop orchestration

prompts/             # Command entry points (thin wrappers)
  irf.md             # References irf-workflow skill
  irf-seed.md        # References irf-planning skill
  ...

agents/              # Subagent execution units
  implementer.md
  reviewer-*.md
  fixer.md
  closer.md
```

When you type a command:
1. Extension reads `model:` and `skill:` frontmatter
2. Switches to specified model
3. Injects skill content into context
4. Executes command

See [docs/architecture.md](docs/architecture.md) for details.

---

## Knowledge Base

All planning and research artifacts are stored in `.pi/knowledge/`:

```
.pi/knowledge/
├── index.json                    # Registry of all topics
├── tickets/
│   └── {ticket-id}.md           # Per-ticket research
└── topics/
    └── {topic-id}/
        ├── overview.md           # Summary + keywords
        ├── sources.md            # References and URLs
        ├── seed.md               # Greenfield ideas
        ├── baseline.md           # Brownfield analysis
        ├── plan.md               # Implementation plans
        ├── spike.md              # Research findings
        ├── backlog.md            # Generated tickets
        ├── mvp-scope.md          # What's in/out
        ├── risk-map.md           # Technical risks
        ├── test-inventory.md     # Test coverage
        └── dependency-map.md     # External dependencies
```

Topics are automatically linked to tickets via `external-ref`.

---

## Configuration

Models are configured in `workflows/implement-review-fix-close/config.json`:

```json
{
  "models": {
    "implementer": "chutes/moonshotai/Kimi-K2.5-TEE:high",
    "reviewer": "openai-codex/gpt-5.1-codex-mini",
    "fixer": "zai/glm-4.7"
  }
}
```

Apply changes with:

```bash
./bin/irf sync
# or
/irf-sync
```

See [docs/configuration.md](docs/configuration.md) for full setup options.

---

## Ralph Loop (Autonomous Processing)

Ralph enables autonomous ticket processing with:

- **Re-anchoring**: Fresh context per ticket
- **Lessons Learned**: Persistent wisdom in `.pi/ralph/AGENTS.md`
- **Progress Tracking**: External state survives resets

```bash
# Initialize Ralph directory
./bin/irf ralph init

# Start loop
/ralph-start --max-iterations 50

# Check status
./bin/irf ralph status
```

See [docs/ralph.md](docs/ralph.md) for the complete guide.

---

## Project Structure

```
pi-tk-workflow/
├── agents/                 # Subagent definitions
├── skills/                 # Domain expertise
├── prompts/                # Command entry points
├── workflows/              # Workflow configurations
├── bin/irf                 # CLI tool
├── install.sh              # Installation script
└── docs/                   # Documentation
```

---

## Documentation

- **[docs/commands.md](docs/commands.md)** - Complete command reference
- **[docs/architecture.md](docs/architecture.md)** - How it works
- **[docs/ralph.md](docs/ralph.md)** - Autonomous processing
- **[docs/configuration.md](docs/configuration.md)** - Setup and models
- **[docs/workflows.md](docs/workflows.md)** - Detailed workflow guides
