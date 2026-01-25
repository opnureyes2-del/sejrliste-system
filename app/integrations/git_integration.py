#!/usr/bin/env python3
"""
Git Integration for Sejrliste Visual System.

Provides automated git workflow for sejr completion:
- Auto-commit on pass completion
- Standardized commit messages
- Branch management
"""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List


class GitIntegration:
    """
    Git integration for automated workflow.

    Features:
    - Auto-commit on pass completion
    - Standardized commit messages with PASS prefix
    - Status checking
    - Branch verification
    """

    def __init__(self, repo_path: Optional[Path] = None):
        """
        Initialize git integration.

        Args:
            repo_path: Path to git repository
        """
        self.repo_path = repo_path or Path.cwd()

    def is_git_repo(self) -> bool:
        """Check if current directory is a git repo."""
        git_dir = self.repo_path / ".git"
        return git_dir.exists()

    def get_status(self) -> Tuple[bool, str]:
        """
        Get git status.

        Returns:
            Tuple of (is_clean, status_text)
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout.strip()
            is_clean = len(output) == 0
            return is_clean, output if output else "Working tree clean"
        except Exception as e:
            return False, f"Error: {e}"

    def get_current_branch(self) -> str:
        """Get current git branch name."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip() or "main"
        except Exception as e:
            return "unknown"

    def stage_files(self, files: List[str]) -> Tuple[bool, str]:
        """
        Stage files for commit.

        Args:
            files: List of file paths to stage

        Returns:
            Tuple of (success, message)
        """
        try:
            result = subprocess.run(
                ["git", "add"] + files,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, f"Staged {len(files)} files"
            return False, result.stderr
        except Exception as e:
            return False, f"Error: {e}"

    def commit_pass(self, pass_number: int, message: str, co_author: bool = True) -> Tuple[bool, str]:
        """
        Create a commit with standardized PASS prefix.

        Args:
            pass_number: Pass number (1, 2, or 3)
            message: Commit message
            co_author: Include Co-Authored-By

        Returns:
            Tuple of (success, commit_hash or error)
        """
        pass_prefix = {
            1: "PASS 1:",
            2: "PASS 2:",
            3: "PASS 3 FINAL:",
        }

        prefix = pass_prefix.get(pass_number, f"PASS {pass_number}:")

        full_message = f"{prefix} {message}"

        if co_author:
            full_message += "\n\nCo-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

        try:
            result = subprocess.run(
                ["git", "commit", "-m", full_message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                # Extract commit hash
                hash_result = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                commit_hash = hash_result.stdout.strip()
                return True, commit_hash
            return False, result.stderr
        except Exception as e:
            return False, f"Error: {e}"

    def get_recent_commits(self, count: int = 5) -> List[dict]:
        """
        Get recent commits.

        Args:
            count: Number of commits to fetch

        Returns:
            List of commit dictionaries
        """
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--pretty=format:%h|%s|%cr"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            commits = []
            for line in result.stdout.strip().split("\n"):
                if "|" in line:
                    parts = line.split("|", 2)
                    if len(parts) >= 3:
                        commits.append({
                            "hash": parts[0],
                            "message": parts[1],
                            "time": parts[2],
                        })
            return commits
        except Exception as e:
            return []

    def verify_clean_state(self) -> Tuple[bool, str]:
        """
        Verify git is in a clean state for archiving.

        Returns:
            Tuple of (is_ready, message)
        """
        is_clean, status = self.get_status()

        if not is_clean:
            return False, f"Uncommitted changes: {status}"

        return True, "Git state clean - ready for archive"

    def render_status(self, width: int = 50) -> str:
        """Render git status for display."""
        lines = []
        lines.append("=" * width)
        lines.append("GIT STATUS".center(width))
        lines.append("=" * width)

        is_repo = self.is_git_repo()
        lines.append(f"  Repository: {'✅' if is_repo else '❌'}")

        if is_repo:
            branch = self.get_current_branch()
            is_clean, status = self.get_status()
            lines.append(f"  Branch: {branch}")
            lines.append(f"  Clean: {'✅' if is_clean else '❌'}")

            # Recent commits
            commits = self.get_recent_commits(3)
            if commits:
                lines.append("")
                lines.append("  Recent Commits:")
                for c in commits:
                    msg = c['message'][:30] + "..." if len(c['message']) > 30 else c['message']
                    lines.append(f"    {c['hash']} {msg}")

        lines.append("=" * width)
        return "\n".join(lines)


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Testing GitIntegration...")

    git = GitIntegration(Path("/home/rasmus/Desktop/sejrliste systemet"))

    # Check status
    print("\n" + git.render_status(50))

    # Test methods
    print(f"\nIs git repo: {git.is_git_repo()}")
    print(f"Current branch: {git.get_current_branch()}")

    is_clean, status = git.get_status()
    print(f"Is clean: {is_clean}")

    # Verify clean state
    ready, msg = git.verify_clean_state()
    print(f"Ready for archive: {ready} - {msg}")

    print("\n✅ GitIntegration test complete!")
