#!/usr/bin/env python3
"""
INTRO HOOK - Sync sejr completion to INTRO folder system
"""
from pathlib import Path
from datetime import datetime
import shutil

INTRO_PATH = Path.home() / "Desktop/projekts/status opdaterings rapport/INTRO"

def sync_to_intro(sejr_path: Path, sejr_name: str) -> bool:
    """Sync completed sejr to INTRO folder"""
    if not INTRO_PATH.exists():
        print(f"[INTRO HOOK] INTRO path not found: {INTRO_PATH}")
        return False

    # Find or create appropriate INTRO folder
    target_folder = INTRO_PATH / "99_SEJRLISTE_ARCHIVE"
    target_folder.mkdir(exist_ok=True)

    # Copy conclusion
    conclusion_src = sejr_path / "CONCLUSION.md"
    if conclusion_src.exists():
        conclusion_dst = target_folder / f"{sejr_name}_CONCLUSION.md"
        shutil.copy2(conclusion_src, conclusion_dst)
        print(f"[INTRO HOOK] Synced conclusion to {conclusion_dst}")
        return True

    return False

def get_intro_status() -> dict:
    """Get INTRO system status"""
    return {
        "path": str(INTRO_PATH),
        "exists": INTRO_PATH.exists(),
        "folders": len(list(INTRO_PATH.iterdir())) if INTRO_PATH.exists() else 0,
    }
