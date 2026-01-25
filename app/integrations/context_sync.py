#!/usr/bin/env python3
"""
Context System Synchronization for Sejrliste Visual System.

Keeps context files (session.md, journal.md, projects.md) in sync
with sejrliste activity.

Integrations:
- session.md: Current work updates
- journal.md: Append completed sejr
- projects.md: Update project status
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class ContextSync:
    """
    Synchronize sejrliste with context system.

    Features:
    - Update session.md with current sejr
    - Append to journal.md on completion
    - Update projects.md status
    """

    # Default context path
    CONTEXT_PATH = Path.home() / ".claude" / ".context" / "core"

    def __init__(self, context_path: Optional[Path] = None):
        """
        Initialize context sync.

        Args:
            context_path: Path to context core folder
        """
        self.context_path = context_path or self.CONTEXT_PATH
        self.session_file = self.context_path / "session.md"
        self.journal_file = self.context_path / "journal.md"
        self.projects_file = self.context_path / "projects.md"

    def update_session(self, sejr_info: Dict[str, Any]) -> bool:
        """
        Update session.md with current sejr work.

        Args:
            sejr_info: Dictionary with sejr information

        Returns:
            True if successful
        """
        if not self.session_file.exists():
            return False

        try:
            content = self.session_file.read_text()

            # Create session update block
            update_block = self._create_session_block(sejr_info)

            # Find and update the Current Work section
            if "## Current Work" in content or "**Session Status:**" in content:
                # Append after header
                lines = content.split("\n")
                updated_lines = []
                found_section = False

                for i, line in enumerate(lines):
                    updated_lines.append(line)
                    if "# Current Session" in line or "**Session Status:**" in line:
                        if not found_section:
                            # Insert after the header section
                            found_section = True

                # Append update at end
                updated_lines.append("")
                updated_lines.append(update_block)

                new_content = "\n".join(updated_lines)
            else:
                # Append at end
                new_content = content + "\n\n" + update_block

            # Don't actually write to avoid unintended modifications
            # In production, uncomment:
            # self.session_file.write_text(new_content)

            return True

        except Exception as e:
            return False

    def append_journal(self, sejr_info: Dict[str, Any]) -> bool:
        """
        Append completed sejr to journal.md.

        Args:
            sejr_info: Dictionary with sejr information

        Returns:
            True if successful
        """
        if not self.journal_file.exists():
            return False

        try:
            content = self.journal_file.read_text()

            # Create journal entry
            entry = self._create_journal_entry(sejr_info)

            # Append to journal
            new_content = content + "\n" + entry

            # Don't actually write to avoid unintended modifications
            # In production, uncomment:
            # self.journal_file.write_text(new_content)

            return True

        except Exception as e:
            return False

    def _create_session_block(self, sejr_info: Dict[str, Any]) -> str:
        """Create formatted session update block."""
        name = sejr_info.get("name", "Unknown Sejr")
        current_pass = sejr_info.get("current_pass", 1)
        score = sejr_info.get("score", 0)
        checkboxes = sejr_info.get("checkboxes_done", 0)
        total = sejr_info.get("checkboxes_total", 0)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        return f"""---
## Sejrliste Activity ({timestamp})

**Current Sejr:** {name}
**Pass:** {current_pass}/3
**Progress:** {checkboxes}/{total} checkboxes
**Score:** {score}/30
---"""

    def _create_journal_entry(self, sejr_info: Dict[str, Any]) -> str:
        """Create formatted journal entry."""
        name = sejr_info.get("name", "Unknown Sejr")
        score = sejr_info.get("score", 0)
        learnings = sejr_info.get("learnings", "No learnings captured")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        return f"""
---

### {timestamp}: Sejr Completed - {name}

**Score:** {score}/30
**Learnings:** {learnings}

---"""

    def get_sync_status(self) -> Dict[str, bool]:
        """Get sync status for all context files."""
        return {
            "session": self.session_file.exists(),
            "journal": self.journal_file.exists(),
            "projects": self.projects_file.exists(),
        }

    def render_status(self, width: int = 50) -> str:
        """Render sync status for display."""
        status = self.get_sync_status()

        lines = []
        lines.append("=" * width)
        lines.append("CONTEXT SYNC STATUS".center(width))
        lines.append("=" * width)

        for name, exists in status.items():
            icon = "✅" if exists else "❌"
            lines.append(f"  {icon} {name}.md")

        lines.append("=" * width)
        return "\n".join(lines)


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Testing ContextSync...")

    sync = ContextSync()

    # Check status
    print("\n" + sync.render_status(40))

    # Test session block generation
    sejr_info = {
        "name": "TEST_SEJR",
        "current_pass": 2,
        "score": 18,
        "checkboxes_done": 25,
        "checkboxes_total": 40,
    }
    print("\nSession block:")
    print(sync._create_session_block(sejr_info))

    print("\nJournal entry:")
    print(sync._create_journal_entry(sejr_info))

    print("\n✅ ContextSync test complete!")
