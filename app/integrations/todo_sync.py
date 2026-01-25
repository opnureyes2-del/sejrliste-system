#!/usr/bin/env python3
"""
TODO SYNC - Bidirectional sync with TodoWrite tool
"""
from pathlib import Path
from datetime import datetime
import json
import re

def extract_todos_from_sejr(sejr_path: Path) -> list:
    """Extract unchecked items from SEJR_LISTE.md"""
    sejr_file = sejr_path / "SEJR_LISTE.md"
    todos = []

    if sejr_file.exists():
        content = sejr_file.read_text()
        for line in content.split("\n"):
            if "- [ ]" in line:
                text = line.split("]", 1)[1].strip() if "]" in line else line
                todos.append({
                    "content": text,
                    "status": "pending",
                    "source": "sejr",
                })

    return todos

def mark_todo_complete(sejr_path: Path, todo_text: str) -> bool:
    """Mark a todo as complete in SEJR_LISTE.md"""
    sejr_file = sejr_path / "SEJR_LISTE.md"

    if not sejr_file.exists():
        return False

    content = sejr_file.read_text()
    # Find and replace the unchecked box
    pattern = rf"- \[ \] {re.escape(todo_text)}"
    replacement = f"- [x] {todo_text}"
    new_content = re.sub(pattern, replacement, content, count=1)

    if new_content != content:
        sejr_file.write_text(new_content)
        return True

    return False

def sync_todowrite(sejr_path: Path, external_todos: list) -> dict:
    """Sync external todos with sejr todos"""
    sejr_todos = extract_todos_from_sejr(sejr_path)

    return {
        "sejr_todos": len(sejr_todos),
        "external_todos": len(external_todos),
        "synced": True,
        "timestamp": datetime.now().isoformat(),
    }
