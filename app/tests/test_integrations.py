#!/usr/bin/env python3
"""
Unit tests for Integration modules.

Tests the ACTUAL function-based API (not class-based).
Fixed 2026-01-31: Tests now match real code.
"""

import sys
from pathlib import Path
import unittest

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestContextSyncFunctions(unittest.TestCase):
    """Test context_sync functions."""

    def test_import(self):
        """Test that context_sync imports correctly."""
        from app.integrations.context_sync import update_context_on_completion, update_journal
        self.assertIsNotNone(update_context_on_completion)
        self.assertIsNotNone(update_journal)

    def test_update_context_callable(self):
        """Test update_context_on_completion is callable."""
        from app.integrations.context_sync import update_context_on_completion
        self.assertTrue(callable(update_context_on_completion))

    def test_update_journal_callable(self):
        """Test update_journal is callable."""
        from app.integrations.context_sync import update_journal
        self.assertTrue(callable(update_journal))


class TestGitIntegrationFunctions(unittest.TestCase):
    """Test git_integration functions."""

    def test_import(self):
        """Test that git_integration imports correctly."""
        from app.integrations.git_integration import auto_commit_on_complete, push_to_remote, get_git_status
        self.assertIsNotNone(auto_commit_on_complete)
        self.assertIsNotNone(push_to_remote)
        self.assertIsNotNone(get_git_status)

    def test_get_git_status(self):
        """Test git status retrieval."""
        from app.integrations.git_integration import get_git_status
        system_path = Path(__file__).parent.parent.parent
        status = get_git_status(system_path)
        self.assertIsInstance(status, dict)


class TestTodoSyncFunctions(unittest.TestCase):
    """Test todo_sync functions."""

    def test_import(self):
        """Test that todo_sync imports correctly."""
        from app.integrations.todo_sync import extract_todos_from_sejr, mark_todo_complete, sync_todowrite
        self.assertIsNotNone(extract_todos_from_sejr)
        self.assertIsNotNone(mark_todo_complete)
        self.assertIsNotNone(sync_todowrite)

    def test_extract_todos(self):
        """Test todo extraction from active sejr."""
        from app.integrations.todo_sync import extract_todos_from_sejr
        system_path = Path(__file__).parent.parent.parent
        active_dir = system_path / "10_ACTIVE"
        if active_dir.exists():
            for folder in active_dir.iterdir():
                if folder.is_dir() and not folder.name.startswith('.'):
                    todos = extract_todos_from_sejr(folder)
                    self.assertIsInstance(todos, list)
                    break


class TestIntegrationModuleImports(unittest.TestCase):
    """Test top-level integration imports."""

    def test_imports(self):
        """Test that all integrations import from __init__.py."""
        from app.integrations import update_context_on_completion, auto_commit_on_complete, sync_todowrite
        self.assertIsNotNone(update_context_on_completion)
        self.assertIsNotNone(auto_commit_on_complete)
        self.assertIsNotNone(sync_todowrite)


if __name__ == "__main__":
    unittest.main(verbosity=2)
