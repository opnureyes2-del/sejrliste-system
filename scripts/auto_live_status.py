#!/usr/bin/env python3
"""
AUTO LIVE STATUS - Opdaterer _CURRENT/LIVE_STATUS.md automatisk
================================================================

Viser i realtid:
- HVAD sker der
- HVOR sker det
- HVORFOR gør vi det
- HVORDAN gør vi det
- HVORNÅR er vi færdige

BRUG:
    python auto_live_status.py           # Opdater én gang
    python auto_live_status.py --watch   # Opdater kontinuerligt
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent.parent
ACTIVE_DIR = BASE_DIR / "10_ACTIVE"
ARCHIVE_DIR = BASE_DIR / "90_ARCHIVE"
CURRENT_DIR = BASE_DIR / "_CURRENT"
OUTPUT_FILE = CURRENT_DIR / "LIVE_STATUS.md"

# ═══════════════════════════════════════════════════════════════════════════
# DATA COLLECTION
# ═══════════════════════════════════════════════════════════════════════════

def get_active_processes() -> Dict[str, str]:
    """Find alle kørende processer relateret til Sejrliste"""
    processes = {}

    # Check web app
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:8501"],
            capture_output=True, text=True, timeout=2
        )
        if result.stdout == "200":
            processes["Web App"] = "http://localhost:8501 [KØRER]"
        else:
            processes["Web App"] = "Ikke kørende"
    except:
        processes["Web App"] = "Ikke tilgængelig"

    # Check for running Python processes
    try:
        result = subprocess.run(
            ["pgrep", "-f", "masterpiece.py"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            processes["Desktop App"] = f"PID {result.stdout.strip().split()[0]} [KØRER]"
        else:
            processes["Desktop App"] = "Klar til brug"
    except:
        processes["Desktop App"] = "Ukendt"

    processes["Timeline Services"] = "services/ [AKTIV]"
    processes["Sync Service"] = "unified_sync.py [AKTIV]"

    return processes


def get_active_sejrs() -> List[Dict]:
    """Hent alle aktive sejrs med deres status fra SEJR_LISTE.md filer."""
    sejrs = []

    if not ACTIVE_DIR.exists():
        return sejrs

    for sejr_dir in sorted(ACTIVE_DIR.iterdir()):
        if not sejr_dir.is_dir():
            continue

        sejr_liste = sejr_dir / "SEJR_LISTE.md"
        if not sejr_liste.exists():
            continue

        try:
            content = sejr_liste.read_text(encoding="utf-8")
            # Count checkboxes
            done = content.count("- [x]") + content.count("- [X]")
            total = done + content.count("- [ ]")
            progress = (done / total * 100) if total > 0 else 0

            # Find current pass
            current_pass = 1
            if "## PASS 2" in content:
                current_pass = 2
            if "## PASS 3" in content:
                current_pass = 3

            sejrs.append({
                "name": sejr_dir.name,
                "progress": progress,
                "position": done,
                "total": total,
                "current_step": f"Pass {current_pass}/3",
                "estimated": "—",
                "outcome": "IN_PROGRESS"
            })
        except Exception as e:
            print(f"  Fejl ved {sejr_dir.name}: {e}")

    return sejrs


def get_next_steps(sejrs: List[Dict]) -> List[str]:
    """Hent de næste 3 skridt baseret på aktive sejrs."""
    if not sejrs:
        return ["Opret ny sejr med generate_sejr.py"]

    # Find the sejr closest to completion
    closest = max(sejrs, key=lambda s: s["progress"])

    steps = []
    if closest["progress"] < 100:
        steps.append(f"Færdiggør {closest['name'].split('_2026')[0].replace('_', ' ')}")
    if closest["progress"] >= 80:
        steps.append("Kør verification (auto_verify.py --all)")
    if closest["progress"] >= 95:
        steps.append("Arkiver (auto_archive.py)")
    else:
        steps.append("Fortsæt med checkboxes")
        steps.append("Kør verification for status-check")

    return steps[:3]


def get_current_context() -> Dict:
    """Hent 5W kontekst for nuværende arbejde"""
    context = {
        "HVAD": "Ukendt",
        "HVOR": str(ACTIVE_DIR),
        "HVORFOR": "Ukendt",
        "HVORDAN": "Ukendt",
        "HVORNÅR": "Nu"
    }

    # Try to get from active sejrs
    sejrs = get_active_sejrs()
    if sejrs:
        s = sejrs[0]
        context["HVAD"] = f"{s['name'].replace('_', ' ')} - {s['current_step']}"
        context["HVOR"] = f"{ACTIVE_DIR}/{s['name']}/"
        context["HVORFOR"] = "Opnå GRAND ADMIRAL status"
        context["HVORDAN"] = "20-skridt workflow med 3-pass system"

        try:
            est = datetime.fromisoformat(s["estimated"])
            context["HVORNÅR"] = f"Nu → {est.strftime('%H:%M')}"
        except:
            context["HVORNÅR"] = "Nu → Snart"

    return context


def get_folder_files() -> List[Dict]:
    """Hent filer i _CURRENT mappe"""
    files = []

    for f in CURRENT_DIR.iterdir():
        if f.is_file():
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            files.append({
                "name": f.name,
                "purpose": get_file_purpose(f.name),
                "modified": mtime.strftime("%H:%M")
            })

    return sorted(files, key=lambda x: x["name"])


def get_file_purpose(filename: str) -> str:
    """Beskriv formålet med en fil"""
    purposes = {
        "STATE.md": "System state overview",
        "LIVE_STATUS.md": "Live status (denne fil)",
        "PATTERNS.json": "Lærte mønstre fra sejrs",
        "DELTA.md": "Hvad er ændret siden sidst",
        "NEXT.md": "Forudsagte næste skridt",
        "OPTIMIZED_PROMPT.md": "Optimeret prompt template",
        "LEARNED_TIPS.md": "Tips fra tidligere sejrs",
    }
    return purposes.get(filename, "System fil")


# ═══════════════════════════════════════════════════════════════════════════
# MARKDOWN GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def generate_live_status() -> str:
    """Generér komplet LIVE_STATUS.md indhold"""
    now = datetime.now()
    processes = get_active_processes()
    sejrs = get_active_sejrs()
    context = get_current_context()
    next_steps = get_next_steps(sejrs)
    files = get_folder_files()

    lines = []

    # Header
    lines.append("# 🔴 LIVE STATUS - Opdateres Automatisk")
    lines.append("")
    lines.append(f"> Sidste opdatering: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 5W Context
    lines.append("## 🎯 HVAD SKER DER NU?")
    lines.append("")
    lines.append("| Aspekt | Status |")
    lines.append("|--------|--------|")
    for key, value in context.items():
        lines.append(f"| **{key}** | {value} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Active Processes
    lines.append("## 🏃 AKTIVE PROCESSER")
    lines.append("")
    lines.append("```")
    for name, status in processes.items():
        lines.append(f"{name:15} {status}")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Progress
    lines.append("## 📊 PROGRESS")
    lines.append("")
    lines.append("| Sejr | Progress | Skridt | Status |")
    lines.append("|------|----------|--------|--------|")
    for s in sejrs:
        name = s["name"][:30]
        lines.append(f"| {name} | {s['progress']:.0f}% | {s['position']}/{s['total']} | {s['current_step']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Next Steps
    lines.append("## 🔮 NÆSTE SKRIDT")
    lines.append("")
    for i, step in enumerate(next_steps, 1):
        marker = "← NU" if i == 1 else ""
        lines.append(f"{i}. **{step}** {marker}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Files
    lines.append("## 📁 FILER I DENNE MAPPE")
    lines.append("")
    lines.append("| Fil | Formål | Sidst Ændret |")
    lines.append("|-----|--------|--------------|")
    for f in files:
        lines.append(f"| `{f['name']}` | {f['purpose']} | {f['modified']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Direct Links
    lines.append("## 🔗 DIREKTE LINKS")
    lines.append("")
    lines.append("- **Web App:** [http://localhost:8501](http://localhost:8501)")
    if sejrs:
        lines.append(f"- **Aktiv Sejr:** [10_ACTIVE/{sejrs[0]['name']}/](../10_ACTIVE/{sejrs[0]['name']}/)")
    lines.append("- **Tidslinjer:** `python services/complete_timeline.py --all`")
    lines.append("- **Workflow:** `python services/active_workflow.py`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Auto-genereret af auto_live_status.py*")

    return "\n".join(lines)


def update_live_status():
    """Opdater LIVE_STATUS.md filen"""
    content = generate_live_status()
    OUTPUT_FILE.write_text(content)
    print(f"✅ LIVE_STATUS.md opdateret: {datetime.now().strftime('%H:%M:%S')}")


def watch_mode():
    """Kør i watch mode - opdater hvert 10. sekund"""
    import time

    print("🔴 LIVE STATUS WATCH MODE")
    print("   Opdaterer hvert 10. sekund")
    print("   Ctrl+C for at stoppe")
    print()

    try:
        while True:
            update_live_status()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n⏹️ Stoppet")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if "--watch" in sys.argv:
        watch_mode()
    else:
        update_live_status()
