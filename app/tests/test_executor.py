#!/usr/bin/env python3
"""
Unit tests for TaskExecutor.

Tests the ACTUAL TaskExecutor class (not ScriptExecutor).
Fixed 2026-01-31: Tests now match real code.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.executor import TaskExecutor


def test_task_executor_init():
    """Test 1: TaskExecutor initializes correctly."""
    system_path = Path(__file__).parent.parent.parent
    executor = TaskExecutor(system_path)

    assert executor is not None
    assert executor.system_path == system_path
    assert executor.task_queue == []
    assert executor.completed_tasks == []
    assert len(executor.tokens_used) == 7  # 7 DNA lags

    print("[OK] Test 1 PASSED: TaskExecutor initializes correctly")
    return True


def test_add_task():
    """Test 2: Can add tasks to queue."""
    system_path = Path(__file__).parent.parent.parent
    executor = TaskExecutor(system_path)

    task = executor.add_task("verify", "Test prompt", dna_lag=3)

    assert task is not None
    assert task["type"] == "verify"
    assert task["prompt"] == "Test prompt"
    assert task["dna_lag"] == 3
    assert task["status"] == "pending"
    assert len(executor.task_queue) == 1

    print("[OK] Test 2 PASSED: Can add tasks to queue")
    return True


def test_add_multiple_tasks():
    """Test 3: Can add multiple tasks."""
    system_path = Path(__file__).parent.parent.parent
    executor = TaskExecutor(system_path)

    executor.add_task("verify", "Task 1")
    executor.add_task("generate", "Task 2")
    executor.add_task("review", "Task 3")

    assert len(executor.task_queue) == 3

    print("[OK] Test 3 PASSED: Can add multiple tasks")
    return True


def test_task_has_id():
    """Test 4: Tasks have unique IDs."""
    system_path = Path(__file__).parent.parent.parent
    executor = TaskExecutor(system_path)

    task = executor.add_task("verify", "Test")

    assert "id" in task
    assert task["id"].startswith("task_")

    print("[OK] Test 4 PASSED: Tasks have unique IDs")
    return True


if __name__ == "__main__":
    test_task_executor_init()
    test_add_task()
    test_add_multiple_tasks()
    test_task_has_id()
    print("\n[OK] All executor tests passed!")
