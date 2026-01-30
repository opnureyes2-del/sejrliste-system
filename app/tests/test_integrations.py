#!/usr/bin/env python3
"""
Unit tests for Integration modules.

Tests:
1. ContextSync - session/journal/projects sync
2. GitIntegration - git workflow automation
"""

import sys
from pathlib import Path
import unittest

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.integrations.context_sync import ContextSync
from app.integrations.git_integration import GitIntegration
from app.integrations.todo_sync import TodoSync


class TestContextSync(unittest.TestCase):
    """Test cases for ContextSync."""

    def setUp(self):
        """Set up test fixtures."""
        self.sync = ContextSync()
        self.sejr_info = {
            "name": "TEST_SEJR",
            "current_pass": 2,
            "score": 18,
            "checkboxes_done": 25,
            "checkboxes_total": 40,
        }

    def test_init(self):
        """Test ContextSync initialization."""
        self.assertIsNotNone(self.sync.context_path)
        self.assertIsNotNone(self.sync.session_file)
        self.assertIsNotNone(self.sync.journal_file)

    def test_session_file_exists(self):
        """Test session.md exists."""
        self.assertTrue(self.sync.session_file.exists())

    def test_journal_file_exists(self):
        """Test journal.md exists."""
        self.assertTrue(self.sync.journal_file.exists())

    def test_create_session_block(self):
        """Test session block creation."""
        block = self.sync._create_session_block(self.sejr_info)
        self.assertIn("TEST_SEJR", block)
        self.assertIn("Pass:", block)
        self.assertIn("25/40", block)

    def test_create_journal_entry(self):
        """Test journal entry creation."""
        entry = self.sync._create_journal_entry(self.sejr_info)
        self.assertIn("TEST_SEJR", entry)
        self.assertIn("18/30", entry)

    def test_get_sync_status(self):
        """Test sync status retrieval."""
        status = self.sync.get_sync_status()
        self.assertIn("session", status)
        self.assertIn("journal", status)
        self.assertIn("projects", status)

    def test_render_status(self):
        """Test status rendering."""
        rendered = self.sync.render_status()
        self.assertIn("CONTEXT SYNC STATUS", rendered)


class TestGitIntegration(unittest.TestCase):
    """Test cases for GitIntegration."""

    def setUp(self):
        """Set up test fixtures."""
        self.git = GitIntegration(Path(__file__).parent.parent.parent)

    def test_init(self):
        """Test GitIntegration initialization."""
        self.assertIsNotNone(self.git.repo_path)

    def test_is_git_repo(self):
        """Test git repo detection."""
        is_repo = self.git.is_git_repo()
        self.assertTrue(is_repo)

    def test_get_current_branch(self):
        """Test branch name retrieval."""
        branch = self.git.get_current_branch()
        self.assertIsNotNone(branch)
        self.assertNotEqual(branch, "unknown")

    def test_get_status(self):
        """Test git status."""
        is_clean, status = self.git.get_status()
        self.assertIsInstance(is_clean, bool)
        self.assertIsInstance(status, str)

    def test_get_recent_commits(self):
        """Test recent commits retrieval."""
        commits = self.git.get_recent_commits(3)
        self.assertIsInstance(commits, list)
        if commits:
            self.assertIn("hash", commits[0])
            self.assertIn("message", commits[0])

    def test_verify_clean_state(self):
        """Test clean state verification."""
        ready, msg = self.git.verify_clean_state()
        self.assertIsInstance(ready, bool)
        self.assertIsInstance(msg, str)

    def test_render_status(self):
        """Test status rendering."""
        rendered = self.git.render_status()
        self.assertIn("GIT STATUS", rendered)
        self.assertIn("Branch", rendered)


class TestTodoSync(unittest.TestCase):
    """Test cases for TodoSync (PASS 2)."""

    def setUp(self):
        """Set up test fixtures."""
        self.system_path = Path(__file__).parent.parent.parent
        self.sync = TodoSync(self.system_path)
        # Find first active sejr
        self.test_sejr = None
        active_dir = self.system_path / "10_ACTIVE"
        if active_dir.exists():
            for folder in active_dir.iterdir():
                if folder.is_dir() and not folder.name.startswith('.'):
                    self.test_sejr = folder
                    break

    def test_init(self):
        """Test TodoSync initialization."""
        self.assertIsNotNone(self.sync.system_path)

    def test_extract_todos(self):
        """Test todo extraction from sejr."""
        if self.test_sejr:
            todos = self.sync.extract_todos_from_sejr(self.test_sejr)
            self.assertIsInstance(todos, list)
            if todos:
                self.assertIn("content", todos[0])
                self.assertIn("status", todos[0])

    def test_get_current_phase(self):
        """Test current phase detection."""
        if self.test_sejr:
            phase = self.sync.get_current_phase(self.test_sejr)
            self.assertIn("phase", phase)
            self.assertIn("pass", phase)

    def test_get_completion_summary(self):
        """Test completion summary."""
        if self.test_sejr:
            summary = self.sync.get_completion_summary(self.test_sejr)
            self.assertIn("total", summary)
            self.assertIn("completed", summary)
            self.assertIn("percentage", summary)

    def test_format_for_todowrite(self):
        """Test TodoWrite format conversion."""
        todos = [
            {"content": "Test task", "status": "pending", "activeForm": "Testing"}
        ]
        formatted = self.sync.format_for_todowrite(todos)
        self.assertEqual(len(formatted), 1)
        self.assertEqual(formatted[0]["content"], "Test task")

    def test_render_status(self):
        """Test status rendering."""
        if self.test_sejr:
            rendered = self.sync.render_status(self.test_sejr)
            self.assertIn("TODO SYNC STATUS", rendered)
            self.assertIn("Current Pass", rendered)


class TestIntegrationModule(unittest.TestCase):
    """Test cases for integration module imports."""

    def test_imports(self):
        """Test that all integrations import correctly."""
        from app.integrations import ContextSync, GitIntegration, TodoSync
        self.assertIsNotNone(ContextSync)
        self.assertIsNotNone(GitIntegration)
        self.assertIsNotNone(TodoSync)


if __name__ == "__main__":
    unittest.main(verbosity=2)
