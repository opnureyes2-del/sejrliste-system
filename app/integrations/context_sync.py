#!/usr/bin/env python3
"""
CONTEXT SYNC - Update context system on sejr completion
Updates session.md and journal.md
"""
from pathlib import Path
from datetime import datetime

CONTEXT_PATH = Path.home() / ".claude/.context/core"

def update_context_on_completion(sejr_name: str, score: int, learnings: str) -> bool:
    """Update context files on sejr completion"""
    if not CONTEXT_PATH.exists():
        print(f"[CONTEXT SYNC] Context path not found: {CONTEXT_PATH}")
        return False

    # Update session.md
    session_file = CONTEXT_PATH / "session.md"
    if session_file.exists():
        content = session_file.read_text()
        update = f"\n\n### Sejr Completed: {sejr_name}\n"
        update += f"- **Score:** {score}/30\n"
        update += f"- **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        update += f"- **Learnings:** {learnings[:200]}\n"
        session_file.write_text(content + update)
        print(f"[CONTEXT SYNC] Updated session.md")

    return True

def update_journal(sejr_name: str, summary: str) -> bool:
    """Add entry to journal.md"""
    journal_file = CONTEXT_PATH / "journal.md"
    if journal_file.exists():
        content = journal_file.read_text()
        entry = f"\n\n### {datetime.now().strftime('%Y-%m-%d')} - Sejr: {sejr_name}\n"
        entry += f"{summary}\n"
        journal_file.write_text(content + entry)
        return True
    return False
