#!/usr/bin/env python3
"""
DNA Status Widget for Sejrliste Visual System.

Displays the 7 DNA lag status with:
- Current state per lag
- Last run timestamp
- Active indicator during execution
"""

from datetime import datetime
from typing import Optional, Dict, Any

# DNA Lag definitions
DNA_LAGS = [
    {"number": 1, "name": "SELF-AWARE", "description": "System identity", "script": None},
    {"number": 2, "name": "SELF-DOCUMENTING", "description": "Auto logging", "script": "auto_track"},
    {"number": 3, "name": "SELF-VERIFYING", "description": "Verification", "script": "auto_verify"},
    {"number": 4, "name": "SELF-IMPROVING", "description": "Pattern learning", "script": "auto_learn"},
    {"number": 5, "name": "SELF-ARCHIVING", "description": "Archive system", "script": "auto_archive"},
    {"number": 6, "name": "PREDICTIVE", "description": "Predictions", "script": "auto_predict"},
    {"number": 7, "name": "SELF-OPTIMIZING", "description": "3 alternatives", "script": "generate_sejr"},
]


class DNAStatusWidget:
    """
    Widget to display 7 DNA lag status.

    Can be used standalone (terminal) or as base for Textual widget.
    """

    def __init__(self):
        """Initialize status tracker."""
        self._last_run: Dict[int, datetime] = {}
        self._active_lag: Optional[int] = None
        self._status: Dict[int, str] = {i: "idle" for i in range(1, 8)}

    def set_active(self, lag_number: int):
        """Mark a DNA lag as currently active (running)."""
        self._active_lag = lag_number
        self._status[lag_number] = "running"

    def set_complete(self, lag_number: int):
        """Mark a DNA lag as complete."""
        self._last_run[lag_number] = datetime.now()
        self._status[lag_number] = "complete"
        if self._active_lag == lag_number:
            self._active_lag = None

    def set_error(self, lag_number: int):
        """Mark a DNA lag as error state."""
        self._status[lag_number] = "error"
        if self._active_lag == lag_number:
            self._active_lag = None

    def set_idle(self, lag_number: int):
        """Reset a DNA lag to idle state."""
        self._status[lag_number] = "idle"
        if self._active_lag == lag_number:
            self._active_lag = None

    def get_status(self, lag_number: int) -> str:
        """Get current status of a DNA lag."""
        return self._status.get(lag_number, "unknown")

    def get_last_run(self, lag_number: int) -> Optional[datetime]:
        """Get last run timestamp for a DNA lag."""
        return self._last_run.get(lag_number)

    def is_active(self, lag_number: int) -> bool:
        """Check if a DNA lag is currently active."""
        return self._active_lag == lag_number

    def render_terminal(self, width: int = 50) -> str:
        """Render DNA status for terminal display."""
        lines = []
        lines.append("=" * width)
        lines.append(" 7 DNA LAG STATUS ".center(width))
        lines.append("=" * width)

        for lag in DNA_LAGS:
            num = lag["number"]
            name = lag["name"]
            status = self._status.get(num, "idle")

            # Status indicator
            if status == "running":
                indicator = "[*]"
                color_start = "\033[33m"  # Yellow
                color_end = "\033[0m"
            elif status == "complete":
                indicator = "[OK]"
                color_start = "\033[32m"  # Green
                color_end = "\033[0m"
            elif status == "error":
                indicator = "[!]"
                color_start = "\033[31m"  # Red
                color_end = "\033[0m"
            else:
                indicator = "[ ]"
                color_start = ""
                color_end = ""

            # Last run time
            last = self._last_run.get(num)
            time_str = last.strftime("%H:%M") if last else "--:--"

            line = f" {color_start}{indicator}{color_end} Lag {num}: {name:<18} {time_str}"
            lines.append(line)

        lines.append("=" * width)

        # Hotkey hint
        lines.append(" Hotkeys: v=verify a=archive p=predict l=learn n=new")

        return "\n".join(lines)

    def get_lag_info(self, lag_number: int) -> Dict[str, Any]:
        """Get full info about a DNA lag."""
        if lag_number < 1 or lag_number > 7:
            return {}

        lag = DNA_LAGS[lag_number - 1]
        return {
            "number": lag["number"],
            "name": lag["name"],
            "description": lag["description"],
            "script": lag["script"],
            "status": self._status.get(lag_number, "idle"),
            "last_run": self._last_run.get(lag_number),
            "is_active": self._active_lag == lag_number,
        }

    def get_all_lags(self) -> list:
        """Get info about all DNA lags."""
        return [self.get_lag_info(i) for i in range(1, 8)]


def render_dna_simple(active_lag: Optional[int] = None, last_runs: Optional[Dict[int, datetime]] = None) -> str:
    """
    Simple function to render DNA status without widget.

    Args:
        active_lag: Currently running lag number (or None)
        last_runs: Dict of lag_number -> last_run_datetime

    Returns:
        Formatted string for terminal display
    """
    last_runs = last_runs or {}
    lines = []

    for lag in DNA_LAGS:
        num = lag["number"]
        name = lag["name"]

        # Status indicator
        if active_lag == num:
            indicator = "[*]"
        elif num in last_runs:
            indicator = "[OK]"
        else:
            indicator = "[ ]"

        # Hotkey hint
        script = lag.get("script")
        hotkey = ""
        if script == "auto_verify":
            hotkey = "(v)"
        elif script == "auto_archive":
            hotkey = "(a)"
        elif script == "auto_predict":
            hotkey = "(p)"
        elif script == "auto_learn":
            hotkey = "(l)"
        elif script == "generate_sejr":
            hotkey = "(n)"

        lines.append(f" {indicator} Lag {num}: {name:<18} {hotkey}")

    return "\n".join(lines)


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Testing DNAStatusWidget...")

    widget = DNAStatusWidget()

    # Initial state
    print("\nInitial state:")
    print(widget.render_terminal())

    # Simulate running verify
    print("\n--- Running auto_verify (Lag 3) ---")
    widget.set_active(3)
    print(widget.render_terminal())

    # Complete verify
    print("\n--- Verify complete ---")
    widget.set_complete(3)
    print(widget.render_terminal())

    # Simulate error
    print("\n--- Predict error (Lag 6) ---")
    widget.set_error(6)
    print(widget.render_terminal())

    print("\nDNAStatusWidget test complete!")
