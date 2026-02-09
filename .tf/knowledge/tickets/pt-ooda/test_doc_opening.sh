#!/bin/bash
# Test script for TUI document opening feature
# Usage: ./test_doc_opening.sh [test-case]
# Ticket: pt-ooda

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_RESULTS="$SCRIPT_DIR/test_results.md"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

print_header() {
    echo ""
    echo "========================================"
    echo "  $1"
    echo "========================================"
    echo ""
}

check_prereqs() {
    print_header "Checking Prerequisites"
    
    # Check if tf is available
    if ! command -v tf &> /dev/null; then
        log_error "tf command not found in PATH"
        log_info "Make sure you're in the project virtual environment"
        exit 1
    fi
    log_info "tf CLI found: $(which tf)"
    
    # Check for knowledge directory
    if [ ! -d "$REPO_ROOT/.tf/knowledge/topics" ]; then
        log_error "Knowledge directory not found at $REPO_ROOT/.tf/knowledge/topics"
        exit 1
    fi
    log_info "Knowledge directory found"
    
    # Check for sample topic
    SAMPLE_TOPIC=$(find "$REPO_ROOT/.tf/knowledge/topics" -name "overview.md" | head -1)
    if [ -z "$SAMPLE_TOPIC" ]; then
        log_warn "No overview.md found in topics - some tests may fail"
    else
        log_info "Sample topic found: $(dirname "$SAMPLE_TOPIC")"
    fi
}

test_pager_less() {
    print_header "Test: PAGER=less"
    echo "Environment: PAGER=less"
    echo "Expected: Opens document with less pager"
    echo "Verification steps:"
    echo "  1. Run: PAGER=less tf ui"
    echo "  2. Select a topic with documents"
    echo "  3. Press 'o' or '1' to open overview"
    echo "  4. Verify less opens with the document"
    echo "  5. Press 'q' to exit less"
    echo "  6. Verify TUI is restored correctly"
    echo ""
    read -p "Press Enter when ready to perform this test..."
}

test_pager_more() {
    print_header "Test: PAGER=more"
    echo "Environment: PAGER=more"
    echo "Expected: Opens document with more pager"
    echo "Verification steps:"
    echo "  1. Run: PAGER=more tf ui"
    echo "  2. Select a topic with documents"
    echo "  3. Press 'o' or '1' to open overview"
    echo "  4. Verify more opens with the document"
    echo "  5. Press 'q' or space to exit more"
    echo "  6. Verify TUI is restored correctly"
    echo ""
    read -p "Press Enter when ready to perform this test..."
}

test_editor_vim() {
    print_header "Test: EDITOR=vim"
    echo "Environment: EDITOR=vim (no PAGER set)"
    echo "Expected: Opens document with vim editor"
    echo "Verification steps:"
    echo "  1. Run: EDITOR=vim PAGER= tf ui"
    echo "  2. Select a topic with documents"
    echo "  3. Press 'o' or '1' to open overview"
    echo "  4. Verify vim opens with the document"
    echo "  5. Type ':q' to exit vim"
    echo "  6. Verify TUI is restored correctly"
    echo ""
    read -p "Press Enter when ready to perform this test..."
}

test_editor_nano() {
    print_header "Test: EDITOR=nano"
    echo "Environment: EDITOR=nano (no PAGER set)"
    echo "Expected: Opens document with nano editor"
    echo "Verification steps:"
    echo "  1. Run: EDITOR=nano PAGER= tf ui"
    echo "  2. Select a topic with documents"
    echo "  3. Press 'o' or '1' to open overview"
    echo "  4. Verify nano opens with the document"
    echo "  5. Press Ctrl+X to exit nano"
    echo "  6. Verify TUI is restored correctly"
    echo ""
    read -p "Press Enter when ready to perform this test..."
}

test_fallback() {
    print_header "Test: Fallback (no PAGER or EDITOR)"
    echo "Environment: No PAGER or EDITOR set"
    echo "Expected: Uses fallback chain (less → more → cat)"
    echo "Verification steps:"
    echo "  1. Run: PAGER= EDITOR= tf ui"
    echo "  2. Select a topic with documents"
    echo "  3. Press 'o' or '1' to open overview"
    echo "  4. Verify a pager opens (likely less)"
    echo "  5. Exit the pager"
    echo "  6. Verify TUI is restored correctly"
    echo ""
    read -p "Press Enter when ready to perform this test..."
}

test_missing_document() {
    print_header "Test: Missing Document"
    echo "Scenario: Topic exists but document file is missing"
    echo "Expected: Shows notification 'document not found'"
    echo "Verification steps:"
    echo "  1. Create a topic entry pointing to non-existent file"
    echo "  2. Run: tf ui"
    echo "  3. Select the topic with missing doc"
    echo "  4. Press 'o' or '1' to open"
    echo "  5. Verify notification shows: 'document not found'"
    echo "  6. Verify TUI continues to work"
    echo ""
    read -p "Press Enter when ready to perform this test..."
}

test_no_topic_selected() {
    print_header "Test: No Topic Selected"
    echo "Scenario: User presses 'o' without selecting a topic"
    echo "Expected: Shows notification 'No topic selected'"
    echo "Verification steps:"
    echo "  1. Run: tf ui"
    echo "  2. Clear any topic selection (press Escape)"
    echo "  3. Press 'o' to open"
    echo "  4. Verify notification shows: 'No topic selected'"
    echo "  5. Verify TUI continues to work"
    echo ""
    read -p "Press Enter when ready to perform this test..."
}

test_all_keys() {
    print_header "Test: All Document Keys"
    echo "Keys to test: o, 1, 2, 3, 4"
    echo "Expected: Each key opens the corresponding document"
    echo "Verification steps:"
    echo "  1. Run: tf ui"
    echo "  2. Select a topic with all document types"
    echo "  3. Test each key:"
    echo "     - 'o' - opens first available"
    echo "     - '1' - opens overview"
    echo "     - '2' - opens sources"
    echo "     - '3' - opens plan"
    echo "     - '4' - opens backlog"
    echo "  4. Verify correct document opens for each key"
    echo "  5. Verify TUI restores after each"
    echo ""
    read -p "Press Enter when ready to perform this test..."
}

run_all_tests() {
    check_prereqs
    test_pager_less
    test_pager_more
    test_editor_vim
    test_editor_nano
    test_fallback
    test_missing_document
    test_no_topic_selected
    test_all_keys
    
    print_header "All Tests Completed"
    log_info "Remember to record results in test_results.md"
}

# Main
case "${1:-all}" in
    pager-less) test_pager_less ;;
    pager-more) test_pager_more ;;
    editor-vim) test_editor_vim ;;
    editor-nano) test_editor_nano ;;
    fallback) test_fallback ;;
    missing-doc) test_missing_document ;;
    no-topic) test_no_topic_selected ;;
    keys) test_all_keys ;;
    all) run_all_tests ;;
    *)
        echo "Usage: $0 [test-case]"
        echo ""
        echo "Test cases:"
        echo "  pager-less   - Test with PAGER=less"
        echo "  pager-more   - Test with PAGER=more"
        echo "  editor-vim   - Test with EDITOR=vim"
        echo "  editor-nano  - Test with EDITOR=nano"
        echo "  fallback     - Test with no PAGER/EDITOR"
        echo "  missing-doc  - Test missing document handling"
        echo "  no-topic     - Test no topic selected handling"
        echo "  keys         - Test all document keys (o, 1-4)"
        echo "  all          - Run all tests (default)"
        exit 1
        ;;
esac
