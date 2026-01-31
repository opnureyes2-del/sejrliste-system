#!/usr/bin/env python3
"""
Visual Polish Widgets for Sejrliste Visual System.

Provides enhanced visual elements:
- Color-coded status indicators
- Session timer
- Statistics view
- Progress animations (terminal-friendly)

FASE 4 of the Sejrliste Visual App.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from pathlib import Path
import json


# Status colors (ANSI escape codes for terminal)
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Status colors
    GREEN = "\033[32m"      # Done/Complete
    YELLOW = "\033[33m"     # At risk/Warning
    RED = "\033[31m"        # Blocked/Error
    BLUE = "\033[34m"       # In progress
    CYAN = "\033[36m"       # Info
    MAGENTA = "\033[35m"    # Special
    WHITE = "\033[37m"      # Default
    BLACK = "\033[30m"      # Dark

    # Bright colors
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_MAGENTA = "\033[95m"

    # Background
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_RED = "\033[41m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"


class Theme:
    """
    Theme configuration for visual polish.

    Supports:
    - Default (colorful)
    - Minimal (reduced colors)
    - No-color (plain text)
    """

    DEFAULT = "default"
    MINIMAL = "minimal"
    NO_COLOR = "no_color"

    def __init__(self, theme: str = "default"):
        self.theme = theme

    def colorize(self, text: str, color: str) -> str:
        """Apply color based on theme setting."""
        if self.theme == self.NO_COLOR:
            return text
        return f"{color}{text}{Colors.RESET}"

    def get_icon(self, icon_type: str) -> str:
        """Get icon based on theme."""
        icons = {
            "default": {
                "done": "[OK]",
                "in_progress": "",
                "blocked": "",
                "warning": "[WARN]",
                "pending": "⏳",
                "error": "[FAIL]",
            },
            "minimal": {
                "done": "[OK]",
                "in_progress": "[..]",
                "blocked": "[!!]",
                "warning": "[!]",
                "pending": "[--]",
                "error": "[X]",
            },
            "no_color": {
                "done": "[OK]",
                "in_progress": "[..]",
                "blocked": "[!!]",
                "warning": "[!]",
                "pending": "[--]",
                "error": "[X]",
            },
        }
        return icons.get(self.theme, icons["default"]).get(icon_type, "•")


class StatusIndicator:
    """
    Color-coded status indicator for sejr items.

    Status types:
    - done: Green
    - in_progress: Blue
    - at_risk: Yellow
    - blocked: Red
    - pending: Gray
    """

    @staticmethod
    def get_icon(status: str) -> str:
        """Get status icon with color."""
        icons = {
            "done": f"{Colors.GREEN}[OK]{Colors.RESET}",
            "complete": f"{Colors.GREEN}[OK]{Colors.RESET}",
            "in_progress": f"{Colors.BLUE}[ACTIVE]{Colors.RESET}",
            "at_risk": f"{Colors.YELLOW}[WARN]{Colors.RESET}",
            "blocked": f"{Colors.RED}[BLOCKED]{Colors.RESET}",
            "pending": "⏳",
            "error": f"{Colors.RED}[FAIL]{Colors.RESET}",
        }
        return icons.get(status.lower(), "•")

    @staticmethod
    def get_progress_color(percentage: float) -> str:
        """Get color based on progress percentage."""
        if percentage >= 80:
            return Colors.GREEN
        elif percentage >= 50:
            return Colors.YELLOW
        else:
            return Colors.RED

    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Wrap text in color codes."""
        return f"{color}{text}{Colors.RESET}"


class SessionTimer:
    """
    Session timer for tracking work duration on sejr.

    Features:
    - Start/stop tracking
    - Pause/resume
    - Format output for display
    """

    def __init__(self):
        self.start_time: Optional[datetime] = None
        self.pause_time: Optional[datetime] = None
        self.paused_duration: timedelta = timedelta()
        self.is_paused: bool = False

    def start(self):
        """Start the session timer."""
        self.start_time = datetime.now()
        self.pause_time = None
        self.paused_duration = timedelta()
        self.is_paused = False

    def pause(self):
        """Pause the session timer."""
        if not self.is_paused and self.start_time:
            self.pause_time = datetime.now()
            self.is_paused = True

    def resume(self):
        """Resume the session timer."""
        if self.is_paused and self.pause_time:
            self.paused_duration += datetime.now() - self.pause_time
            self.pause_time = None
            self.is_paused = False

    def get_elapsed(self) -> timedelta:
        """Get elapsed time (excluding pauses)."""
        if not self.start_time:
            return timedelta()

        if self.is_paused and self.pause_time:
            return self.pause_time - self.start_time - self.paused_duration
        return datetime.now() - self.start_time - self.paused_duration

    def format_elapsed(self) -> str:
        """Format elapsed time as HH:MM:SS."""
        elapsed = self.get_elapsed()
        total_seconds = int(elapsed.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def render(self, width: int = 30) -> str:
        """Render timer for display."""
        elapsed = self.format_elapsed()
        status = "⏸ PAUSED" if self.is_paused else "▶ RUNNING"
        return f"⏱ Session: {elapsed} {status}"


class StatisticsView:
    """
    Statistics view for sejr system.

    Shows:
    - Total sejr completed
    - Total tests passed
    - Time saved (estimated)
    - Patterns learned
    """

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.archive_dir = system_path / "90_ARCHIVE"
        self.patterns_file = system_path / "_CURRENT" / "PATTERNS.yaml"

    def get_stats(self) -> Dict[str, Any]:
        """Calculate all statistics."""
        return {
            "sejr_completed": self._count_archived(),
            "tests_passed": self._count_tests(),
            "patterns_learned": self._count_patterns(),
            "time_saved_estimate": self._estimate_time_saved(),
            "total_checkboxes": self._count_total_checkboxes(),
        }

    def _count_archived(self) -> int:
        """Count archived sejr."""
        if not self.archive_dir.exists():
            return 0
        return len([d for d in self.archive_dir.iterdir() if d.is_dir()])

    def _count_tests(self) -> int:
        """Count total tests passed from archives."""
        count = 0
        if not self.archive_dir.exists():
            return 0

        for archive in self.archive_dir.iterdir():
            if archive.is_dir():
                conclusion = archive / "CONCLUSION.md"
                if conclusion.exists():
                    content = conclusion.read_text()
                    # Look for test count patterns
                    import re
                    match = re.search(r'(\d+)\s*tests?\s*passed', content, re.IGNORECASE)
                    if match:
                        count += int(match.group(1))

        return count

    def _count_patterns(self) -> int:
        """Count learned patterns."""
        if not self.patterns_file.exists():
            return 0

        try:
            content = self.patterns_file.read_text()
            return content.count("pattern:")
        except:
            return 0

    def _estimate_time_saved(self) -> str:
        """Estimate time saved by automation."""
        archived = self._count_archived()
        # Estimate 10 min saved per automated sejr workflow
        minutes = archived * 10
        hours = minutes // 60
        remaining_mins = minutes % 60
        return f"{hours}h {remaining_mins}m"

    def _count_total_checkboxes(self) -> int:
        """Count total checkboxes completed across all archives."""
        count = 0
        if not self.archive_dir.exists():
            return 0

        for archive in self.archive_dir.iterdir():
            if archive.is_dir():
                sejr_file = archive / "SEJR_LISTE.md"
                if sejr_file.exists():
                    content = sejr_file.read_text()
                    import re
                    count += len(re.findall(r'- \[[xX]\]', content))

        return count

    def render(self, width: int = 50) -> str:
        """Render statistics panel."""
        stats = self.get_stats()

        lines = []
        lines.append("=" * width)
        lines.append(f"{Colors.BOLD} STATISTICS{Colors.RESET}".center(width + 8))
        lines.append("=" * width)
        lines.append("")
        lines.append(f"  [OK] Sejr Completed:    {stats['sejr_completed']}")
        lines.append(f"   Tests Passed:      {stats['tests_passed']}")
        lines.append(f"   Checkboxes Done:   {stats['total_checkboxes']}")
        lines.append(f"   Patterns Learned:  {stats['patterns_learned']}")
        lines.append(f"  ⏱  Time Saved:        {stats['time_saved_estimate']}")
        lines.append("")
        lines.append("=" * width)

        return "\n".join(lines)


class RankDisplay:
    """
    Display military ranks based on score.

    Ranks:
    - KADET: 0-5 points
    - LØJTNANT: 6-12 points
    - KAPTAJN: 13-18 points
    - KOMMANDØR: 19-23 points
    - ADMIRAL: 24-27 points
    - GRAND ADMIRAL: 28-30 points
    """

    RANKS = [
        (0, "KADET", "", Colors.WHITE),
        (6, "LØJTNANT", "", Colors.CYAN),
        (13, "KAPTAJN", "", Colors.BLUE),
        (19, "KOMMANDØR", "", Colors.YELLOW),
        (24, "ADMIRAL", "", Colors.GREEN),
        (28, "GRAND ADMIRAL", "", Colors.BRIGHT_MAGENTA),
    ]

    @classmethod
    def get_rank(cls, score: int) -> tuple:
        """Get rank based on score. Returns (name, icon, color)."""
        for min_score, name, icon, color in reversed(cls.RANKS):
            if score >= min_score:
                return name, icon, color
        return "KADET", "", Colors.WHITE

    @classmethod
    def render_rank(cls, score: int) -> str:
        """Render rank with color and icon."""
        name, icon, color = cls.get_rank(score)
        return f"{color}{icon} {name}{Colors.RESET}"

    @classmethod
    def get_next_rank(cls, score: int) -> Optional[tuple]:
        """Get next rank and points needed."""
        for min_score, name, icon, color in cls.RANKS:
            if score < min_score:
                points_needed = min_score - score
                return name, points_needed
        return None  # Already max rank

    @classmethod
    def render_progress_to_next(cls, score: int) -> str:
        """Render progress to next rank."""
        next_rank = cls.get_next_rank(score)
        if next_rank is None:
            return f"{Colors.BRIGHT_MAGENTA}MAX RANK ACHIEVED!{Colors.RESET}"

        name, points_needed = next_rank
        return f"Next: {name} ({points_needed} points needed)"


class ProgressAnimation:
    """
    Terminal-friendly progress animation.

    Provides:
    - Spinning indicator
    - Progress bar with color
    - Completion celebration
    """

    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    COMPLETION_FRAMES = ["", "", "", "", ""]

    def __init__(self):
        self.frame_index = 0

    def get_spinner(self) -> str:
        """Get current spinner frame."""
        frame = self.SPINNER_FRAMES[self.frame_index % len(self.SPINNER_FRAMES)]
        self.frame_index += 1
        return frame

    @staticmethod
    def get_progress_bar(percentage: float, width: int = 20) -> str:
        """Get colored progress bar."""
        filled = int(percentage / 100 * width)
        empty = width - filled

        color = StatusIndicator.get_progress_color(percentage)

        bar = f"{color}{'█' * filled}{Colors.RESET}{'░' * empty}"
        return f"[{bar}] {percentage:.0f}%"

    @staticmethod
    def get_completion_message() -> str:
        """Get completion celebration message."""
        import random
        messages = [
            " FÆRDIG! Admiral niveau opnået!",
            " COMPLETE! Excellent execution!",
            " DONE! Another victory secured!",
            " FINISHED! Stellar performance!",
            " COMPLETE! Mission accomplished!",
        ]
        return random.choice(messages)


class VisualPolishWidget:
    """
    Main widget combining all visual polish features.

    Integrates:
    - Status indicators
    - Session timer
    - Statistics
    - Progress animations
    """

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.timer = SessionTimer()
        self.stats = StatisticsView(system_path)
        self.animation = ProgressAnimation()
        self.indicator = StatusIndicator()

    def start_session(self):
        """Start tracking session time."""
        self.timer.start()

    def get_status_icon(self, status: str) -> str:
        """Get colored status icon."""
        return self.indicator.get_icon(status)

    def get_progress_bar(self, percentage: float) -> str:
        """Get colored progress bar."""
        return self.animation.get_progress_bar(percentage)

    def get_timer_display(self) -> str:
        """Get timer display."""
        return self.timer.render()

    def get_stats_panel(self) -> str:
        """Get statistics panel."""
        return self.stats.render()

    def render_dashboard(self, width: int = 60) -> str:
        """Render complete visual dashboard."""
        lines = []
        lines.append("╔" + "═" * (width - 2) + "╗")
        lines.append(f"║{Colors.BOLD} SEJRLISTE VISUAL DASHBOARD {Colors.RESET}".center(width + 7) + "║")
        lines.append("╠" + "═" * (width - 2) + "╣")

        # Timer
        timer = self.timer.render()
        lines.append(f"║ {timer}".ljust(width - 1) + "║")

        lines.append("╠" + "─" * (width - 2) + "╣")

        # Stats summary
        stats = self.stats.get_stats()
        lines.append(f"║  Stats: {stats['sejr_completed']} sejr | {stats['tests_passed']} tests | {stats['time_saved_estimate']} saved".ljust(width - 1) + "║")

        lines.append("╚" + "═" * (width - 2) + "╝")

        return "\n".join(lines)


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    import time

    print("Testing Visual Polish Widgets...")

    # Test Colors
    print(f"\n{Colors.GREEN}GREEN{Colors.RESET} - Done")
    print(f"{Colors.YELLOW}YELLOW{Colors.RESET} - At Risk")
    print(f"{Colors.RED}RED{Colors.RESET} - Blocked")
    print(f"{Colors.BLUE}BLUE{Colors.RESET} - In Progress")

    # Test StatusIndicator
    print("\nStatus Icons:")
    for status in ["done", "in_progress", "at_risk", "blocked", "pending", "error"]:
        print(f"  {StatusIndicator.get_icon(status)} {status}")

    # Test ProgressAnimation
    print("\nProgress Bars:")
    for pct in [25, 50, 75, 100]:
        print(f"  {ProgressAnimation.get_progress_bar(pct)}")

    # Test SessionTimer
    print("\nSession Timer:")
    timer = SessionTimer()
    timer.start()
    time.sleep(1)
    print(f"  {timer.render()}")

    # Test StatisticsView (with mock path)
    print("\nStatistics View (sample):")
    # Only test if path exists
    test_path = Path(__file__).parent.parent.parent
    if test_path.exists():
        stats = StatisticsView(test_path)
        print(stats.render(40))

    # Test VisualPolishWidget
    print("\nVisual Dashboard:")
    if test_path.exists():
        widget = VisualPolishWidget(test_path)
        widget.start_session()
        time.sleep(0.5)
        print(widget.render_dashboard(50))

    print("\n[OK] Visual Polish test complete!")
