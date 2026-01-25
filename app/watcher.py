#!/usr/bin/env python3
"""
FILE WATCHER - Real-time file monitoring for Sejrliste
Watches key files and triggers updates
"""
import time
from pathlib import Path
from typing import Dict, Callable
from datetime import datetime
import hashlib

class FileWatcher:
    """Watches files for changes and triggers callbacks"""

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.watched_files: Dict[str, str] = {}  # path -> last_hash
        self.callbacks: Dict[str, Callable] = {}
        self.last_check = datetime.now()

        # Files to watch (from plan)
        self.watch_patterns = {
            "10_ACTIVE/*/SEJR_LISTE.md": "update_task_list",
            "10_ACTIVE/*/STATUS.yaml": "update_progress",
            "10_ACTIVE/*/AUTO_LOG.jsonl": "append_log_stream",
            "_CURRENT/STATE.md": "refresh_overview",
            "_CURRENT/PATTERNS.yaml": "update_patterns",
            "_CURRENT/NEXT.md": "update_predictions",
        }

    def get_file_hash(self, filepath: Path) -> str:
        """Get MD5 hash of file content"""
        if filepath.exists():
            content = filepath.read_bytes()
            return hashlib.md5(content).hexdigest()
        return ""

    def register_callback(self, name: str, callback: Callable) -> None:
        """Register callback function for file changes"""
        self.callbacks[name] = callback

    def check_file(self, filepath: Path, callback_name: str) -> bool:
        """Check single file for changes"""
        current_hash = self.get_file_hash(filepath)
        str_path = str(filepath)

        if str_path not in self.watched_files:
            self.watched_files[str_path] = current_hash
            return False

        if current_hash != self.watched_files[str_path]:
            self.watched_files[str_path] = current_hash
            if callback_name in self.callbacks:
                self.callbacks[callback_name](filepath)
            return True

        return False

    def check_all(self) -> list:
        """Check all watched files for changes"""
        changes = []
        for pattern, callback_name in self.watch_patterns.items():
            # Handle glob patterns
            if "*" in pattern:
                for filepath in self.system_path.glob(pattern):
                    if self.check_file(filepath, callback_name):
                        changes.append((str(filepath), callback_name))
            else:
                filepath = self.system_path / pattern
                if self.check_file(filepath, callback_name):
                    changes.append((str(filepath), callback_name))

        self.last_check = datetime.now()
        return changes

    def get_status(self) -> dict:
        """Get watcher status"""
        return {
            "files_watched": len(self.watched_files),
            "callbacks_registered": len(self.callbacks),
            "last_check": self.last_check.isoformat(),
        }


def create_watcher(system_path: Path) -> FileWatcher:
    """Factory function to create configured watcher"""
    watcher = FileWatcher(system_path)

    # Default callbacks (just log for now)
    def log_change(filepath):
        print(f"[WATCHER] File changed: {filepath}")

    watcher.register_callback("update_task_list", log_change)
    watcher.register_callback("update_progress", log_change)
    watcher.register_callback("append_log_stream", log_change)
    watcher.register_callback("refresh_overview", log_change)
    watcher.register_callback("update_patterns", log_change)
    watcher.register_callback("update_predictions", log_change)

    return watcher
