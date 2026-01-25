#!/usr/bin/env python3
"""
File Watcher for Sejrliste System
Monitors changes to key files and triggers updates

Watches:
- 10_ACTIVE/*/SEJR_LISTE.md
- 10_ACTIVE/*/STATUS.yaml
- 10_ACTIVE/*/AUTO_LOG.jsonl
- _CURRENT/STATE.md
- _CURRENT/PATTERNS.yaml
- _CURRENT/NEXT.md
"""

import time
from pathlib import Path
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


class SejrFileHandler(FileSystemEventHandler):
    """Handle file system events for sejrliste files."""

    def __init__(self, callback=None):
        self.callback = callback
        self.last_event_time = {}

    def on_modified(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)

        # Debounce: ignore events within 1 second of each other
        now = time.time()
        if path in self.last_event_time:
            if now - self.last_event_time[path] < 1.0:
                return

        self.last_event_time[path] = now

        # Check if it's a file we care about
        watched_patterns = [
            "SEJR_LISTE.md",
            "STATUS.yaml",
            "AUTO_LOG.jsonl",
            "STATE.md",
            "PATTERNS.yaml",
            "NEXT.md",
        ]

        if path.name in watched_patterns:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Changed: {path.name}")
            if self.callback:
                self.callback(path)

    def on_created(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Created: {path.name}")
        if self.callback:
            self.callback(path)


class SejrWatcher:
    """Watch sejrliste system for changes."""

    def __init__(self, system_path: Path, callback=None):
        self.system_path = system_path
        self.callback = callback
        self.observer = None

    def start(self):
        """Start watching for file changes."""
        if not WATCHDOG_AVAILABLE:
            print("Warning: watchdog not installed. File watching disabled.")
            print("Install with: pip install watchdog")
            return False

        self.observer = Observer()
        handler = SejrFileHandler(callback=self.callback)

        # Watch active sejr folder
        active_dir = self.system_path / "10_ACTIVE"
        if active_dir.exists():
            self.observer.schedule(handler, str(active_dir), recursive=True)

        # Watch _CURRENT folder
        current_dir = self.system_path / "_CURRENT"
        if current_dir.exists():
            self.observer.schedule(handler, str(current_dir), recursive=False)

        self.observer.start()
        print(f"Watching: {self.system_path}")
        return True

    def stop(self):
        """Stop watching."""
        if self.observer:
            self.observer.stop()
            self.observer.join()


def watch_and_print(system_path: Path):
    """Simple watcher that prints changes."""

    def on_change(path):
        print(f"  → File changed: {path}")

    watcher = SejrWatcher(system_path, callback=on_change)

    if not watcher.start():
        return

    print("Press Ctrl+C to stop watching...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        watcher.stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Watch sejrliste for changes")
    parser.add_argument("--path", default=None, help="Path to sejrliste system")
    args = parser.parse_args()

    if args.path:
        system_path = Path(args.path)
    else:
        system_path = Path(__file__).parent.parent

    watch_and_print(system_path)
