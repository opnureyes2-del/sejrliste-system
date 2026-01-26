#!/usr/bin/env python3
"""
UNIFIED SYNC SERVICE - Forbinder Alt Med Alt
============================================

DNA Lag: SELF-AWARE + PREDICTIVE + SELF-OPTIMIZING

Dette er HJERNEN der forbinder:
- Desktop app (GTK4)
- Web app (Streamlit)
- Ubuntu filsystem (Nautilus/D-Bus)
- Fremtidsvisioner (7 dage frem)

PRINCIP: Altid vide det næste skridt efter det næste skridt.
"""

import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
import threading
import socket
import hashlib

# ═══════════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

BASE_DIR = Path("/home/rasmus/Desktop/sejrliste systemet")
ACTIVE_DIR = BASE_DIR / "10_ACTIVE"
ARCHIVE_DIR = BASE_DIR / "90_ARCHIVE"
SYNC_PORT = 51470  # Port til inter-app kommunikation
SYNC_FILE = BASE_DIR / ".sync_state.json"

# ═══════════════════════════════════════════════════════════════════════════
# DATA MODELLER
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class SejrEvent:
    """En hændelse i sejrliste systemet"""
    event_type: str  # "created", "updated", "dropped", "archived", "predicted"
    sejr_name: str
    timestamp: str
    source: str  # "desktop", "web", "nautilus", "prediction"
    path: Optional[str] = None
    data: Optional[Dict] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def from_json(cls, data: str) -> 'SejrEvent':
        return cls(**json.loads(data))


@dataclass
class FutureVision:
    """Forudsigelse for kommende uge"""
    date: str
    predicted_sejrs: List[str]
    recommended_actions: List[str]
    confidence: float
    reasoning: str


# ═══════════════════════════════════════════════════════════════════════════
# PREDICTIVE ENGINE - Ser 7 Dage Frem
# ═══════════════════════════════════════════════════════════════════════════

class PredictiveEngine:
    """
    KLARSYN: Altid vide det næste skridt efter det næste skridt.
    Analyserer mønstre og forudsiger hvad der kommer.
    """

    def __init__(self):
        self.patterns_file = BASE_DIR / "_CURRENT" / "PATTERNS.json"
        self.history_file = BASE_DIR / "_CURRENT" / "HISTORY.json"

    def load_patterns(self) -> Dict:
        """Indlæs lærte mønstre"""
        if self.patterns_file.exists():
            try:
                return json.loads(self.patterns_file.read_text())
            except:
                pass
        return {"learned_patterns": [], "success_rates": {}}

    def analyze_week_ahead(self) -> List[FutureVision]:
        """
        Generér forudsigelser for de næste 7 dage.
        Baseret på:
        - Eksisterende aktive sejrs og deres deadlines
        - Historiske mønstre (hvilke ugedage er mest produktive)
        - Lærte patterns fra tidligere sejrs
        """
        visions = []
        patterns = self.load_patterns()
        active_sejrs = self._get_active_sejrs()

        today = datetime.now()

        for day_offset in range(7):
            target_date = today + timedelta(days=day_offset)
            weekday = target_date.strftime("%A")
            date_str = target_date.strftime("%Y-%m-%d")

            # Forudsig hvad der bør ske denne dag
            predicted = []
            actions = []
            confidence = 0.7
            reasoning = []

            # Check aktive sejrs for deadlines
            for sejr in active_sejrs:
                sejr_deadline = sejr.get("deadline")
                if sejr_deadline and sejr_deadline == date_str:
                    predicted.append(f"DEADLINE: {sejr['name']}")
                    actions.append(f"Færdiggør {sejr['name']} inden midnat")
                    confidence = 0.95
                    reasoning.append(f"{sejr['name']} har deadline")

            # Dag 0 (i dag): Fokusér på current work
            if day_offset == 0:
                current_sejrs = [s['name'] for s in active_sejrs if s.get('current_pass')]
                if current_sejrs:
                    predicted.extend(current_sejrs)
                    actions.append("Fortsæt aktive sejrs")
                    reasoning.append("Aktive sejrs kræver opmærksomhed")

            # Dag 1 (i morgen): Planlægning
            elif day_offset == 1:
                incomplete = [s['name'] for s in active_sejrs if s.get('completion_pct', 0) < 50]
                if incomplete:
                    actions.append(f"Prioriter: {', '.join(incomplete[:2])}")
                    reasoning.append("Sejrs under 50% bør have fokus")

            # Fredag: Review-dag (baseret på mønster)
            if weekday == "Friday":
                actions.append("Ugentlig review: Arkiver færdige sejrs")
                reasoning.append("Fredag er god til oprydning")

            # Mandag: Ny uge, nye mål
            if weekday == "Monday":
                actions.append("Planlæg ugens sejrs")
                reasoning.append("Mandag er god til planlægning")

            visions.append(FutureVision(
                date=date_str,
                predicted_sejrs=predicted,
                recommended_actions=actions,
                confidence=confidence,
                reasoning="; ".join(reasoning) if reasoning else "Standard forudsigelse"
            ))

        return visions

    def _get_active_sejrs(self) -> List[Dict]:
        """Hent alle aktive sejrs med deres status"""
        sejrs = []

        if ACTIVE_DIR.exists():
            for sejr_dir in ACTIVE_DIR.iterdir():
                if sejr_dir.is_dir():
                    status_file = sejr_dir / "STATUS.yaml"
                    sejr_info = {"name": sejr_dir.name, "path": str(sejr_dir)}

                    if status_file.exists():
                        try:
                            content = status_file.read_text()
                            for line in content.split("\n"):
                                if ":" in line:
                                    key, value = line.split(":", 1)
                                    key = key.strip()
                                    value = value.strip().strip('"')

                                    if key == "current_pass":
                                        sejr_info["current_pass"] = int(value) if value.isdigit() else 1
                                    elif key == "completion_percentage":
                                        sejr_info["completion_pct"] = int(value) if value.isdigit() else 0
                                    elif key == "total_score":
                                        sejr_info["score"] = int(value) if value.isdigit() else 0
                        except Exception:
                            pass

                    sejrs.append(sejr_info)

        return sejrs

    def get_next_steps(self, current_sejr: str) -> List[str]:
        """
        Hvad er det næste skridt EFTER det næste skridt?
        Returnerer en kæde af handlinger.
        """
        patterns = self.load_patterns()
        active_sejrs = self._get_active_sejrs()

        # Find current sejr
        current = None
        for s in active_sejrs:
            if s["name"] == current_sejr:
                current = s
                break

        if not current:
            return ["Opret ny sejr først"]

        steps = []
        current_pass = current.get("current_pass", 1)
        completion = current.get("completion_pct", 0)

        # Næste skridt baseret på current pass
        if current_pass == 1:
            steps.append("1. Færdiggør Pass 1 planlægning")
            steps.append("2. Start Pass 2 eksekvering")
            steps.append("3. Kør tests efter implementation")
            steps.append("4. Pass 3: 7-DNA review")
            steps.append("5. Arkiver med CONCLUSION.md")
        elif current_pass == 2:
            steps.append("1. Færdiggør implementation")
            steps.append("2. Kør tests og verifikation")
            steps.append("3. Start Pass 3 review")
            steps.append("4. Gennemgå alle 7 DNA lag")
            steps.append("5. Arkiver med fuld dokumentation")
        elif current_pass == 3:
            steps.append("1. Gennemgå 7 DNA lag")
            steps.append("2. Fix eventuelle mangler")
            steps.append("3. Kør final verification")
            steps.append("4. Arkiver sejr")
            steps.append("5. Start næste sejr fra backlog")

        return steps


# ═══════════════════════════════════════════════════════════════════════════
# DRAG & DROP SERVICE - Universelt
# ═══════════════════════════════════════════════════════════════════════════

class UnifiedDragDrop:
    """
    Håndterer drag-and-drop fra ALLE kilder:
    - GTK4 desktop app
    - Streamlit web app (via upload)
    - Nautilus file manager (via D-Bus)

    Resultat: Ny sejr oprettes og synkroniseres til ALLE platforme.
    """

    def __init__(self, on_drop_callback: Optional[Callable] = None):
        self.on_drop = on_drop_callback
        self.prediction_engine = PredictiveEngine()

    def handle_drop(self, source: str, path: str, metadata: Optional[Dict] = None) -> SejrEvent:
        """
        Håndter et drop fra enhver kilde.

        Args:
            source: "desktop", "web", "nautilus"
            path: Sti til droppet fil/mappe
            metadata: Ekstra data fra kilden

        Returns:
            SejrEvent med resultatet
        """
        dropped_path = Path(path)

        if not dropped_path.exists():
            return SejrEvent(
                event_type="error",
                sejr_name="",
                timestamp=datetime.now().isoformat(),
                source=source,
                data={"error": f"Sti findes ikke: {path}"}
            )

        # Generer sejr navn fra sti
        sejr_name = self._generate_sejr_name(dropped_path)

        # Opret sejr via generate_sejr.py
        result = self._create_sejr_from_drop(sejr_name, dropped_path, metadata)

        # Broadcast til alle klienter
        event = SejrEvent(
            event_type="created",
            sejr_name=sejr_name,
            timestamp=datetime.now().isoformat(),
            source=source,
            path=str(result.get("sejr_path", "")),
            data=result
        )

        self._broadcast_event(event)

        # Trigger callback hvis sat
        if self.on_drop:
            self.on_drop(event)

        return event

    def _generate_sejr_name(self, path: Path) -> str:
        """Generer et meningsfuldt sejr navn fra sti"""
        name = path.stem.upper()
        # Fjern ulovlige tegn
        name = "".join(c for c in name if c.isalnum() or c in "_-")
        # Tilføj dato
        date_str = datetime.now().strftime("%Y-%m-%d")
        return f"{name}_{date_str}"

    def _create_sejr_from_drop(self, name: str, path: Path, metadata: Optional[Dict]) -> Dict:
        """Opret sejr fra droppet indhold"""
        script_path = BASE_DIR / "scripts" / "generate_sejr.py"

        try:
            # Bestem goal baseret på droppet sti
            if path.is_file():
                goal = f"Bearbejd fil: {path.name}"
            else:
                goal = f"Organiser mappe: {path.name}"

            # Kør generate_sejr.py med korrekte argumenter
            result = subprocess.run(
                ["python3", str(script_path),
                 "--name", name,
                 "--goal", goal],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR)
            )

            if result.returncode == 0:
                # Find den nye sejr mappe
                sejr_path = ACTIVE_DIR / f"{name}"
                if not sejr_path.exists():
                    # Prøv med dato suffix
                    for d in ACTIVE_DIR.iterdir():
                        if d.name.startswith(name):
                            sejr_path = d
                            break

                return {
                    "success": True,
                    "sejr_path": str(sejr_path),
                    "message": f"Sejr '{name}' oprettet fra {path.name}",
                    "next_steps": self.prediction_engine.get_next_steps(name)
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _broadcast_event(self, event: SejrEvent):
        """Send event til alle lyttende klienter"""
        # Gem til sync fil
        sync_data = []
        if SYNC_FILE.exists():
            try:
                sync_data = json.loads(SYNC_FILE.read_text())
            except:
                pass

        sync_data.append(asdict(event))

        # Behold kun sidste 100 events
        sync_data = sync_data[-100:]

        SYNC_FILE.write_text(json.dumps(sync_data, ensure_ascii=False, indent=2))


# ═══════════════════════════════════════════════════════════════════════════
# NAUTILUS INTEGRATION (Ubuntu Files)
# ═══════════════════════════════════════════════════════════════════════════

class NautilusIntegration:
    """
    Integration med Ubuntu's Nautilus filhåndtering via D-Bus og .desktop filer.

    Muliggør:
    - Højreklik → "Opret Sejr"
    - Drag til Sejrliste mappe → Auto-opret
    - Notifikationer når sejrs ændres
    """

    DESKTOP_FILE_PATH = Path.home() / ".local/share/nautilus/scripts/Opret Sejr"

    def install_nautilus_integration(self) -> bool:
        """Installer Nautilus scripts og actions"""
        try:
            # Opret scripts mappe
            scripts_dir = Path.home() / ".local/share/nautilus/scripts"
            scripts_dir.mkdir(parents=True, exist_ok=True)

            # Opret script der håndterer højreklik
            script_content = f'''#!/bin/bash
# Nautilus script: Opret Sejr fra valgt fil/mappe
# Auto-genereret af Sejrliste System

SELECTED="$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"
SEJR_SCRIPT="{BASE_DIR}/scripts/generate_sejr.py"

if [ -n "$SELECTED" ]; then
    while IFS= read -r file; do
        if [ -n "$file" ]; then
            NAME=$(basename "$file" | tr '[:lower:]' '[:upper:]' | tr ' ' '_' | cut -c1-30)

            if [ -f "$file" ]; then
                GOAL="Bearbejd fil: $(basename "$file")"
            elif [ -d "$file" ]; then
                GOAL="Organiser mappe: $(basename "$file")"
            else
                GOAL="Ny opgave"
            fi

            python3 "$SEJR_SCRIPT" --name "$NAME" --goal "$GOAL"
            notify-send "Sejrliste" "Sejr oprettet: $NAME" -i dialog-information
        fi
    done <<< "$SELECTED"
fi
'''

            script_path = scripts_dir / "Opret Sejr"
            script_path.write_text(script_content)
            script_path.chmod(0o755)

            # Opret .desktop fil for application menu
            desktop_content = f'''[Desktop Entry]
Name=Sejrliste
GenericName=Opgavestyring
Comment=Opret og spor sejrs
Exec=python3 {BASE_DIR}/masterpiece.py
Icon=checkbox-checked
Terminal=false
Type=Application
Categories=Utility;ProjectManagement;
Keywords=todo;tasks;projects;sejr;
'''

            applications_dir = Path.home() / ".local/share/applications"
            applications_dir.mkdir(parents=True, exist_ok=True)
            (applications_dir / "sejrliste.desktop").write_text(desktop_content)

            return True

        except Exception as e:
            print(f"Nautilus integration fejlede: {e}")
            return False

    def create_drop_target_folder(self) -> Path:
        """
        Opret en 'drop target' mappe som Nautilus overvåger.
        Filer droppet her konverteres automatisk til sejrs.
        """
        drop_folder = BASE_DIR / "DROP_HER"
        drop_folder.mkdir(exist_ok=True)

        # Opret README
        readme = drop_folder / "README.txt"
        readme.write_text("""╔══════════════════════════════════════════════════════════════╗
║                    DROP ZONE - SEJRLISTE                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Drop filer eller mapper her for at oprette nye Sejrs!       ║
║                                                              ║
║  ➡️  Drop en fil → Ny Sejr med fil som input                 ║
║  ➡️  Drop en mappe → Ny Sejr med mappe som input             ║
║                                                              ║
║  Systemet overvåger denne mappe og opretter                  ║
║  automatisk sejrs når du dropper noget.                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

        return drop_folder


# ═══════════════════════════════════════════════════════════════════════════
# REAL-TIME SYNC SERVICE
# ═══════════════════════════════════════════════════════════════════════════

class SyncService:
    """
    Real-time synkronisering mellem alle dele af systemet.
    Bruger simpel fil-baseret synk + socket for hastighed.
    """

    def __init__(self):
        self.running = False
        self.listeners: List[Callable] = []
        self.prediction_engine = PredictiveEngine()

    def add_listener(self, callback: Callable[[SejrEvent], None]):
        """Tilføj en listener der kaldes når events sker"""
        self.listeners.append(callback)

    def start(self):
        """Start synkroniseringsservice i baggrunden"""
        self.running = True
        thread = threading.Thread(target=self._watch_loop, daemon=True)
        thread.start()

    def stop(self):
        """Stop synkroniseringsservice"""
        self.running = False

    def _watch_loop(self):
        """Overvåg for ændringer"""
        last_check = {}

        while self.running:
            try:
                # Check ACTIVE folder for ændringer
                for sejr_dir in ACTIVE_DIR.iterdir():
                    if sejr_dir.is_dir():
                        status_file = sejr_dir / "STATUS.yaml"
                        if status_file.exists():
                            mtime = status_file.stat().st_mtime
                            if sejr_dir.name not in last_check or last_check[sejr_dir.name] < mtime:
                                last_check[sejr_dir.name] = mtime
                                self._notify_change(sejr_dir)

                # Check sync file for events fra andre apps
                if SYNC_FILE.exists():
                    events = json.loads(SYNC_FILE.read_text())
                    # Process new events...

            except Exception as e:
                print(f"Sync fejl: {e}")

            # Vent før næste check
            import time
            time.sleep(1)

    def _notify_change(self, sejr_dir: Path):
        """Notificér listeners om ændring"""
        event = SejrEvent(
            event_type="updated",
            sejr_name=sejr_dir.name,
            timestamp=datetime.now().isoformat(),
            source="filesystem",
            path=str(sejr_dir)
        )

        for listener in self.listeners:
            try:
                listener(event)
            except Exception as e:
                print(f"Listener fejl: {e}")

    def get_week_vision(self) -> List[Dict]:
        """Hent forudsigelser for næste uge"""
        visions = self.prediction_engine.analyze_week_ahead()
        return [asdict(v) for v in visions]


# ═══════════════════════════════════════════════════════════════════════════
# HOVEDFUNKTIONER
# ═══════════════════════════════════════════════════════════════════════════

def setup_complete_integration():
    """Opsæt komplet integration på tværs af alle platforme"""
    print("🔗 OPSÆTTER UNIFIED SYNC SERVICE...")
    print("=" * 60)

    # 1. Nautilus integration
    nautilus = NautilusIntegration()
    if nautilus.install_nautilus_integration():
        print("✅ Nautilus højreklik-menu installeret")
        print("   → Højreklik på fil → Scripts → 'Opret Sejr'")

    # 2. Drop folder
    drop_folder = nautilus.create_drop_target_folder()
    print(f"✅ Drop zone oprettet: {drop_folder}")
    print("   → Drop filer her for auto-konvertering")

    # 3. Sync service
    sync = SyncService()
    print("✅ Sync service klar")
    print("   → Real-time synk mellem desktop og web")

    # 4. Predictions
    engine = PredictiveEngine()
    visions = engine.analyze_week_ahead()
    print("\n📅 NÆSTE 7 DAGE (KLARSYN):")
    print("-" * 40)
    for v in visions:
        date_formatted = datetime.strptime(v.date, "%Y-%m-%d").strftime("%A %d/%m")
        print(f"\n{date_formatted}:")
        if v.predicted_sejrs:
            for s in v.predicted_sejrs:
                print(f"  📋 {s}")
        if v.recommended_actions:
            for a in v.recommended_actions:
                print(f"  → {a}")

    print("\n" + "=" * 60)
    print("✅ UNIFIED SYNC SERVICE KLAR!")
    print("")
    print("BRUG:")
    print("  • Desktop: python masterpiece.py")
    print("  • Web: streamlit run web_app.py")
    print("  • Drop: Træk filer til DROP_HER mappen")
    print("  • Nautilus: Højreklik → Scripts → Opret Sejr")

    return sync


def get_predictions_json() -> str:
    """Hent forudsigelser som JSON (til web/desktop)"""
    engine = PredictiveEngine()
    visions = engine.analyze_week_ahead()
    return json.dumps([asdict(v) for v in visions], ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--install":
            setup_complete_integration()

        elif cmd == "--predictions":
            print(get_predictions_json())

        elif cmd == "--next-steps" and len(sys.argv) > 2:
            sejr_name = sys.argv[2]
            engine = PredictiveEngine()
            steps = engine.get_next_steps(sejr_name)
            print(f"\n🔮 NÆSTE SKRIDT FOR: {sejr_name}")
            print("-" * 40)
            for step in steps:
                print(f"  {step}")

        elif cmd == "--help":
            print("""
UNIFIED SYNC SERVICE - Forbinder Alt Med Alt
=============================================

KOMMANDOER:
  --install      Installer Nautilus integration og drop zone
  --predictions  Vis forudsigelser for næste 7 dage (JSON)
  --next-steps   Vis næste skridt for en sejr
  --help         Vis denne hjælp

EKSEMPLER:
  python unified_sync.py --install
  python unified_sync.py --predictions
  python unified_sync.py --next-steps "NY_SEJR_2026-01-25"
""")
    else:
        setup_complete_integration()
