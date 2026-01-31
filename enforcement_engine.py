#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    ENFORCEMENT ENGINE - UMULIG AT FEJLE
═══════════════════════════════════════════════════════════════════════════════

WHAT:  Kvalitets-enforcement for 3-pass konkurrence systemet.
       TVINGER korrekt arbejde — BLOKERER indtil bevis er leveret.

WHY:   Kerne-modul importeret af web_app.py og web_app_en.py.
       Uden dette modul kan brugere springe passes over.

WHO:   Importeret af: web_app.py, web_app_en.py (Streamlit web apps)
       VIGTIG: Denne fil SKAL ligge i project root (samme dir som web_app.py)

HOW:   import enforcement_engine
       engine = enforcement_engine.EnforcementEngine(sejr_path)
       engine.check_pass_requirements()

Det er UMULIGT at:
- [FAIL] Goere samme opgave forkert
- [FAIL] Springe punkter over
- [FAIL] Overse hvor vi er
- [FAIL] Faerdiggoere noget der ikke er gjort rigtigt

FILOSOFI: Systemet BLOKERER indtil bevis er leveret.

Version: 3.0.0 | Opdateret: 2026-01-31
═══════════════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json
import re
import hashlib

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"

# ═══════════════════════════════════════════════════════════════════════════════
# ENFORCEMENT STATES
# ═══════════════════════════════════════════════════════════════════════════════

class EnforcementState:
    """States a task can be in"""
    LOCKED = " LOCKED"           # Cannot start - prerequisites not met
    AVAILABLE = " AVAILABLE"      # Can be started
    IN_PROGRESS = " IN PROGRESS"  # Currently working
    PENDING_VERIFY = "[WARN] PENDING"   # Done but needs verification
    VERIFIED = "[OK] VERIFIED"        # Verified and complete
    BLOCKED = " BLOCKED"          # Blocked by failed verification
    SKIPPED_TEMP = "⏸ TEMP SKIP"   # Temporarily skipped (must return)

# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════

class Checkpoint:
    """A single checkpoint that MUST be verified before proceeding"""

    def __init__(self,
                 id: str,
                 name: str,
                 verification_type: str,
                 verification_command: Optional[str] = None,
                 expected_result: Optional[str] = None,
                 manual_confirm: bool = False,
                 dependencies: Optional[List[str]] = None):
        self.id = id
        self.name = name
        self.verification_type = verification_type  # "command", "file_exists", "checkbox_count", "manual"
        self.verification_command = verification_command
        self.expected_result = expected_result
        self.manual_confirm = manual_confirm
        self.dependencies = dependencies or []
        self.state = EnforcementState.LOCKED
        self.verification_proof = None
        self.verified_at = None
        self.attempts = 0
        self.last_error = None

# ═══════════════════════════════════════════════════════════════════════════════
# ENFORCEMENT ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class EnforcementEngine:
    """
    UMULIG-AT-FEJLE System

    Denne motor TVINGER:
    1. Korrekt rækkefølge
    2. Verifikation ved hvert skridt
    3. Ingen spring
    4. Synlig position
    5. Fysisk bevis
    """

    def __init__(self, sejr_path: Path):
        self.sejr_path = sejr_path
        self.sejr_name = sejr_path.name
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.current_checkpoint_id: Optional[str] = None
        self.skipped_checkpoints: List[str] = []  # Must return to these
        self.enforcement_log: List[dict] = []
        self.state_file = sejr_path / "ENFORCEMENT_STATE.json"

        # Load existing state if available
        self._load_state()

        # If no checkpoints, generate from SEJR_LISTE.md
        if not self.checkpoints:
            self._generate_checkpoints_from_sejr()

    # ═══════════════════════════════════════════════════════════════════════════
    # CHECKPOINT GENERATION
    # ═══════════════════════════════════════════════════════════════════════════

    def _generate_checkpoints_from_sejr(self):
        """Generate checkpoints from SEJR_LISTE.md"""
        sejr_file = self.sejr_path / "SEJR_LISTE.md"
        if not sejr_file.exists():
            return

        content = sejr_file.read_text()

        # Find all checkboxes with their context
        checkbox_pattern = r'- \[( |x|X)\] (.+?)(?:\n|$)'
        matches = re.findall(checkbox_pattern, content)

        current_section = "UNKNOWN"
        checkpoint_id = 0
        prev_id = None

        for match in matches:
            is_checked = match[0].lower() == 'x'
            task_text = match[1].strip()

            # Detect section from task context
            if "PHASE 0" in task_text or "Research" in task_text:
                current_section = "PHASE_0"
            elif "PHASE 1" in task_text or "Planning" in task_text:
                current_section = "PHASE_1"
            elif "PHASE 2" in task_text or "Development" in task_text:
                current_section = "PHASE_2"
            elif "PHASE 3" in task_text or "Verification" in task_text:
                current_section = "PHASE_3"
            elif "PHASE 4" in task_text or "Git" in task_text:
                current_section = "PHASE_4"
            elif "Pass 1" in task_text.lower():
                current_section = "PASS_1"
            elif "Pass 2" in task_text.lower():
                current_section = "PASS_2"
            elif "Pass 3" in task_text.lower():
                current_section = "PASS_3"

            cp_id = f"CP_{checkpoint_id:03d}"

            # Determine verification type
            if "Verify:" in task_text:
                verify_type = "command"
                # Extract command
                cmd_match = re.search(r'Verify:\s*`([^`]+)`', task_text)
                verify_cmd = cmd_match.group(1) if cmd_match else None
            elif "git" in task_text.lower():
                verify_type = "command"
                verify_cmd = "git status"
            else:
                verify_type = "manual"
                verify_cmd = None

            checkpoint = Checkpoint(
                id=cp_id,
                name=f"[{current_section}] {task_text[:60]}",
                verification_type=verify_type,
                verification_command=verify_cmd,
                dependencies=[prev_id] if prev_id else [],
                manual_confirm=verify_type == "manual"
            )

            # If already checked, mark as verified
            if is_checked:
                checkpoint.state = EnforcementState.VERIFIED
                checkpoint.verified_at = datetime.now().isoformat()
                checkpoint.verification_proof = "Pre-existing checkbox"

            self.checkpoints[cp_id] = checkpoint
            prev_id = cp_id
            checkpoint_id += 1

        # Set first unverified as current
        self._update_current_checkpoint()
        self._save_state()

    # ═══════════════════════════════════════════════════════════════════════════
    # STATE MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════

    def _load_state(self):
        """Load enforcement state from file"""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                self.current_checkpoint_id = data.get('current_checkpoint_id')
                self.skipped_checkpoints = data.get('skipped_checkpoints', [])
                self.enforcement_log = data.get('enforcement_log', [])

                for cp_data in data.get('checkpoints', []):
                    cp = Checkpoint(
                        id=cp_data['id'],
                        name=cp_data['name'],
                        verification_type=cp_data['verification_type'],
                        verification_command=cp_data.get('verification_command'),
                        expected_result=cp_data.get('expected_result'),
                        manual_confirm=cp_data.get('manual_confirm', False),
                        dependencies=cp_data.get('dependencies', [])
                    )
                    cp.state = cp_data.get('state', EnforcementState.LOCKED)
                    cp.verification_proof = cp_data.get('verification_proof')
                    cp.verified_at = cp_data.get('verified_at')
                    cp.attempts = cp_data.get('attempts', 0)
                    cp.last_error = cp_data.get('last_error')
                    self.checkpoints[cp.id] = cp
            except Exception as e:
                print(f"Error loading state: {e}")

    def _save_state(self):
        """Save enforcement state to file"""
        data = {
            'current_checkpoint_id': self.current_checkpoint_id,
            'skipped_checkpoints': self.skipped_checkpoints,
            'enforcement_log': self.enforcement_log[-100:],  # Keep last 100 entries
            'checkpoints': [
                {
                    'id': cp.id,
                    'name': cp.name,
                    'verification_type': cp.verification_type,
                    'verification_command': cp.verification_command,
                    'expected_result': cp.expected_result,
                    'manual_confirm': cp.manual_confirm,
                    'dependencies': cp.dependencies,
                    'state': cp.state,
                    'verification_proof': cp.verification_proof,
                    'verified_at': cp.verified_at,
                    'attempts': cp.attempts,
                    'last_error': cp.last_error
                }
                for cp in self.checkpoints.values()
            ],
            'last_updated': datetime.now().isoformat()
        }
        self.state_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _update_current_checkpoint(self):
        """Find the next checkpoint that needs work"""
        # First, check if there are skipped checkpoints we MUST return to
        if self.skipped_checkpoints:
            for cp_id in self.skipped_checkpoints:
                if cp_id in self.checkpoints:
                    cp = self.checkpoints[cp_id]
                    if cp.state != EnforcementState.VERIFIED:
                        self.current_checkpoint_id = cp_id
                        cp.state = EnforcementState.IN_PROGRESS
                        return
            # All skipped are now verified
            self.skipped_checkpoints.clear()

        # Find first unverified checkpoint
        for cp_id, cp in self.checkpoints.items():
            if cp.state not in [EnforcementState.VERIFIED, EnforcementState.SKIPPED_TEMP]:
                # Check dependencies
                deps_met = all(
                    self.checkpoints.get(dep_id, Checkpoint("", "", "")).state == EnforcementState.VERIFIED
                    for dep_id in cp.dependencies
                )
                if deps_met:
                    self.current_checkpoint_id = cp_id
                    cp.state = EnforcementState.AVAILABLE
                    return

        # All done!
        self.current_checkpoint_id = None

    # ═══════════════════════════════════════════════════════════════════════════
    # ENFORCEMENT ACTIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def start_checkpoint(self, checkpoint_id: str) -> Tuple[bool, str]:
        """
        Start working on a checkpoint.
        BLOCKS if:
        - Checkpoint doesn't exist
        - Dependencies not met
        - Another checkpoint is in progress
        """
        if checkpoint_id not in self.checkpoints:
            return False, f" BLOKERET: Checkpoint {checkpoint_id} findes ikke"

        cp = self.checkpoints[checkpoint_id]

        # Check dependencies
        for dep_id in cp.dependencies:
            dep = self.checkpoints.get(dep_id)
            if dep and dep.state != EnforcementState.VERIFIED:
                return False, f" BLOKERET: Afhængighed {dep_id} er ikke færdig. FÆRDIGGØR DEN FØRST!"

        # Check if there are skipped checkpoints that must be done first
        if self.skipped_checkpoints and checkpoint_id not in self.skipped_checkpoints:
            return False, f" BLOKERET: Du SKAL først færdiggøre: {', '.join(self.skipped_checkpoints)}"

        cp.state = EnforcementState.IN_PROGRESS
        self.current_checkpoint_id = checkpoint_id
        self._log_action("START", checkpoint_id, "Checkpoint påbegyndt")
        self._save_state()

        return True, f"[OK] Starter: {cp.name}"

    def verify_checkpoint(self, checkpoint_id: str, proof: Optional[str] = None) -> Tuple[bool, str]:
        """
        Verify a checkpoint.
        BLOCKS if verification fails.
        """
        if checkpoint_id not in self.checkpoints:
            return False, f" BLOKERET: Checkpoint {checkpoint_id} findes ikke"

        cp = self.checkpoints[checkpoint_id]
        cp.attempts += 1

        # Run verification based on type
        if cp.verification_type == "command" and cp.verification_command:
            success, result = self._run_verification_command(cp.verification_command)
            if not success:
                cp.state = EnforcementState.BLOCKED
                cp.last_error = result
                self._log_action("VERIFY_FAIL", checkpoint_id, result)
                self._save_state()
                return False, f" VERIFIKATION FEJLET!\n\nKommando: {cp.verification_command}\nFejl: {result}\n\nFIX PROBLEMET OG PRØV IGEN!"
            cp.verification_proof = result

        elif cp.verification_type == "file_exists":
            file_path = Path(cp.verification_command) if cp.verification_command else None
            if file_path and not file_path.exists():
                cp.state = EnforcementState.BLOCKED
                cp.last_error = f"Fil findes ikke: {file_path}"
                self._log_action("VERIFY_FAIL", checkpoint_id, cp.last_error)
                self._save_state()
                return False, f" VERIFIKATION FEJLET!\n\nFil mangler: {file_path}\n\nOPRET FILEN OG PRØV IGEN!"
            cp.verification_proof = f"File exists: {file_path}"

        elif cp.verification_type == "manual":
            if not proof:
                cp.state = EnforcementState.PENDING_VERIFY
                self._save_state()
                return False, f"[WARN] AFVENTER MANUEL BEKRÆFTELSE\n\nDu SKAL levere bevis for:\n{cp.name}\n\nHvad er dit bevis?"
            cp.verification_proof = proof

        # Verification passed!
        cp.state = EnforcementState.VERIFIED
        cp.verified_at = datetime.now().isoformat()

        # Remove from skipped if it was there
        if checkpoint_id in self.skipped_checkpoints:
            self.skipped_checkpoints.remove(checkpoint_id)

        self._log_action("VERIFIED", checkpoint_id, cp.verification_proof)
        self._update_current_checkpoint()
        self._save_state()

        return True, f"[OK] VERIFICERET: {cp.name}\n\nBevis: {cp.verification_proof}"

    def skip_checkpoint(self, checkpoint_id: str, reason: str) -> Tuple[bool, str]:
        """
        Temporarily skip a checkpoint.
        FORCES return to this checkpoint before completion.
        """
        if checkpoint_id not in self.checkpoints:
            return False, f" BLOKERET: Checkpoint {checkpoint_id} findes ikke"

        cp = self.checkpoints[checkpoint_id]

        # Can only skip available or in-progress checkpoints
        if cp.state not in [EnforcementState.AVAILABLE, EnforcementState.IN_PROGRESS]:
            return False, f" BLOKERET: Kan ikke springe {cp.state} checkpoint over"

        cp.state = EnforcementState.SKIPPED_TEMP
        if checkpoint_id not in self.skipped_checkpoints:
            self.skipped_checkpoints.append(checkpoint_id)

        self._log_action("SKIP_TEMP", checkpoint_id, f"Reason: {reason}")
        self._update_current_checkpoint()
        self._save_state()

        return True, f"⏸ MIDLERTIDIGT SPRUNGET OVER: {cp.name}\n\n[WARN] DU SKAL VENDE TILBAGE TIL DENNE OPGAVE!\n\nGrund: {reason}"

    def _run_verification_command(self, command: str) -> Tuple[bool, str]:
        """Run a verification command and return success/result"""
        import subprocess
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.sejr_path)
            )
            if result.returncode == 0:
                return True, result.stdout.strip() or "Command succeeded"
            else:
                return False, result.stderr.strip() or f"Exit code: {result.returncode}"
        except subprocess.TimeoutExpired:
            return False, "Timeout - kommando tog for lang tid"
        except Exception as e:
            return False, str(e)

    def _log_action(self, action: str, checkpoint_id: str, details: str):
        """Log an enforcement action"""
        self.enforcement_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'checkpoint_id': checkpoint_id,
            'details': details
        })

    # ═══════════════════════════════════════════════════════════════════════════
    # STATUS & VISUALIZATION
    # ═══════════════════════════════════════════════════════════════════════════

    def get_current_position(self) -> dict:
        """Get current position with visual indicator"""
        total = len(self.checkpoints)
        verified = sum(1 for cp in self.checkpoints.values() if cp.state == EnforcementState.VERIFIED)
        skipped = len(self.skipped_checkpoints)

        current_cp = self.checkpoints.get(self.current_checkpoint_id) if self.current_checkpoint_id else None

        return {
            'total': total,
            'verified': verified,
            'remaining': total - verified,
            'skipped_must_return': skipped,
            'progress_percent': round((verified / total) * 100) if total > 0 else 0,
            'current_checkpoint': {
                'id': current_cp.id if current_cp else None,
                'name': current_cp.name if current_cp else "ALLE FÆRDIGE!",
                'state': current_cp.state if current_cp else "[OK] COMPLETE"
            },
            'can_complete': verified == total and skipped == 0,
            'blocking_reason': f"SKAL TILBAGE TIL: {', '.join(self.skipped_checkpoints)}" if skipped > 0 else None
        }

    def get_visual_timeline(self) -> str:
        """Generate a visual timeline of all checkpoints"""
        lines = []
        lines.append("═" * 70)
        lines.append("                     ENFORCEMENT TIMELINE")
        lines.append("═" * 70)

        for cp_id, cp in self.checkpoints.items():
            marker = ""
            if cp_id == self.current_checkpoint_id:
                marker = " ◀◀◀ DU ER HER"
            elif cp_id in self.skipped_checkpoints:
                marker = " [WARN] SKAL TILBAGE!"

            # State icon
            if cp.state == EnforcementState.VERIFIED:
                icon = "[OK]"
            elif cp.state == EnforcementState.IN_PROGRESS:
                icon = ""
            elif cp.state == EnforcementState.BLOCKED:
                icon = ""
            elif cp.state == EnforcementState.SKIPPED_TEMP:
                icon = "⏸"
            elif cp.state == EnforcementState.PENDING_VERIFY:
                icon = "[WARN]"
            elif cp.state == EnforcementState.AVAILABLE:
                icon = ""
            else:
                icon = ""

            line = f"{icon} [{cp_id}] {cp.name[:45]:<45}{marker}"
            lines.append(line)

        lines.append("═" * 70)

        pos = self.get_current_position()
        lines.append(f"Progress: {pos['verified']}/{pos['total']} ({pos['progress_percent']}%)")
        if pos['skipped_must_return'] > 0:
            lines.append(f"[WARN] SKAL TILBAGE TIL {pos['skipped_must_return']} OPGAVER!")
        if pos['can_complete']:
            lines.append("[OK] KAN ARKIVERES!")

        return "\n".join(lines)

    def can_archive(self) -> Tuple[bool, str]:
        """Check if this sejr can be archived"""
        pos = self.get_current_position()

        if pos['skipped_must_return'] > 0:
            return False, f" KAN IKKE ARKIVERE!\n\nDu har {pos['skipped_must_return']} opgaver du SKAL tilbage til:\n" + \
                          "\n".join([f"- {self.checkpoints[cp_id].name}" for cp_id in self.skipped_checkpoints])

        if pos['remaining'] > 0:
            remaining = [cp for cp in self.checkpoints.values() if cp.state != EnforcementState.VERIFIED]
            return False, f" KAN IKKE ARKIVERE!\n\n{pos['remaining']} opgaver mangler:\n" + \
                          "\n".join([f"- {cp.name}" for cp in remaining[:5]])

        return True, "[OK] ALLE CHECKPOINTS VERIFICERET - KAN ARKIVERES!"


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_enforcement_for_sejr(sejr_path: Path) -> EnforcementEngine:
    """Get or create enforcement engine for a sejr"""
    return EnforcementEngine(sejr_path)


def get_all_active_enforcements() -> List[EnforcementEngine]:
    """Get enforcement engines for all active sejrs"""
    engines = []
    if ACTIVE_DIR.exists():
        for folder in ACTIVE_DIR.iterdir():
            if folder.is_dir():
                engines.append(EnforcementEngine(folder))
    return engines


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    print("═" * 70)
    print("          ENFORCEMENT ENGINE - UMULIG AT FEJLE SYSTEM")
    print("═" * 70)

    engines = get_all_active_enforcements()

    if not engines:
        print("Ingen aktive sejr fundet.")
        sys.exit(0)

    for engine in engines:
        print(f"\n {engine.sejr_name}")
        print(engine.get_visual_timeline())

        can_archive, reason = engine.can_archive()
        print(f"\nArkivering: {reason}")
