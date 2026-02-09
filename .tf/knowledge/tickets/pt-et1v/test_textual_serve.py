#!/usr/bin/env python3
"""Test script to verify textual serve functionality and asset loading."""

import subprocess
import sys
import time
import urllib.request
from pathlib import Path


def test_textual_serve():
    """Test that textual serve works and serves the UI correctly."""
    print("Testing textual serve functionality...")
    
    # Start textual serve (use venv textual if available)
    textual_cmd = "/home/volker/coding/pi-ticketflow/.venv/bin/textual"
    if not Path(textual_cmd).exists():
        textual_cmd = "textual"
    
    proc = subprocess.Popen(
        [textual_cmd, "serve", "python -m tf_cli.ui"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test main page
        req = urllib.request.Request("http://localhost:8000")
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            
            # Check for key elements
            checks = [
                ("HTML structure", "<!DOCTYPE html>" in html),
                ("Textual CSS", "xterm.css" in html or "textual.css" in html),
                ("Textual JS", "textual.js" in html),
                ("WebSocket connection", "ws://" in html or "wss://" in html),
            ]
            
            print("\n=== UI Load Checks ===")
            all_passed = True
            for name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"{status} {name}")
                if not passed:
                    all_passed = False
            
            if all_passed:
                print("\n✅ All checks passed - UI loads correctly via textual serve")
            else:
                print("\n❌ Some checks failed")
                return False
                
        # Test static CSS file
        try:
            css_req = urllib.request.Request("http://localhost:8000/static/css/xterm.css")
            with urllib.request.urlopen(css_req, timeout=5) as response:
                css = response.read().decode('utf-8')
                if css and len(css) > 100:
                    print("✅ Static CSS file loads correctly")
                else:
                    print("⚠️ Static CSS file seems empty or small")
        except Exception as e:
            print(f"⚠️ Could not load static CSS: {e}")
            # This is not a failure - xterm.css might not be critical for the UI
            
    except Exception as e:
        print(f"❌ Failed to connect to textual serve: {e}")
        return False
    finally:
        # Cleanup
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    
    return True


def test_knowledge_dir_resolution():
    """Test that knowledge directory resolution works correctly."""
    print("\n=== Knowledge Directory Resolution ===")
    
    # Import and test the resolve function
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
    from tf_cli.ui import resolve_knowledge_dir
    
    kb_dir = resolve_knowledge_dir()
    print(f"Resolved knowledge directory: {kb_dir}")
    
    if kb_dir.exists():
        print("✅ Knowledge directory exists")
        
        # Check for topics
        topics_dir = kb_dir / "topics"
        if topics_dir.exists():
            topic_count = len(list(topics_dir.iterdir()))
            print(f"✅ Topics directory exists with {topic_count} topics")
        else:
            print("⚠️ Topics directory not found")
            
        # Check for tickets  
        tickets_dir = kb_dir / "tickets"
        if tickets_dir.exists():
            ticket_count = len([d for d in tickets_dir.iterdir() if d.is_dir()])
            print(f"✅ Tickets directory exists with {ticket_count} tickets")
        else:
            print("⚠️ Tickets directory not found")
    else:
        print(f"❌ Knowledge directory does not exist: {kb_dir}")
        return False
    
    return True


def main():
    print("=" * 60)
    print("Textual Serve Audit Test")
    print("=" * 60)
    
    # Test 1: Knowledge directory resolution
    kb_ok = test_knowledge_dir_resolution()
    
    # Test 2: Textual serve functionality
    serve_ok = test_textual_serve()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Knowledge directory resolution: {'✅ PASS' if kb_ok else '❌ FAIL'}")
    print(f"Textual serve functionality: {'✅ PASS' if serve_ok else '❌ FAIL'}")
    
    if kb_ok and serve_ok:
        print("\n✅ All tests passed - textual serve works correctly")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
