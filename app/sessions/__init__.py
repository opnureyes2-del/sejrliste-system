"""
SEJR SESSIONS - Permanent Session Context
=========================================

Formål: Bevarer session state mellem conversations.
Løser: "Hvad arbejdede vi på?" problemet.

Files per sejr session:
- SESSION_STATE.json: Hvad model arbejder på NU
- FOCUS_LOCK.yaml: Hvad model SKAL fokusere på
- PROGRESS_LOG.jsonl: Alt model har gjort (immutable)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

SESSIONS_DIR = Path(__file__).parent


class SejrSession:
    """Manages session state for a specific sejr."""

    def __init__(self, sejr_id: str):
        self.sejr_id = sejr_id
        self.session_dir = SESSIONS_DIR / sejr_id
        self.state_file = self.session_dir / "SESSION_STATE.json"
        self.focus_file = self.session_dir / "FOCUS_LOCK.yaml"
        self.log_file = self.session_dir / "PROGRESS_LOG.jsonl"

    def ensure_exists(self):
        """Create session directory if not exists."""
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Initialize state file if not exists
        if not self.state_file.exists():
            self.save_state({
                "sejr_id": self.sejr_id,
                "created": datetime.now().isoformat(),
                "current_phase": "PASS_1",
                "current_checkbox": 0,
                "total_checkboxes": 0,
                "status": "active",
                "last_action": None,
                "last_updated": datetime.now().isoformat()
            })

        # Initialize focus file if not exists
        if not self.focus_file.exists():
            self._write_focus({
                "focus_locked": True,
                "locked_on": self.sejr_id,
                "allowed_actions": [
                    "Work on current sejr",
                    "Update AUTO_LOG.jsonl",
                    "Run verification",
                    "Mark checkboxes"
                ],
                "blocked_actions": [
                    "Start new sejr",
                    "Work on other projects",
                    "Skip phases"
                ]
            })

    def save_state(self, state: dict):
        """Save session state to JSON."""
        self.ensure_exists()
        state["last_updated"] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def load_state(self) -> dict:
        """Load session state from JSON."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {}

    def _write_focus(self, focus: dict):
        """Write focus lock to YAML."""
        import yaml
        with open(self.focus_file, 'w') as f:
            yaml.dump(focus, f, default_flow_style=False, allow_unicode=True)

    def log_progress(self, action: str, details: dict = None):
        """Append to immutable progress log."""
        self.ensure_exists()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def update_progress(self, phase: str, checkbox: int, total: int):
        """Update current progress in state."""
        state = self.load_state()
        state["current_phase"] = phase
        state["current_checkbox"] = checkbox
        state["total_checkboxes"] = total
        state["last_action"] = f"Completed checkbox {checkbox}/{total} in {phase}"
        self.save_state(state)
        self.log_progress("checkbox_completed", {
            "phase": phase,
            "checkbox": checkbox,
            "total": total
        })

    def complete_phase(self, phase: str):
        """Mark a phase as complete."""
        state = self.load_state()
        state["current_phase"] = self._next_phase(phase)
        state["current_checkbox"] = 0
        state["last_action"] = f"Completed {phase}"
        self.save_state(state)
        self.log_progress("phase_completed", {"phase": phase})

    def _next_phase(self, phase: str) -> str:
        """Get the next phase after current."""
        phases = ["PASS_1", "PASS_2", "PASS_3", "FINAL_VERIFICATION", "ARCHIVE"]
        try:
            idx = phases.index(phase)
            return phases[min(idx + 1, len(phases) - 1)]
        except ValueError:
            return phase

    def close_session(self):
        """Mark session as complete and archived."""
        state = self.load_state()
        state["status"] = "archived"
        state["archived_at"] = datetime.now().isoformat()
        self.save_state(state)
        self.log_progress("session_closed", {"final_state": state})


def get_active_session() -> Optional[SejrSession]:
    """Find and return the currently active session."""
    if not SESSIONS_DIR.exists():
        return None

    for session_dir in SESSIONS_DIR.iterdir():
        if not session_dir.is_dir() or session_dir.name.startswith('_'):
            continue
        state_file = session_dir / "SESSION_STATE.json"
        if state_file.exists():
            with open(state_file) as f:
                state = json.load(f)
                if state.get("status") == "active":
                    return SejrSession(session_dir.name)
    return None


def create_session(sejr_id: str) -> SejrSession:
    """Create a new session for a sejr."""
    session = SejrSession(sejr_id)
    session.ensure_exists()
    return session


def resume_session(sejr_id: str) -> Optional[SejrSession]:
    """Resume an existing session."""
    session = SejrSession(sejr_id)
    if session.state_file.exists():
        return session
    return None


def list_sessions() -> list:
    """List all session IDs."""
    if not SESSIONS_DIR.exists():
        return []

    sessions = []
    for session_dir in SESSIONS_DIR.iterdir():
        if session_dir.is_dir() and not session_dir.name.startswith('_'):
            state_file = session_dir / "SESSION_STATE.json"
            if state_file.exists():
                sessions.append(session_dir.name)
    return sessions
