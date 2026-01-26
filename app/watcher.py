#!/usr/bin/env python3
"""
FILE WATCHER - Real-time updates for Sejrliste
Watches for changes in:
- 10_ACTIVE/*/SEJR_LISTE.md
- 10_ACTIVE/*/VERIFY_STATUS.yaml
- 10_ACTIVE/*/AUTO_LOG.jsonl
- _CURRENT/STATE.md
- _CURRENT/PATTERNS.yaml
- _CURRENT/NEXT.md
"""

import asyncio
from pathlib import Path
from typing import Callable, Dict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

BASE_PATH = Path(__file__).parent.parent


class SejrFileHandler(FileSystemEventHandler):
    """Handler for file system events"""
    
    def __init__(self, callbacks: Dict[str, Callable]):
        self.callbacks = callbacks
    
    def on_modified(self, event: FileSystemEvent):
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        filename = path.name
        
        # Match against watched patterns
        if filename == "SEJR_LISTE.md":
            self._call("update_task_list", path)
        elif filename == "VERIFY_STATUS.yaml":
            self._call("update_progress", path)
        elif filename == "AUTO_LOG.jsonl":
            self._call("append_log_stream", path)
        elif filename == "STATE.md":
            self._call("refresh_overview", path)
        elif filename == "PATTERNS.yaml":
            self._call("update_patterns", path)
        elif filename == "NEXT.md":
            self._call("update_predictions", path)
    
    def _call(self, callback_name: str, path: Path):
        if callback_name in self.callbacks:
            self.callbacks[callback_name](path)


class FileWatcher:
    """Watches sejrliste files for changes"""
    
    def __init__(self):
        self.observer = Observer()
        self.callbacks: Dict[str, Callable] = {}
    
    def register_callback(self, name: str, callback: Callable):
        """Register a callback for a specific event"""
        self.callbacks[name] = callback
    
    def start(self):
        """Start watching for file changes"""
        handler = SejrFileHandler(self.callbacks)
        
        # Watch active sejr folder
        active_path = BASE_PATH / "10_ACTIVE"
        if active_path.exists():
            self.observer.schedule(handler, str(active_path), recursive=True)
        
        # Watch current state folder
        current_path = BASE_PATH / "_CURRENT"
        if current_path.exists():
            self.observer.schedule(handler, str(current_path), recursive=True)
        
        self.observer.start()
    
    def stop(self):
        """Stop watching"""
        self.observer.stop()
        self.observer.join()


async def watch_files(app):
    """Async file watcher integration with Textual app"""
    watcher = FileWatcher()
    
    def on_update(path: Path):
        app.load_sejrs()
        app.refresh()
    
    watcher.register_callback("update_task_list", on_update)
    watcher.register_callback("update_progress", on_update)
    watcher.register_callback("append_log_stream", on_update)
    watcher.register_callback("refresh_overview", on_update)
    watcher.register_callback("update_patterns", on_update)
    watcher.register_callback("update_predictions", on_update)
    
    watcher.start()
    
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        watcher.stop()
