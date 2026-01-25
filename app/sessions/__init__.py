"""Session management for Sejrliste"""
from pathlib import Path
import json
from datetime import datetime

def get_session_path(system_path: Path, sejr_id: str) -> Path:
    """Get path to session folder for sejr"""
    return system_path / "app" / "sessions" / sejr_id

def load_session_state(session_path: Path) -> dict:
    """Load session state from JSON"""
    state_file = session_path / "SESSION_STATE.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {
        "created": datetime.now().isoformat(),
        "current_phase": "PLANNING",
        "focus": None,
        "tokens_used": {},
    }

def save_session_state(session_path: Path, state: dict) -> None:
    """Save session state to JSON"""
    session_path.mkdir(parents=True, exist_ok=True)
    state_file = session_path / "SESSION_STATE.json"
    state["updated"] = datetime.now().isoformat()
    state_file.write_text(json.dumps(state, indent=2))
