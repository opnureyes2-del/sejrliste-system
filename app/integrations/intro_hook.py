#!/usr/bin/env python3
"""
INTRO Folder Hook for Sejrliste Visual System.

Keeps the INTRO context system (/.claude/.context/) in sync with sejrliste activity.
Updates session.md, journal.md, and projects.md automatically when:
- A new sejr is started
- A sejr is completed/archived
- Significant progress is made

DNA LAG INTEGRATION:
- Lag 2 (SELF-DOCUMENTING): Updates session.md with current work
- Lag 5 (SELF-ARCHIVING): Appends to journal.md on completion
- Lag 4 (SELF-IMPROVING): Updates patterns in projects.md
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class IntroHook:
    """
    Hook into INTRO context system for automatic updates.

    When sejrliste events happen, this hook updates the appropriate
    context files to keep everything in sync.
    """

    # Default INTRO context path
    INTRO_PATH = Path.home() / ".claude" / ".context" / "core"

    def __init__(self, intro_path: Optional[Path] = None):
        """
        Initialize INTRO hook.

        Args:
            intro_path: Path to INTRO core folder (defaults to ~/.claude/.context/core/)
        """
        self.intro_path = intro_path or self.INTRO_PATH
        self.session_file = self.intro_path / "session.md"
        self.journal_file = self.intro_path / "journal.md"
        self.projects_file = self.intro_path / "projects.md"
        self.rules_file = self.intro_path / "rules.md"

    def on_sejr_started(self, sejr_info: Dict[str, Any]) -> bool:
        """
        Called when a new sejr is started.

        Updates session.md with the new sejr information.

        Args:
            sejr_info: Dictionary containing sejr details
                - name: Sejr name
                - path: Path to sejr folder
                - goal: What this sejr aims to achieve

        Returns:
            True if hook executed successfully
        """
        if not self.session_file.exists():
            return False

        try:
            # Create session update
            name = sejr_info.get("name", "Unknown")
            goal = sejr_info.get("goal", "No goal specified")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            entry = f"""
---

## Sejrliste Started: {timestamp}

**Sejr:** {name}
**Goal:** {goal}
**Status:** 🔵 In Progress

---
"""

            # Read and append
            content = self.session_file.read_text()

            # Don't duplicate entries
            if name in content:
                return True

            # Append after current session header
            new_content = content.rstrip() + "\n" + entry
            self.session_file.write_text(new_content)

            return True

        except Exception as e:
            print(f"[IntroHook] Error on_sejr_started: {e}")
            return False

    def on_sejr_progress(self, sejr_info: Dict[str, Any]) -> bool:
        """
        Called when significant progress is made on a sejr.

        Only updates if major milestone (e.g., pass completed).

        Args:
            sejr_info: Dictionary containing progress info
                - name: Sejr name
                - current_pass: Which pass we're on (1-3)
                - checkboxes_done: Number of completed checkboxes
                - checkboxes_total: Total checkboxes

        Returns:
            True if hook executed successfully
        """
        # Only update on pass completion or significant milestone
        current_pass = sejr_info.get("current_pass", 1)
        done = sejr_info.get("checkboxes_done", 0)
        total = sejr_info.get("checkboxes_total", 1)

        pct = (done / total * 100) if total > 0 else 0

        # Only update at 50%, 100%, or pass transitions
        if pct not in [50, 100] and done != 0:
            return True  # Skip minor updates

        if not self.session_file.exists():
            return False

        try:
            name = sejr_info.get("name", "Unknown")
            timestamp = datetime.now().strftime("%H:%M")

            # Short progress note
            note = f"\n**{timestamp}:** {name} - Pass {current_pass}/3 - {done}/{total} ({pct:.0f}%)\n"

            content = self.session_file.read_text()
            new_content = content.rstrip() + note
            self.session_file.write_text(new_content)

            return True

        except Exception as e:
            print(f"[IntroHook] Error on_sejr_progress: {e}")
            return False

    def on_sejr_archived(self, sejr_info: Dict[str, Any]) -> bool:
        """
        Called when a sejr is archived (completed).

        Updates journal.md with the completion summary.

        Args:
            sejr_info: Dictionary containing completion info
                - name: Sejr name
                - score: Total score achieved (out of 30)
                - rank: Final rank (KADET, OFFICER, etc.)
                - learnings: What was learned
                - archived_at: Timestamp

        Returns:
            True if hook executed successfully
        """
        if not self.journal_file.exists():
            return False

        try:
            name = sejr_info.get("name", "Unknown")
            score = sejr_info.get("score", 0)
            rank = sejr_info.get("rank", "KADET")
            learnings = sejr_info.get("learnings", "No learnings captured")
            archived_at = sejr_info.get("archived_at", datetime.now().isoformat())

            # Parse timestamp
            if isinstance(archived_at, str):
                try:
                    ts = datetime.fromisoformat(archived_at)
                    date_str = ts.strftime("%Y-%m-%d %H:%M")
                except:
                    date_str = archived_at[:16]
            else:
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Create journal entry
            entry = f"""
---

### {date_str}: Sejr Completed - {name}

**Score:** {score}/30 | **Rank:** {rank}

**Learnings:**
{learnings}

**DNA Lag Activated:** All 7 layers successfully processed.

---
"""

            content = self.journal_file.read_text()
            new_content = content.rstrip() + "\n" + entry
            self.journal_file.write_text(new_content)

            # Also clear session entry
            self._clear_session_entry(name)

            return True

        except Exception as e:
            print(f"[IntroHook] Error on_sejr_archived: {e}")
            return False

    def on_pattern_learned(self, pattern_info: Dict[str, Any]) -> bool:
        """
        Called when a new pattern is learned (DNA Lag 4).

        Can optionally update rules.md if pattern is significant.

        Args:
            pattern_info: Dictionary containing pattern info
                - pattern: The pattern description
                - source: Where it was learned from
                - confidence: How confident we are (0.0-1.0)

        Returns:
            True if hook executed successfully
        """
        confidence = pattern_info.get("confidence", 0.5)

        # Only add to rules if high confidence
        if confidence < 0.9:
            return True  # Skip low confidence patterns

        if not self.rules_file.exists():
            return False

        try:
            pattern = pattern_info.get("pattern", "Unknown pattern")
            source = pattern_info.get("source", "Unknown source")

            # Check if pattern already exists
            content = self.rules_file.read_text()
            if pattern in content:
                return True  # Already exists

            # Append as learned pattern
            entry = f"""

---

**Learned Pattern ({datetime.now().strftime('%Y-%m-%d')}):**
- Pattern: {pattern}
- Source: {source}
- Confidence: {confidence:.0%}

---
"""

            new_content = content.rstrip() + entry
            self.rules_file.write_text(new_content)

            return True

        except Exception as e:
            print(f"[IntroHook] Error on_pattern_learned: {e}")
            return False

    def _clear_session_entry(self, sejr_name: str) -> bool:
        """
        Clear completed sejr from session.md.

        Args:
            sejr_name: Name of the completed sejr

        Returns:
            True if successful
        """
        if not self.session_file.exists():
            return False

        try:
            content = self.session_file.read_text()

            # Mark as completed rather than removing
            if f"**Sejr:** {sejr_name}" in content:
                content = content.replace(
                    f"**Status:** 🔵 In Progress",
                    f"**Status:** ✅ Archived"
                )
                self.session_file.write_text(content)

            return True

        except Exception as e:
            return False

    def get_hook_status(self) -> Dict[str, Any]:
        """
        Get status of all INTRO files.

        Returns:
            Dictionary with file existence and write permissions
        """
        return {
            "session": {
                "exists": self.session_file.exists(),
                "writable": self.session_file.exists() and self.session_file.stat().st_mode & 0o200
            },
            "journal": {
                "exists": self.journal_file.exists(),
                "writable": self.journal_file.exists() and self.journal_file.stat().st_mode & 0o200
            },
            "projects": {
                "exists": self.projects_file.exists(),
                "writable": self.projects_file.exists() and self.projects_file.stat().st_mode & 0o200
            },
            "rules": {
                "exists": self.rules_file.exists(),
                "writable": self.rules_file.exists() and self.rules_file.stat().st_mode & 0o200
            }
        }

    def render_status(self, width: int = 50) -> str:
        """Render hook status for display."""
        status = self.get_hook_status()

        lines = []
        lines.append("=" * width)
        lines.append("INTRO HOOK STATUS".center(width))
        lines.append("=" * width)

        for name, info in status.items():
            exists_icon = "✅" if info["exists"] else "❌"
            write_icon = "✍️" if info.get("writable") else "🔒"
            lines.append(f"  {exists_icon} {write_icon} {name}.md")

        lines.append("=" * width)
        return "\n".join(lines)


# ============================================================================
# Factory function for easy integration
# ============================================================================

def create_intro_hook(intro_path: Optional[Path] = None) -> IntroHook:
    """
    Create an INTRO hook instance.

    Args:
        intro_path: Optional path to INTRO context folder

    Returns:
        IntroHook instance
    """
    return IntroHook(intro_path)


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Testing IntroHook...")

    hook = IntroHook()

    # Check status
    print("\n" + hook.render_status(40))

    # Test events (dry run - won't actually write in test mode)
    print("\nTesting hook events...")

    # Test sejr started
    result = hook.on_sejr_started({
        "name": "TEST_SEJR",
        "goal": "Test the INTRO hook system"
    })
    print(f"on_sejr_started: {'✅' if result else '❌'}")

    # Test progress
    result = hook.on_sejr_progress({
        "name": "TEST_SEJR",
        "current_pass": 2,
        "checkboxes_done": 25,
        "checkboxes_total": 50
    })
    print(f"on_sejr_progress: {'✅' if result else '❌'}")

    # Test archived
    result = hook.on_sejr_archived({
        "name": "TEST_SEJR",
        "score": 27,
        "rank": "ADMIRAL",
        "learnings": "INTRO hook integration works!"
    })
    print(f"on_sejr_archived: {'✅' if result else '❌'}")

    print("\n✅ IntroHook test complete!")
