#!/usr/bin/env python3
"""
TodoWrite Synchronization for Sejrliste Visual System.

Provides bi-directional sync between sejr checkboxes and TodoWrite:
- Convert sejr checkboxes to TodoWrite format
- Update TodoWrite when sejr progress changes
- Track phase completion

PASS 2 Feature: TodoWrite sync integration.
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class TodoSync:
    """
    Synchronize sejr checkboxes with TodoWrite tool.

    Features:
    - Extract todos from SEJR_LISTE.md
    - Convert to TodoWrite format
    - Track completion status
    - Bi-directional sync (planned)
    """

    def __init__(self, system_path: Path):
        """
        Initialize TodoSync.

        Args:
            system_path: Path to sejrliste system folder
        """
        self.system_path = system_path
        self.active_dir = system_path / "10_ACTIVE"

    def extract_todos_from_sejr(self, sejr_path: Path) -> List[Dict[str, Any]]:
        """
        Extract todos from SEJR_LISTE.md.

        Args:
            sejr_path: Path to sejr folder

        Returns:
            List of todo dictionaries
        """
        sejr_file = sejr_path / "SEJR_LISTE.md"
        if not sejr_file.exists():
            return []

        todos = []
        content = sejr_file.read_text()

        # Find all checkboxes
        checkbox_pattern = r'- \[([ xX])\] (.+)'
        for match in re.finditer(checkbox_pattern, content):
            is_done = match.group(1).lower() == 'x'
            text = match.group(2).strip()

            # Determine status
            status = "completed" if is_done else "pending"

            todos.append({
                "content": text[:80],  # Truncate long items
                "status": status,
                "activeForm": text[:50] + "..." if len(text) > 50 else text,
            })

        return todos

    def get_current_phase(self, sejr_path: Path) -> Dict[str, Any]:
        """
        Get current phase from sejr.

        Args:
            sejr_path: Path to sejr folder

        Returns:
            Phase information dictionary
        """
        status_file = sejr_path / "STATUS.yaml"
        if not status_file.exists():
            return {"phase": "PHASE 0", "pass": 1}

        # Simple YAML parse
        try:
            content = status_file.read_text()
            current_pass = 1
            for line in content.split("\n"):
                if "current_pass:" in line:
                    current_pass = int(line.split(":")[1].strip())

            return {
                "phase": f"PHASE {current_pass - 1}" if current_pass > 1 else "PHASE 0",
                "pass": current_pass,
            }
        except:
            return {"phase": "PHASE 0", "pass": 1}

    def get_phase_todos(self, sejr_path: Path) -> List[Dict[str, Any]]:
        """
        Get todos for current phase only.

        Args:
            sejr_path: Path to sejr folder

        Returns:
            List of phase-specific todos
        """
        sejr_file = sejr_path / "SEJR_LISTE.md"
        if not sejr_file.exists():
            return []

        content = sejr_file.read_text()
        phase_info = self.get_current_phase(sejr_path)
        current_pass = phase_info["pass"]

        # Find section for current pass
        todos = []
        in_current_pass = False
        pass_markers = {
            1: "# 🥉 PASS 1:",
            2: "# 🥈 PASS 2:",
            3: "# 🥇 PASS 3:",
        }
        current_marker = pass_markers.get(current_pass, "# 🥉 PASS 1:")

        for line in content.split("\n"):
            # Check if we entered current pass section
            if current_marker in line:
                in_current_pass = True
                continue

            # Check if we left current pass section
            if in_current_pass and line.startswith("# 🥈") or line.startswith("# 🥇") or line.startswith("# 🔍"):
                break

            # Extract checkboxes in current section
            if in_current_pass:
                match = re.match(r'- \[([ xX])\] (.+)', line)
                if match:
                    is_done = match.group(1).lower() == 'x'
                    text = match.group(2).strip()
                    status = "completed" if is_done else "pending"

                    todos.append({
                        "content": text[:80],
                        "status": status,
                        "activeForm": text[:50],
                    })

        return todos

    def format_for_todowrite(self, todos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format todos for TodoWrite tool format.

        Args:
            todos: List of extracted todos

        Returns:
            TodoWrite-compatible list
        """
        formatted = []
        for todo in todos:
            formatted.append({
                "content": todo["content"],
                "status": todo["status"],
                "activeForm": todo.get("activeForm", todo["content"][:50]),
            })
        return formatted

    def get_completion_summary(self, sejr_path: Path) -> Dict[str, Any]:
        """
        Get completion summary for sejr.

        Args:
            sejr_path: Path to sejr folder

        Returns:
            Summary dictionary
        """
        todos = self.extract_todos_from_sejr(sejr_path)
        total = len(todos)
        completed = sum(1 for t in todos if t["status"] == "completed")

        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "percentage": (completed / total * 100) if total > 0 else 0,
        }

    def render_status(self, sejr_path: Path, width: int = 50) -> str:
        """Render todo sync status."""
        summary = self.get_completion_summary(sejr_path)
        phase = self.get_current_phase(sejr_path)

        lines = []
        lines.append("=" * width)
        lines.append("TODO SYNC STATUS".center(width))
        lines.append("=" * width)
        lines.append(f"  Current Pass: {phase['pass']}/3")
        lines.append(f"  Checkboxes: {summary['completed']}/{summary['total']}")
        lines.append(f"  Progress: {summary['percentage']:.0f}%")
        lines.append("=" * width)

        return "\n".join(lines)


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Testing TodoSync...")

    system_path = Path("/home/rasmus/Desktop/sejrliste systemet")
    sync = TodoSync(system_path)

    # Find first active sejr
    active_dir = system_path / "10_ACTIVE"
    if active_dir.exists():
        for sejr_folder in active_dir.iterdir():
            if sejr_folder.is_dir() and not sejr_folder.name.startswith('.'):
                print(f"\nTesting with: {sejr_folder.name}")

                # Test extraction
                todos = sync.extract_todos_from_sejr(sejr_folder)
                print(f"  Extracted {len(todos)} todos")

                # Test phase todos
                phase_todos = sync.get_phase_todos(sejr_folder)
                print(f"  Phase todos: {len(phase_todos)}")

                # Test summary
                summary = sync.get_completion_summary(sejr_folder)
                print(f"  Completed: {summary['completed']}/{summary['total']}")

                # Test render
                print("\n" + sync.render_status(sejr_folder, 40))

                break

    print("\n✅ TodoSync test complete!")
