#!/usr/bin/env python3
"""
SEJR LIST WIDGET - Checkbox list for tasks
"""
from pathlib import Path
import re
from typing import List, Tuple

class SejrListWidget:
    """Widget for displaying and managing sejr checkboxes"""

    def __init__(self, sejr_path: Path):
        self.sejr_path = sejr_path
        self.sejr_file = sejr_path / "SEJR_LISTE.md"
        self.checkboxes: List[Tuple[str, bool]] = []

    def load(self) -> None:
        """Load checkboxes from SEJR_LISTE.md"""
        self.checkboxes = []
        if self.sejr_file.exists():
            content = self.sejr_file.read_text(encoding="utf-8")
            for line in content.split("\n"):
                if "- [" in line:
                    is_checked = "- [x]" in line.lower()
                    text = line.split("]", 1)[1].strip() if "]" in line else line
                    self.checkboxes.append((text, is_checked))

    def get_progress(self) -> Tuple[int, int]:
        """Get (done, total) counts"""
        done = sum(1 for _, checked in self.checkboxes if checked)
        return done, len(self.checkboxes)

    def get_completion_pct(self) -> int:
        """Get completion percentage"""
        done, total = self.get_progress()
        return int((done / total * 100)) if total > 0 else 0

    def get_display_items(self, limit: int = 15) -> List[dict]:
        """Get items formatted for display"""
        items = []
        for i, (text, checked) in enumerate(self.checkboxes[:limit]):
            items.append({
                "index": i,
                "text": text[:50],
                "checked": checked,
                "icon": "[OK]" if checked else "⬜",
            })
        return items
