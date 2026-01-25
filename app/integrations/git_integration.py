#!/usr/bin/env python3
"""
GIT INTEGRATION - Auto-commit on sejr completion
"""
from pathlib import Path
import subprocess
from datetime import datetime

def auto_commit_on_complete(sejr_path: Path, sejr_name: str, score: int) -> bool:
    """Auto-commit when sejr is completed"""
    try:
        # Stage changes
        subprocess.run(
            ["git", "add", "."],
            cwd=str(sejr_path.parent.parent),
            capture_output=True,
            check=True
        )

        # Commit with message
        commit_msg = f"Sejr completed: {sejr_name} ({score}/30)\n\nCo-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=str(sejr_path.parent.parent),
            capture_output=True,
            check=True
        )

        print(f"[GIT] Committed: {sejr_name}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[GIT] Error: {e}")
        return False

def push_to_remote(sejr_path: Path) -> bool:
    """Push commits to remote"""
    try:
        subprocess.run(
            ["git", "push"],
            cwd=str(sejr_path.parent.parent),
            capture_output=True,
            check=True
        )
        print("[GIT] Pushed to remote")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[GIT] Push error: {e}")
        return False

def get_git_status(sejr_path: Path) -> dict:
    """Get git status"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(sejr_path.parent.parent),
            capture_output=True,
            text=True
        )
        return {
            "clean": len(result.stdout.strip()) == 0,
            "changes": len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0,
        }
    except:
        return {"clean": False, "changes": -1}
