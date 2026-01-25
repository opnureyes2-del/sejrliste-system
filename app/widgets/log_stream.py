#!/usr/bin/env python3
"""
LOG STREAM WIDGET - Live AUTO_LOG.jsonl viewer
"""
from pathlib import Path
import json
from typing import List
from datetime import datetime

class LogStream:
    """Widget for displaying live log stream"""

    def __init__(self, sejr_path: Path):
        self.sejr_path = sejr_path
        self.log_file = sejr_path / "AUTO_LOG.jsonl"
        self.entries: List[dict] = []

    def load(self, limit: int = 10) -> None:
        """Load recent log entries"""
        self.entries = []
        if self.log_file.exists():
            lines = self.log_file.read_text(encoding="utf-8").strip().split("\n")
            for line in lines[-limit:]:
                try:
                    entry = json.loads(line)
                    self.entries.append(entry)
                except json.JSONDecodeError:
                    pass

    def get_formatted_entries(self) -> List[str]:
        """Get entries formatted for display"""
        formatted = []
        for entry in reversed(self.entries):
            timestamp = entry.get("timestamp", "N/A")[:19]
            action = entry.get("action", "unknown")
            details = str(entry.get("details", {}))[:60]
            formatted.append(f"[{timestamp}] {action}: {details}")
        return formatted

    def append_entry(self, action: str, details: dict) -> None:
        """Add new entry to log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        self.entries.append(entry)
