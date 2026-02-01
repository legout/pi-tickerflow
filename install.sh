#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./install.sh --global
  ./install.sh --project /path/to/project

Options:
  --global              Install into ~/.pi/agent
  --project <path>      Install into <path>/.pi
  --help                Show this help

Notes:
  This script copies agents, skills, prompts, and workflow config.
  Use ./bin/irf setup for interactive setup (extensions + MCP).
EOF
}

if [ "$#" -eq 0 ]; then
  usage
  exit 1
fi

TARGET_BASE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --global)
      TARGET_BASE="$HOME/.pi/agent"
      shift
      ;;
    --project)
      if [ -z "${2:-}" ]; then
        echo "Missing path after --project" >&2
        exit 1
      fi
      TARGET_BASE="$2/.pi"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
 done

if [ -z "$TARGET_BASE" ]; then
  echo "No target specified." >&2
  usage
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MANIFEST="$SCRIPT_DIR/config/install-manifest.txt"

if [ ! -f "$MANIFEST" ]; then
  echo "Install manifest not found: $MANIFEST" >&2
  exit 1
fi

agents_count=0
skills_count=0
prompts_count=0
workflows_count=0

while IFS= read -r line || [ -n "$line" ]; do
  line="$(printf '%s' "$line" | sed -e 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  if [ -z "$line" ] || [[ "$line" == \#* ]]; then
    continue
  fi
  if [ ! -f "$SCRIPT_DIR/$line" ]; then
    echo "Missing install file: $SCRIPT_DIR/$line" >&2
    exit 1
  fi
  mkdir -p "$TARGET_BASE/$(dirname "$line")"
  cp "$SCRIPT_DIR/$line" "$TARGET_BASE/$line"
  case "$line" in
    agents/*) agents_count=$((agents_count + 1)) ;;
    skills/*) skills_count=$((skills_count + 1)) ;;
    prompts/*) prompts_count=$((prompts_count + 1)) ;;
    workflows/*) workflows_count=$((workflows_count + 1)) ;;
  esac
 done < "$MANIFEST"

# Create root AGENTS.md if it doesn't exist (for --project installs)
if [ -f "$SCRIPT_DIR/docs/AGENTS.md.template" ] && [ ! -f "AGENTS.md" ]; then
  if [[ "$TARGET_BASE" != "$HOME/.pi/agent" ]]; then
    cp "$SCRIPT_DIR/docs/AGENTS.md.template" "AGENTS.md"
    echo "Created AGENTS.md in project root"
  fi
fi

echo "Installed IRF workflow files to: $TARGET_BASE"
echo ""
echo "Installed components:"
echo "  - $agents_count agents (execution units)"
echo "  - $skills_count skills (domain expertise)"
echo "  - $prompts_count prompts (command entry points)"
echo "  - $workflows_count workflow files"
echo ""
echo "Next steps:"
echo "  1. Review AGENTS.md (project patterns)"
echo "  2. Initialize Ralph: ./bin/irf ralph init"
echo "  3. Start working: /irf <ticket>"
