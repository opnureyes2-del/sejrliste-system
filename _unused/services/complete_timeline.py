#!/usr/bin/env python3
"""
COMPLETE TIMELINE - Se ALLE Skridt Fra Nu Til Afslutning
========================================================

PRINCIP: At se ALLE de skridt der endnu ikke er gået,
         og dem der ender, NÅR de ender,
         og se tydeligt HVORDAN de ender.

Dette viser:
1. Hvor du er NU
2. ALLE skridt der mangler
3. HVORNÅR hvert skridt ender
4. HVORDAN det hele ender (det endelige resultat)
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

BASE_DIR = Path("/home/rasmus/Desktop/sejrliste systemet")
ACTIVE_DIR = BASE_DIR / "10_ACTIVE"
ARCHIVE_DIR = BASE_DIR / "90_ARCHIVE"

# ═══════════════════════════════════════════════════════════════════════════
# STEP DEFINITION - ALLE MULIGE SKRIDT
# ═══════════════════════════════════════════════════════════════════════════

class StepStatus(Enum):
    DONE = "[OK]"
    CURRENT = ""
    PENDING = "⏳"
    BLOCKED = ""


@dataclass
class TimelineStep:
    """Et enkelt skridt på tidslinjen"""
    number: int
    name: str
    description: str
    status: StepStatus
    estimated_end: Optional[str] = None  # ISO datetime
    actual_end: Optional[str] = None
    dependencies: List[str] = None
    outputs: List[str] = None  # Hvad producerer dette skridt

    def to_dict(self) -> Dict:
        d = asdict(self)
        d['status'] = self.status.value
        return d


@dataclass
class SejrTimeline:
    """Komplet tidslinje for én sejr"""
    sejr_name: str
    created: str
    current_position: int  # Hvilket skridt er vi på nu
    total_steps: int
    estimated_completion: str  # Hvornår ender det hele
    final_outcome: str  # HVORDAN ender det
    steps: List[TimelineStep]
    progress_percentage: float

    def to_dict(self) -> Dict:
        d = asdict(self)
        d['steps'] = [s.to_dict() for s in self.steps]
        return d


# ═══════════════════════════════════════════════════════════════════════════
# MASTER STEP TEMPLATE - DE 17 SKRIDT TIL GRAND ADMIRAL
# ═══════════════════════════════════════════════════════════════════════════

MASTER_STEPS = [
    # PASS 1: PLANLÆGNING (Skridt 1-5)
    {
        "number": 1,
        "name": "Oprettelse",
        "description": "Sejr oprettet med navn og mål",
        "phase": "PASS_1",
        "typical_duration_minutes": 2,
        "outputs": ["SEJR_LISTE.md", "STATUS.yaml", "CLAUDE.md"]
    },
    {
        "number": 2,
        "name": "Mål Defineret",
        "description": "Hvad skal opnås? Hvad er success?",
        "phase": "PASS_1",
        "typical_duration_minutes": 10,
        "outputs": ["Klart mål i SEJR_LISTE.md"]
    },
    {
        "number": 3,
        "name": "Opgaver Listet",
        "description": "Alle checkboxes tilføjet",
        "phase": "PASS_1",
        "typical_duration_minutes": 15,
        "outputs": ["Checkboxes i SEJR_LISTE.md"]
    },
    {
        "number": 4,
        "name": "Afhængigheder Identificeret",
        "description": "Hvad blokerer hvad?",
        "phase": "PASS_1",
        "typical_duration_minutes": 5,
        "outputs": ["Rækkefølge af opgaver"]
    },
    {
        "number": 5,
        "name": "Pass 1 Review",
        "description": "Gennemgang af plan - er den komplet?",
        "phase": "PASS_1",
        "typical_duration_minutes": 10,
        "outputs": ["pass_1_complete: true"]
    },

    # PASS 2: EKSEKVERING (Skridt 6-11)
    {
        "number": 6,
        "name": "Første Checkbox",
        "description": "Start på implementering",
        "phase": "PASS_2",
        "typical_duration_minutes": 30,
        "outputs": ["Første checkbox afkrydset"]
    },
    {
        "number": 7,
        "name": "Kode Skrevet",
        "description": "Hovedimplementering færdig",
        "phase": "PASS_2",
        "typical_duration_minutes": 120,
        "outputs": ["Kode filer", "Funktionalitet"]
    },
    {
        "number": 8,
        "name": "Tests Bestået",
        "description": "Minimum 5 tests passed",
        "phase": "PASS_2",
        "typical_duration_minutes": 30,
        "outputs": ["test_passed: 5+"]
    },
    {
        "number": 9,
        "name": "Dokumentation",
        "description": "Kode og brug dokumenteret",
        "phase": "PASS_2",
        "typical_duration_minutes": 20,
        "outputs": ["README", "docstrings"]
    },
    {
        "number": 10,
        "name": "Alle Checkboxes",
        "description": "Alle opgaver afkrydset",
        "phase": "PASS_2",
        "typical_duration_minutes": 60,
        "outputs": ["completion_percentage: 100"]
    },
    {
        "number": 11,
        "name": "Pass 2 Review",
        "description": "Virker det? Er det komplet?",
        "phase": "PASS_2",
        "typical_duration_minutes": 15,
        "outputs": ["pass_2_complete: true"]
    },

    # PASS 3: 7-DNA REVIEW (Skridt 12-18)
    {
        "number": 12,
        "name": "DNA Lag 1: Self-Aware",
        "description": "Kender systemet sig selv?",
        "phase": "PASS_3",
        "typical_duration_minutes": 5,
        "outputs": ["DNA.yaml verificeret"]
    },
    {
        "number": 13,
        "name": "DNA Lag 2: Self-Documenting",
        "description": "Er alt logget?",
        "phase": "PASS_3",
        "typical_duration_minutes": 5,
        "outputs": ["AUTO_LOG.jsonl komplet"]
    },
    {
        "number": 14,
        "name": "DNA Lag 3: Self-Verifying",
        "description": "Er alt testet?",
        "phase": "PASS_3",
        "typical_duration_minutes": 10,
        "outputs": ["Alle tests passed"]
    },
    {
        "number": 15,
        "name": "DNA Lag 4: Self-Improving",
        "description": "Har vi lært noget?",
        "phase": "PASS_3",
        "typical_duration_minutes": 10,
        "outputs": ["PATTERNS.json opdateret"]
    },
    {
        "number": 16,
        "name": "DNA Lag 5-7",
        "description": "Archiving, Predictive, Self-Optimizing",
        "phase": "PASS_3",
        "typical_duration_minutes": 15,
        "outputs": ["7 DNA lag verified"]
    },
    {
        "number": 17,
        "name": "Final Verification",
        "description": "Score ≥ 24/30 bekræftet",
        "phase": "PASS_3",
        "typical_duration_minutes": 5,
        "outputs": ["final_verification_complete: true"]
    },

    # AFSLUTNING (Skridt 18-20)
    {
        "number": 18,
        "name": "Arkivering",
        "description": "Flyt til 90_ARCHIVE med CONCLUSION.md",
        "phase": "ARCHIVE",
        "typical_duration_minutes": 5,
        "outputs": ["90_ARCHIVE/{sejr}/CONCLUSION.md"]
    },
    {
        "number": 19,
        "name": "Context Opdateret",
        "description": "Session og journal opdateret",
        "phase": "ARCHIVE",
        "typical_duration_minutes": 2,
        "outputs": ["session.md", "journal.md"]
    },
    {
        "number": 20,
        "name": "GRAND ADMIRAL",
        "description": " Sejr komplet - Rang opnået",
        "phase": "COMPLETE",
        "typical_duration_minutes": 0,
        "outputs": ["GRAND ADMIRAL status"]
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# TIMELINE GENERATOR
# ═══════════════════════════════════════════════════════════════════════════

class TimelineGenerator:
    """Genererer komplet tidslinje for alle sejrs"""

    def __init__(self):
        self.steps_template = MASTER_STEPS

    def generate_sejr_timeline(self, sejr_path: Path) -> SejrTimeline:
        """Generér komplet tidslinje for én sejr"""
        status_file = sejr_path / "STATUS.yaml"
        sejr_name = sejr_path.name

        # Læs nuværende status
        status = self._read_status(status_file)

        # Bestem nuværende position
        current_position = self._determine_position(status)

        # Generer alle skridt med status
        steps = self._generate_steps(status, current_position)

        # Beregn estimeret afslutning
        estimated_completion = self._estimate_completion(current_position)

        # Bestem det endelige resultat
        final_outcome = self._predict_outcome(status)

        return SejrTimeline(
            sejr_name=sejr_name,
            created=status.get("created", datetime.now().isoformat()),
            current_position=current_position,
            total_steps=len(steps),
            estimated_completion=estimated_completion,
            final_outcome=final_outcome,
            steps=steps,
            progress_percentage=round((current_position / len(steps)) * 100, 1)
        )

    def _read_status(self, status_file: Path) -> Dict:
        """Læs STATUS.yaml"""
        if not status_file.exists():
            return {}

        try:
            content = status_file.read_text()
            status = {}
            for line in content.split("\n"):
                if ":" in line and not line.strip().startswith("#"):
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    if value.isdigit():
                        value = int(value)
                    elif value.lower() in ("true", "false"):
                        value = value.lower() == "true"
                    status[key] = value
            return status
        except:
            return {}

    def _determine_position(self, status: Dict) -> int:
        """Bestem hvilket skridt vi er på baseret på status"""
        current_pass = status.get("current_pass", 1)
        pass_1_complete = status.get("pass_1_complete", False)
        pass_2_complete = status.get("pass_2_complete", False)
        pass_3_complete = status.get("pass_3_complete", False)
        final_complete = status.get("final_verification_complete", False)
        completion_pct = status.get("completion_percentage", 0)

        # Arkiveret?
        if final_complete:
            return 20  # GRAND ADMIRAL

        # Pass 3?
        if pass_2_complete and current_pass >= 3:
            if pass_3_complete:
                return 17  # Final verification
            return 12 + (completion_pct // 20)  # Skridt 12-16

        # Pass 2?
        if pass_1_complete and current_pass >= 2:
            if pass_2_complete:
                return 11  # Pass 2 review
            return 6 + min(4, completion_pct // 25)  # Skridt 6-10

        # Pass 1
        if completion_pct >= 80:
            return 5  # Pass 1 review
        elif completion_pct >= 60:
            return 4
        elif completion_pct >= 40:
            return 3
        elif completion_pct >= 20:
            return 2
        else:
            return 1

    def _generate_steps(self, status: Dict, current_position: int) -> List[TimelineStep]:
        """Generer alle skridt med korrekt status"""
        steps = []
        now = datetime.now()

        cumulative_minutes = 0

        for template in self.steps_template:
            number = template["number"]

            # Bestem status
            if number < current_position:
                step_status = StepStatus.DONE
                estimated_end = None
                actual_end = now.isoformat()  # Approximation
            elif number == current_position:
                step_status = StepStatus.CURRENT
                estimated_end = (now + timedelta(minutes=template["typical_duration_minutes"])).isoformat()
                actual_end = None
            else:
                step_status = StepStatus.PENDING
                cumulative_minutes += template["typical_duration_minutes"]
                estimated_end = (now + timedelta(minutes=cumulative_minutes)).isoformat()
                actual_end = None

            steps.append(TimelineStep(
                number=number,
                name=template["name"],
                description=template["description"],
                status=step_status,
                estimated_end=estimated_end,
                actual_end=actual_end,
                dependencies=[],
                outputs=template.get("outputs", [])
            ))

        return steps

    def _estimate_completion(self, current_position: int) -> str:
        """Estimér hvornår sejren er færdig"""
        remaining_minutes = 0
        for template in self.steps_template:
            if template["number"] >= current_position:
                remaining_minutes += template["typical_duration_minutes"]

        completion_time = datetime.now() + timedelta(minutes=remaining_minutes)
        return completion_time.isoformat()

    def _predict_outcome(self, status: Dict) -> str:
        """Forudsig det endelige resultat"""
        total_score = status.get("total_score", 0)
        current_pass = status.get("current_pass", 1)

        if total_score >= 28:
            return " GRAND ADMIRAL (28-30 points) - Exceptionel kvalitet, alt dokumenteret og testet"
        elif total_score >= 24:
            return " ADMIRAL (24-27 points) - Høj kvalitet, alle krav opfyldt"
        elif total_score >= 18:
            return " KOMMANDØR (18-23 points) - God kvalitet, enkelte mangler"
        elif total_score >= 12:
            return " KAPTAJN (12-17 points) - Acceptabel kvalitet, forbedring mulig"
        else:
            # Forudsig baseret på pass
            if current_pass == 3:
                return " ADMIRAL forventet - Pass 3 i gang"
            elif current_pass == 2:
                return " KOMMANDØR forventet - Implementering i gang"
            else:
                return " KADET - Planlægning i gang, potentiale til GRAND ADMIRAL"


# ═══════════════════════════════════════════════════════════════════════════
# VISUALISERING
# ═══════════════════════════════════════════════════════════════════════════

def visualize_timeline(timeline: SejrTimeline) -> str:
    """Generer visual ASCII tidslinje"""
    lines = []

    lines.append("╔" + "═" * 78 + "╗")
    lines.append(f"║   KOMPLET TIDSLINJE: {timeline.sejr_name:<52} ║")
    lines.append("╠" + "═" * 78 + "╣")

    # Progress bar
    progress_bar_width = 50
    filled = int((timeline.progress_percentage / 100) * progress_bar_width)
    bar = "█" * filled + "░" * (progress_bar_width - filled)
    lines.append(f"║ Progress: [{bar}] {timeline.progress_percentage:>5.1f}% ║")
    lines.append("╠" + "═" * 78 + "╣")

    # Alle skridt
    for step in timeline.steps:
        status_icon = step.status
        number = f"{step.number:2d}"

        if step.status == StepStatus.CURRENT:
            line = f"║ {status_icon} [{number}] ▶ {step.name:<25} ← DU ER HER"
        elif step.status == StepStatus.DONE:
            line = f"║ {status_icon} [{number}]   {step.name:<25}"
        else:
            # Vis estimeret tid
            if step.estimated_end:
                try:
                    est = datetime.fromisoformat(step.estimated_end)
                    time_str = est.strftime("%H:%M")
                    line = f"║ {status_icon} [{number}]   {step.name:<25} → {time_str}"
                except:
                    line = f"║ {status_icon} [{number}]   {step.name:<25}"
            else:
                line = f"║ {status_icon} [{number}]   {step.name:<25}"

        # Pad til bredde
        line = f"{line:<79}║"
        lines.append(line)

    lines.append("╠" + "═" * 78 + "╣")

    # Estimeret afslutning
    try:
        est_complete = datetime.fromisoformat(timeline.estimated_completion)
        est_str = est_complete.strftime("%Y-%m-%d %H:%M")
    except:
        est_str = "Ukendt"
    lines.append(f"║ ⏱  Estimeret færdig: {est_str:<54} ║")

    # Endelig outcome
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  HVORDAN DET ENDER:                                                        ║")
    outcome_lines = [timeline.final_outcome[i:i+76] for i in range(0, len(timeline.final_outcome), 76)]
    for ol in outcome_lines:
        lines.append(f"║    {ol:<74} ║")

    lines.append("╚" + "═" * 78 + "╝")

    return "\n".join(lines)


def visualize_all_sejrs() -> str:
    """Vis tidslinjer for ALLE aktive sejrs"""
    generator = TimelineGenerator()
    output = []

    output.append("\n" + "=" * 80)
    output.append("       KOMPLET OVERBLIK: ALLE SKRIDT FRA NU TIL AFSLUTNING")
    output.append("=" * 80 + "\n")

    if not ACTIVE_DIR.exists():
        output.append("Ingen aktive sejrs fundet.")
        return "\n".join(output)

    for sejr_dir in sorted(ACTIVE_DIR.iterdir()):
        if sejr_dir.is_dir():
            timeline = generator.generate_sejr_timeline(sejr_dir)
            output.append(visualize_timeline(timeline))
            output.append("")

    # Samlet oversigt
    output.append("\n" + "=" * 80)
    output.append("       SAMLET FREMTIDSUDSIGT")
    output.append("=" * 80)

    # Vis de næste 7 dage
    from datetime import date
    today = date.today()

    output.append("\n DE NÆSTE 7 DAGE:")
    output.append("-" * 40)

    for i in range(7):
        day = today + timedelta(days=i)
        weekday = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"][day.weekday()]

        if i == 0:
            output.append(f"\n I DAG ({weekday} {day.strftime('%d/%m')}):")
            output.append("   → Fokusér på aktive sejrs")
        elif i == 1:
            output.append(f"\n⏳ I MORGEN ({weekday} {day.strftime('%d/%m')}):")
            output.append("   → Fortsæt implementation")
        else:
            output.append(f"\n {weekday} {day.strftime('%d/%m')}:")
            if day.weekday() == 4:  # Fredag
                output.append("   → Ugentlig review og arkivering")
            elif day.weekday() == 0:  # Mandag
                output.append("   → Planlæg ugens sejrs")
            else:
                output.append("   → Arbejd på aktive sejrs")

    return "\n".join(output)


def get_timeline_json(sejr_name: str = None) -> str:
    """Hent tidslinje som JSON"""
    generator = TimelineGenerator()

    if sejr_name:
        sejr_path = ACTIVE_DIR / sejr_name
        if sejr_path.exists():
            timeline = generator.generate_sejr_timeline(sejr_path)
            return json.dumps(timeline.to_dict(), ensure_ascii=False, indent=2)
        else:
            return json.dumps({"error": f"Sejr ikke fundet: {sejr_name}"})
    else:
        # Alle sejrs
        timelines = []
        if ACTIVE_DIR.exists():
            for sejr_dir in ACTIVE_DIR.iterdir():
                if sejr_dir.is_dir():
                    timeline = generator.generate_sejr_timeline(sejr_dir)
                    timelines.append(timeline.to_dict())
        return json.dumps(timelines, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--all":
            print(visualize_all_sejrs())

        elif cmd == "--json":
            if len(sys.argv) > 2:
                print(get_timeline_json(sys.argv[2]))
            else:
                print(get_timeline_json())

        elif cmd == "--sejr" and len(sys.argv) > 2:
            sejr_name = sys.argv[2]
            sejr_path = ACTIVE_DIR / sejr_name
            if sejr_path.exists():
                generator = TimelineGenerator()
                timeline = generator.generate_sejr_timeline(sejr_path)
                print(visualize_timeline(timeline))
            else:
                print(f"Sejr ikke fundet: {sejr_name}")

        elif cmd == "--help":
            print("""
COMPLETE TIMELINE - Se ALLE Skridt Fra Nu Til Afslutning
=========================================================

KOMMANDOER:
  --all          Vis tidslinjer for ALLE aktive sejrs
  --sejr <navn>  Vis tidslinje for én specifik sejr
  --json [navn]  Output som JSON (alle eller én)
  --help         Vis denne hjælp

EKSEMPLER:
  python complete_timeline.py --all
  python complete_timeline.py --sejr "NY_SEJR_2026-01-25"
  python complete_timeline.py --json > timelines.json
""")
    else:
        print(visualize_all_sejrs())
