#!/usr/bin/env python3
"""
Update CLAUDE.md focus lock based on current state
Part of SEJR LISTE SYSTEM - FOKUS ENFORCEMENT

Opdaterer CLAUDE.md med:
- Current pass
- Next action
- Scores
- Blockers

Kør automatisk efter verify eller manuelt.
"""

import re
import sys
import yaml
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from yaml_utils import parse_yaml_simple


def find_next_action(sejr_path: Path, current_pass: int) -> str:
    """Find the next unchecked checkbox in SEJR_LISTE.md."""
    sejr_file = sejr_path / "SEJR_LISTE.md"

    if not sejr_file.exists():
        return "Åbn SEJR_LISTE.md"

    content = sejr_file.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Find unchecked checkboxes
    for i, line in enumerate(lines):
        if re.match(r'^- \[ \]', line.strip()):
            # Get the task text
            task = line.strip()[6:].strip()  # Remove "- [ ] "
            if task:
                return task[:80] + "..." if len(task) > 80 else task

    # If all checked in current pass, suggest next step
    if current_pass == 1:
        return "Pass 1 færdig - Udfyld REVIEW sektion og start Pass 2"
    elif current_pass == 2:
        return "Pass 2 færdig - Udfyld REVIEW sektion og start Pass 3"
    else:
        return "Pass 3 færdig - Gennemgå 7-DNA checkliste og arkiver"


def determine_blocker(status: dict) -> str:
    """Determine what's blocking progress."""
    if not status.get("pass_1_complete", False):
        return "Færdiggør alle checkboxes i Pass 1"

    if not status.get("pass_2_complete", False):
        if status.get("pass_2_score", 0) <= status.get("pass_1_score", 0):
            return f"Pass 2 score ({status.get('pass_2_score', 0)}) skal være > Pass 1 ({status.get('pass_1_score', 0)})"
        return "Færdiggør alle checkboxes i Pass 2"

    if not status.get("pass_3_complete", False):
        if status.get("pass_3_score", 0) <= status.get("pass_2_score", 0):
            return f"Pass 3 score ({status.get('pass_3_score', 0)}) skal være > Pass 2 ({status.get('pass_2_score', 0)})"
        return "Færdiggør 7-DNA gennemgang i Pass 3"

    if not status.get("final_verification_complete", False):
        return "Gennemfør final verification (5+ tests)"

    if status.get("total_score", 0) < 24:
        return f"Total score for lav ({status.get('total_score', 0)}/30, minimum 24)"

    return "INTET - Klar til arkivering!"


def update_claude_md(sejr_path: Path):
    """Update CLAUDE.md with current state."""
    status_file = sejr_path / "STATUS.yaml"
    claude_file = sejr_path / "CLAUDE.md"
    template_path = sejr_path.parent.parent / "00_TEMPLATES" / "CLAUDE.md"

    # Get current status
    status = parse_yaml_simple(status_file)

    if not status:
        print(f"[WARN]  No STATUS.yaml found in {sejr_path}")
        return False

    # Read template
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
    elif claude_file.exists():
        content = claude_file.read_text(encoding="utf-8")
    else:
        print(f"[WARN]  No CLAUDE.md template found")
        return False

    # Determine values
    current_pass = status.get("current_pass", 1)
    sejr_name = status.get("sejr_name", sejr_path.name)

    pass_status = ["⏳ Pending", "⏳ Pending", "⏳ Pending"]
    if current_pass == 1:
        pass_status[0] = " In Progress"
    elif current_pass == 2:
        pass_status[0] = "[OK] Complete"
        pass_status[1] = " In Progress"
    elif current_pass == 3:
        pass_status[0] = "[OK] Complete"
        pass_status[1] = "[OK] Complete"
        pass_status[2] = " In Progress"

    if status.get("pass_1_complete"):
        pass_status[0] = "[OK] Complete"
    if status.get("pass_2_complete"):
        pass_status[1] = "[OK] Complete"
    if status.get("pass_3_complete"):
        pass_status[2] = "[OK] Complete"

    # Status text
    if status.get("can_archive"):
        status_text = "[OK] KLAR TIL ARKIVERING"
    else:
        status_text = f"Pass {current_pass} - " + ["", "Planlægning", "Eksekvering", "7-DNA Review"][current_pass]

    # Replace placeholders
    replacements = {
        "{SEJR_NAVN}": sejr_name,
        "{CURRENT_PASS}": str(current_pass),
        "{STATUS}": status_text,
        "{BLOCKER}": determine_blocker(status),
        "{NEXT_ACTION}": find_next_action(sejr_path, current_pass),
        "{PASS_1_STATUS}": pass_status[0],
        "{PASS_1_SCORE}": str(status.get("pass_1_score", 0)),
        "{PASS_2_STATUS}": pass_status[1],
        "{PASS_2_SCORE}": str(status.get("pass_2_score", 0)),
        "{PASS_3_STATUS}": pass_status[2],
        "{PASS_3_SCORE}": str(status.get("pass_3_score", 0)),
        "{TOTAL_SCORE}": str(status.get("total_score", 0)),
        "{TIMESTAMP}": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    # Write updated CLAUDE.md
    claude_file.write_text(content, encoding="utf-8")
    print(f"[OK] Updated: {claude_file}")

    # Print summary
    print(f"\n{'─' * 40}")
    print(f" CLAUDE FOKUS OPDATERET")
    print(f"{'─' * 40}")
    print(f"   Sejr: {sejr_name}")
    print(f"   Pass: {current_pass}/3")
    print(f"   Status: {status_text}")
    print(f"   Score: {status.get('total_score', 0)}/30")
    print(f"   Næste: {find_next_action(sejr_path, current_pass)[:50]}...")
    print(f"{'─' * 40}\n")

    return True


def update_all(system_path: Path):
    """Update CLAUDE.md for all active sejr."""
    active_dir = system_path / "10_ACTIVE"

    if not active_dir.exists():
        print("[FAIL] No 10_ACTIVE directory")
        return

    sejr_folders = [f for f in active_dir.iterdir() if f.is_dir()]

    if not sejr_folders:
        print("[INFO]  No active sejr found")
        return

    print(f" Updating CLAUDE.md for {len(sejr_folders)} sejr...\n")

    for sejr_path in sejr_folders:
        update_claude_md(sejr_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Update CLAUDE.md focus lock based on current state"
    )
    parser.add_argument("--sejr", help="Specific sejr folder name")
    parser.add_argument("--all", action="store_true", help="Update all active sejr")
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent

    if args.all:
        update_all(system_path)
    elif args.sejr:
        sejr_path = system_path / "10_ACTIVE" / args.sejr
        if sejr_path.exists():
            update_claude_md(sejr_path)
        else:
            print(f"[FAIL] Sejr not found: {sejr_path}")
    else:
        update_all(system_path)
