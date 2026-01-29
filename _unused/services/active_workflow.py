#!/usr/bin/env python3
"""
ACTIVE WORKFLOW - Bruger Alt I Realtid
======================================

Dette script integrerer ALLE services i den aktive udviklingsproces.
Det er IKKE en demo - det er et arbejdsværktøj.

BRUG:
    python active_workflow.py              # Vis nuværende status
    python active_workflow.py --next       # Hvad er næste skridt?
    python active_workflow.py --done       # Marker nuværende som færdig
    python active_workflow.py --predict    # Vis ugens forudsigelser
    python active_workflow.py --start NAME # Start ny sejr
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Setup paths
BASE_DIR = Path("/home/rasmus/Desktop/sejrliste systemet")
ACTIVE_DIR = BASE_DIR / "10_ACTIVE"
SERVICES_DIR = BASE_DIR / "services"

sys.path.insert(0, str(SERVICES_DIR))

from complete_timeline import TimelineGenerator, visualize_timeline
from unified_sync import PredictiveEngine, UnifiedDragDrop

# ═══════════════════════════════════════════════════════════════════════════
# CORE WORKFLOW FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def get_current_work() -> dict:
    """Hvad arbejder vi på LIGE NU?"""
    generator = TimelineGenerator()

    current = None
    highest_progress = -1

    for sejr_dir in ACTIVE_DIR.iterdir():
        if sejr_dir.is_dir():
            timeline = generator.generate_sejr_timeline(sejr_dir)

            # Find den sejr vi er tættest på at færdiggøre
            if timeline.current_position > 0:
                progress = timeline.progress_percentage
                if progress > highest_progress and progress < 100:
                    highest_progress = progress
                    current = {
                        "name": timeline.sejr_name,
                        "path": str(sejr_dir),
                        "position": timeline.current_position,
                        "total_steps": timeline.total_steps,
                        "progress": timeline.progress_percentage,
                        "estimated_completion": timeline.estimated_completion,
                        "final_outcome": timeline.final_outcome,
                        "current_step": timeline.steps[timeline.current_position - 1] if timeline.current_position > 0 else None,
                        "next_step": timeline.steps[timeline.current_position] if timeline.current_position < len(timeline.steps) else None
                    }

    return current


def show_current_status():
    """Vis nuværende arbejdsstatus"""
    current = get_current_work()

    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║               📋 AKTIV ARBEJDSSTATUS                          ║")
    print("╠═══════════════════════════════════════════════════════════════╣")

    if current:
        print(f"║  Arbejder på: {current['name']:<46} ║")
        print(f"║  Progress: {current['progress']:.1f}% (skridt {current['position']}/{current['total_steps']}) ║")

        if current.get('current_step'):
            step = current['current_step']
            print("╠═══════════════════════════════════════════════════════════════╣")
            print(f"║  🔵 NU: {step.name:<52} ║")
            print(f"║     {step.description:<55} ║")

        if current.get('next_step'):
            step = current['next_step']
            print("╠═══════════════════════════════════════════════════════════════╣")
            print(f"║  ⏳ NÆSTE: {step.name:<49} ║")
            print(f"║     {step.description:<55} ║")

        print("╠═══════════════════════════════════════════════════════════════╣")
        print(f"║  🎯 Forventet: {current['final_outcome'][:45]:<45} ║")
    else:
        print("║  Ingen aktiv sejr fundet.                                     ║")
        print("║  Brug: python active_workflow.py --start NAVN                 ║")

    print("╚═══════════════════════════════════════════════════════════════╝")
    print()


def show_next_steps():
    """Hvad er de næste 5 skridt?"""
    current = get_current_work()

    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║               🔮 NÆSTE SKRIDT                                  ║")
    print("╠═══════════════════════════════════════════════════════════════╣")

    if current:
        engine = PredictiveEngine()
        steps = engine.get_next_steps(current['name'])

        for step in steps:
            print(f"║  {step:<60} ║")
    else:
        print("║  Ingen aktiv sejr - start en ny først                         ║")

    print("╚═══════════════════════════════════════════════════════════════╝")
    print()


def show_week_predictions():
    """Vis forudsigelser for næste uge"""
    engine = PredictiveEngine()
    visions = engine.analyze_week_ahead()

    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║               📅 DE NÆSTE 7 DAGE                               ║")
    print("╠═══════════════════════════════════════════════════════════════╣")

    for v in visions:
        date = datetime.strptime(v.date, "%Y-%m-%d")
        weekday = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"][date.weekday()]
        date_str = date.strftime("%d/%m")

        print(f"║  {weekday} {date_str}:                                                  ║")

        if v.predicted_sejrs:
            for s in v.predicted_sejrs[:2]:
                print(f"║    📋 {s[:53]:<53} ║")

        if v.recommended_actions:
            for a in v.recommended_actions[:2]:
                print(f"║    → {a[:54]:<54} ║")

        if not v.predicted_sejrs and not v.recommended_actions:
            print("║    (ingen planlagte opgaver)                                ║")

        print("║                                                               ║")

    print("╚═══════════════════════════════════════════════════════════════╝")
    print()


def start_new_sejr(name: str, goal: Optional[str] = None):
    """Start en ny sejr"""
    import subprocess

    script = BASE_DIR / "scripts" / "generate_sejr.py"

    args = ["python3", str(script), "--name", name]
    if goal:
        args.extend(["--goal", goal])

    print(f"Opretter ny sejr: {name}...")
    result = subprocess.run(args, capture_output=True, text=True, cwd=str(BASE_DIR))

    if result.returncode == 0:
        print(f"✅ Sejr '{name}' oprettet!")

        # Vis næste skridt
        engine = PredictiveEngine()
        steps = engine.get_next_steps(name)

        print("\n🔮 Næste skridt:")
        for step in steps[:3]:
            print(f"  → {step}")
    else:
        print(f"❌ Fejl: {result.stderr}")


def mark_current_done():
    """Log at current skridt er færdigt"""
    current = get_current_work()

    if not current:
        print("Ingen aktiv sejr fundet.")
        return

    # Log to AUTO_LOG.jsonl
    log_file = Path(current['path']) / "AUTO_LOG.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": "STEP_COMPLETE",
        "step": current['position'],
        "step_name": current.get('current_step', {}).name if current.get('current_step') else "unknown",
        "actor": "active_workflow"
    }

    with open(log_file, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"✅ Skridt {current['position']} markeret som færdigt!")
    print(f"   Logged til: {log_file}")

    # Show next step
    if current.get('next_step'):
        print(f"\n⏳ Næste skridt: {current['next_step'].name}")
        print(f"   {current['next_step'].description}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        show_current_status()
        return

    cmd = sys.argv[1]

    if cmd == "--next":
        show_next_steps()

    elif cmd == "--predict":
        show_week_predictions()

    elif cmd == "--done":
        mark_current_done()

    elif cmd == "--start" and len(sys.argv) > 2:
        name = sys.argv[2]
        goal = sys.argv[3] if len(sys.argv) > 3 else None
        start_new_sejr(name, goal)

    elif cmd == "--help":
        print(__doc__)

    else:
        show_current_status()


if __name__ == "__main__":
    main()
