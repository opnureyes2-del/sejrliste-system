#!/usr/bin/env python3
"""
EXECUTOR - Run AI model tasks with budget tracking
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict

class TaskExecutor:
    """Executes AI tasks with model routing and budget tracking"""

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.task_queue: list = []
        self.completed_tasks: list = []
        self.tokens_used: Dict[int, int] = {lag: 0 for lag in range(1, 8)}

    def add_task(self, task_type: str, prompt: str, dna_lag: int = None) -> dict:
        task = {
            "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": task_type,
            "prompt": prompt,
            "dna_lag": dna_lag,
            "status": "pending",
            "created": datetime.now().isoformat(),
        }
        self.task_queue.append(task)
        return task

    def get_queue_status(self) -> dict:
        return {
            "pending": len([t for t in self.task_queue if t["status"] == "pending"]),
            "completed_today": len(self.completed_tasks),
            "tokens_used": self.tokens_used.copy(),
        }

    def log_activity(self, sejr_path: Path, action: str, details: dict) -> None:
        log_file = sejr_path / "AUTO_LOG.jsonl"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        }
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
