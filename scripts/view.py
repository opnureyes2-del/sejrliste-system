#!/usr/bin/env python3
"""
SEJRLISTE VIEWER - Simpel terminal visning
===========================================

Viser status for aktive sejr lister.
INGEN dependencies - kun Python standard library.

Brug: python view.py
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Import centralized YAML parser
sys.path.insert(0, str(Path(__file__).parent))
from yaml_utils import parse_yaml_simple

# Paths — project root is one level up from scripts/
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
ACTIVE_DIR = PROJECT_DIR / "10_ACTIVE"
CURRENT_DIR = PROJECT_DIR / "_CURRENT"

def clear_screen():
    """Clear terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

# parse_yaml_simple imported from yaml_utils (centralized PyYAML parser)

def parse_checkboxes(filepath: Path) -> tuple:
    """Parse checkboxes from SEJR_LISTE.md. Returns (done, total)."""
    if not filepath.exists():
        return 0, 0

    content = filepath.read_text(encoding="utf-8")

    # Find all checkboxes: - [x] or - [ ]
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))

    return checked, checked + unchecked

def parse_log(filepath: Path) -> list:
    """Parse AUTO_LOG.jsonl. Returns last 5 entries."""
    if not filepath.exists():
        return []

    entries = []
    content = filepath.read_text(encoding="utf-8")

    for line in content.strip().split("\n"):
        if line.strip():
            try:
                entry = json.loads(line)
                entries.append(entry)
            except Exception:
                pass

    return entries[-5:]  # Last 5

def format_timestamp(ts: str) -> str:
    """Format timestamp to HH:MM."""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%H:%M")
    except Exception:
        return ts[:5] if ts else "??:??"

def print_box(title: str, content: list, width: int = 50):
    """Print a simple box."""
    print("┌" + "─" * (width - 2) + "┐")
    print("│" + f" {title}".ljust(width - 2) + "│")
    print("├" + "─" * (width - 2) + "┤")

    for line in content:
        text = line[:width - 4]
        print("│ " + text.ljust(width - 4) + " │")

    if not content:
        print("│ " + "(ingen data)".ljust(width - 4) + " │")

    print("└" + "─" * (width - 2) + "┘")

def progress_bar(done: int, total: int, width: int = 20) -> str:
    """Create ASCII progress bar."""
    if total == 0:
        return "░" * width + " 0%"

    pct = done / total
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"{bar} {int(pct * 100)}%"

def find_active_sejr() -> list:
    """Find all active sejr folders."""
    if not ACTIVE_DIR.exists():
        return []

    sejr_list = []
    for d in ACTIVE_DIR.iterdir():
        if d.is_dir() and (d / "SEJR_LISTE.md").exists():
            sejr_list.append(d)

    return sorted(sejr_list, key=lambda x: x.name, reverse=True)

def display_sejr(sejr_path: Path):
    """Display status for a single sejr with 3-PASS tracking."""
    name = sejr_path.name

    # Parse files
    status = parse_yaml_simple(sejr_path / "STATUS.yaml")
    done, total = parse_checkboxes(sejr_path / "SEJR_LISTE.md")
    logs = parse_log(sejr_path / "AUTO_LOG.jsonl")

    # 3-PASS Status
    current_pass = status.get("current_pass", 1)
    pass_1_score = status.get("pass_1_score", 0)
    pass_2_score = status.get("pass_2_score", 0)
    pass_3_score = status.get("pass_3_score", 0)
    total_score = status.get("total_score", 0)
    can_archive = status.get("can_archive", False)

    # Status line
    completion = status.get("completion_percentage", 0)
    if isinstance(completion, str):
        try:
            completion = int(float(completion))
        except Exception:
            completion = 0

    status_text = status.get("status", "unknown")

    # Color codes (ANSI)
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    if completion >= 100:
        color = GREEN
        status_icon = "[OK]"
    elif completion >= 50:
        color = YELLOW
        status_icon = "[ACTIVE]"
    else:
        color = RED
        status_icon = "[PENDING]"

    # Print header
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD} SEJR: {name}{RESET}")
    print(f"{'=' * 60}")

    # 3-PASS Status
    pass_icons = ["[PENDING]", "[PENDING]", "[PENDING]"]
    if current_pass >= 1 and pass_1_score > 0:
        pass_icons[0] = "[OK]"
    if current_pass >= 2 and pass_2_score > 0:
        pass_icons[1] = "[OK]"
    if current_pass >= 3 and pass_3_score > 0:
        pass_icons[2] = "[OK]"
    if current_pass == 1:
        pass_icons[0] = "[ACTIVE]"
    elif current_pass == 2:
        pass_icons[1] = "[ACTIVE]"
    elif current_pass == 3:
        pass_icons[2] = "[ACTIVE]"

    print(f"\n [TARGET] 3-PASS KONKURRENCE:")
    print(f"    {pass_icons[0]} Pass 1 (Planlægning):  {pass_1_score}/10")
    print(f"    {pass_icons[1]} Pass 2 (Eksekvering):  {pass_2_score}/10")
    print(f"    {pass_icons[2]} Pass 3 (7-DNA Review): {pass_3_score}/10")
    print(f"    {'─' * 30}")
    print(f"     Total: {total_score}/30 {'[OK] Klar til arkiv' if can_archive else '[LOCK] Blokeret'}")

    # Status
    print(f"\n {status_icon} Status: {color}{status_text}{RESET}")
    print(f" [DATA] Progress: {progress_bar(done, total)}")
    print(f" [OK] Tasks: {done}/{total} done")

    # Phases (simplified)
    phases = status.get("phases_complete", {})
    if phases:
        print(f"\n Phases:")
        phase_names = ["optimization", "planning", "development", "verification", "git_workflow"]
        for phase in phase_names:
            is_done = phases.get(phase, False) if isinstance(phases, dict) else False
            icon = f"{GREEN}[OK]{RESET}" if is_done else "○"
            print(f"   {icon} {phase.replace('_', ' ').title()}")

    # Recent log
    if logs:
        print(f"\n Recent Activity:")
        for log in logs[-3:]:
            time = format_timestamp(log.get("timestamp", ""))
            action = log.get("action", "unknown")
            print(f"   {time} - {action}")

    print()

def main():
    """Main display loop."""
    clear_screen()

    print("\n" + "=" * 60)
    print(" SEJRLISTE SYSTEM - Status Viewer")
    print(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    # Find active sejr
    active_sejr = find_active_sejr()

    if not active_sejr:
        print("\n Ingen aktive sejr i 10_ACTIVE/")
        print("\n Opret en ny med:")
        print('   python scripts/generate_sejr.py --name "Dit Projekt"')
        print()
        return

    print(f"\n [FOLDER] Fundet {len(active_sejr)} aktiv(e) sejr:\n")

    # Display each sejr
    for sejr_path in active_sejr:
        display_sejr(sejr_path)

    # Quick commands
    print("-" * 60)
    print(" HURTIGE KOMMANDOER:")
    print("-" * 60)
    print(" python scripts/generate_sejr.py --name \"Navn\"  # Ny sejr")
    print(" python scripts/auto_verify.py --all            # Verificer")
    print(" python scripts/auto_archive.py --list          # Se færdige")
    print(" python scripts/view.py                         # Denne visning")
    print("-" * 60)
    print()

if __name__ == "__main__":
    main()
