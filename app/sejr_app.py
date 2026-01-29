#!/usr/bin/env python3
"""
SEJRLISTE VISUAL APP - Steam-Style TUI
======================================
LIBRARY: Se alle dine sejr som games
PRODUCTION ROOM: Arbejd på aktiv sejr
DNA LAYERS: 7 automatiserede processer

Keyboard Shortcuts (Fra Plan):
- q: Quit
- j/k: Navigate up/down
- Enter: Open sejr (enter Production Room)
- Tab: Switch panel
- v: Run verification
- a: Archive completed
- p: Generate predictions
- n: New sejr
- r: Refresh all
- ?: Help
- Escape: Back to Library
"""

from __future__ import annotations
import os
import sys
import json
import yaml
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Static, Button, Label,
    ListItem, ListView, ProgressBar, RichLog, 
    DataTable, Tree, TabbedContent, TabPane,
    Checkbox, Rule, Markdown
)
from textual.screen import Screen
from textual.reactive import reactive
from textual.message import Message

# Base path
BASE_PATH = Path(__file__).parent.parent
SCRIPTS_PATH = BASE_PATH / "scripts"
ACTIVE_PATH = BASE_PATH / "10_ACTIVE"
ARCHIVE_PATH = BASE_PATH / "90_ARCHIVE"
CURRENT_PATH = BASE_PATH / "_CURRENT"
DNA_FILE = BASE_PATH / "DNA.yaml"

# ═══════════════════════════════════════════════════════════════════════════════
# STEAM-STYLE CSS - Dark Theme with Accent Colors
# ═══════════════════════════════════════════════════════════════════════════════
STEAM_CSS = """
/* Base Steam-like dark theme */
Screen {
    background: #1b2838;
}

/* Library Sidebar - Like Steam's left panel */
#library-sidebar {
    width: 30;
    background: #171a21;
    border-right: solid #2a475e;
    padding: 0 1;
}

#library-header {
    text-style: bold;
    color: #66c0f4;
    padding: 1 0;
    text-align: center;
    border-bottom: solid #2a475e;
}

.library-category {
    padding: 0 1;
    color: #8f98a0;
}

.library-category:hover {
    background: #2a475e;
    color: #c7d5e0;
}

.library-category:focus {
    background: #1a9fff;
    color: white;
}

/* Sejr Cards - Like Steam game tiles */
#main-content {
    padding: 1;
}

.sejr-card {
    width: 100%;
    height: 5;
    margin-bottom: 1;
    padding: 1;
    background: #2a475e;
    border: solid #3d6a8e;
}

.sejr-card:hover {
    background: #3d6a8e;
    border: solid #66c0f4;
}

.sejr-card:focus {
    background: #1a9fff;
    border: solid white;
}

.sejr-title {
    text-style: bold;
    color: #c7d5e0;
}

.sejr-progress {
    color: #66c0f4;
}

.sejr-status-active {
    color: #5ba32b;
}

.sejr-status-archived {
    color: #8f98a0;
}

/* Production Room - Active workspace */
#production-room {
    background: #1b2838;
    padding: 1;
}

#production-header {
    text-style: bold;
    color: #66c0f4;
    padding: 1;
    background: #171a21;
    border-bottom: solid #2a475e;
}

/* DNA Layers Panel */
#dna-panel {
    width: 25;
    background: #171a21;
    border-left: solid #2a475e;
    padding: 1;
}

.dna-layer {
    padding: 0 1;
    margin-bottom: 1;
}

.dna-layer-active {
    color: #5ba32b;
}

.dna-layer-pending {
    color: #8f98a0;
}

.dna-layer-running {
    color: #66c0f4;
    text-style: bold blink;
}

/* Log Stream */
#log-stream {
    background: #0d1117;
    border: solid #30363d;
    padding: 1;
    height: 10;
}

/* Task List */
#task-list {
    background: #1b2838;
    padding: 1;
}

.task-item {
    padding: 0 1;
}

.task-done {
    color: #5ba32b;
}

.task-pending {
    color: #c7d5e0;
}

/* Progress Bar Steam Style */
ProgressBar > .bar--bar {
    color: #1a9fff;
}

ProgressBar > .bar--complete {
    color: #5ba32b;
}

/* Buttons */
Button {
    margin: 0 1;
}

Button.primary {
    background: #1a9fff;
    color: white;
}

Button.primary:hover {
    background: #47bfff;
}

Button.success {
    background: #5ba32b;
    color: white;
}

Button.danger {
    background: #c23b23;
    color: white;
}

/* Header and Footer */
Header {
    background: #171a21;
}

Footer {
    background: #171a21;
}

/* Status indicators */
.status-good {
    color: #5ba32b;
}

.status-warning {
    color: #f7b93e;
}

.status-error {
    color: #c23b23;
}

/* Animations for live updates */
.pulse {
    text-style: bold;
}

/* Help overlay */
#help-panel {
    align: center middle;
    background: #171a21 80%;
    border: solid #66c0f4;
    padding: 2;
    width: 60;
    height: 30;
}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SEJR DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class Sejr:
    """Represents a single Sejr (Victory) project"""
    def __init__(self, path: Path, is_archived: bool = False):
        self.path = path
        self.name = path.name
        self.is_archived = is_archived
        self.progress = 0.0
        self.score = "0/30"
        self.phase = "UNKNOWN"
        self.tasks_total = 0
        self.tasks_done = 0
        self.load_status()
    
    def load_status(self):
        """Load status from VERIFY_STATUS.yaml"""
        status_file = self.path / "VERIFY_STATUS.yaml"
        if status_file.exists():
            try:
                with open(status_file) as f:
                    data = yaml.safe_load(f) or {}
                    self.progress = data.get("completion_percentage", 0)
                    self.score = f"{data.get('current_score', 0)}/30"
                    self.phase = data.get("current_phase", "UNKNOWN")
            except Exception:
                pass
        
        # Count tasks from SEJR_LISTE.md
        sejr_file = self.path / "SEJR_LISTE.md"
        if sejr_file.exists():
            try:
                content = sejr_file.read_text()
                self.tasks_total = content.count("- [ ]") + content.count("- [x]")
                self.tasks_done = content.count("- [x]")
                if self.tasks_total > 0:
                    self.progress = (self.tasks_done / self.tasks_total) * 100
            except Exception:
                pass

    @property
    def status_class(self) -> str:
        if self.is_archived:
            return "sejr-status-archived"
        return "sejr-status-active"


# ═══════════════════════════════════════════════════════════════════════════════
# LIBRARY SCREEN - Steam-like game library
# ═══════════════════════════════════════════════════════════════════════════════

class LibrarySidebar(Container):
    """Steam-like sidebar with library categories"""
    
    def compose(self) -> ComposeResult:
        yield Static("📚 LIBRARY", id="library-header")
        yield Rule()
        yield Button("🎮 Aktive Sejr", id="btn-active", classes="library-category")
        yield Button("🏆 Arkiverede", id="btn-archived", classes="library-category")
        yield Button("📊 Statistik", id="btn-stats", classes="library-category")
        yield Rule()
        yield Static("⌨️ SHORTCUTS", classes="library-category")
        yield Static("v: Verify", classes="library-category")
        yield Static("a: Archive", classes="library-category")
        yield Static("p: Predict", classes="library-category")
        yield Static("n: New Sejr", classes="library-category")
        yield Static("?: Help", classes="library-category")


class SejrCard(Static):
    """A single Sejr displayed as a Steam-like game card"""
    
    def __init__(self, sejr: Sejr) -> None:
        super().__init__()
        self.sejr = sejr
        self.classes = "sejr-card"
    
    def compose(self) -> ComposeResult:
        status_icon = "🏆" if self.sejr.is_archived else "🎮"
        progress_bar = "█" * int(self.sejr.progress / 10) + "░" * (10 - int(self.sejr.progress / 10))
        
        yield Static(f"{status_icon} {self.sejr.name}", classes="sejr-title")
        yield Static(f"   [{progress_bar}] {self.sejr.progress:.0f}% | Score: {self.sejr.score}", classes="sejr-progress")
        yield Static(f"   Phase: {self.sejr.phase} | Tasks: {self.sejr.tasks_done}/{self.sejr.tasks_total}", classes=self.sejr.status_class)


class SejrGrid(ScrollableContainer):
    """Grid of Sejr cards - like Steam's game grid"""
    
    def __init__(self, sejrs: List[Sejr]) -> None:
        super().__init__()
        self.sejrs = sejrs
        self.selected_index = 0
    
    def compose(self) -> ComposeResult:
        if not self.sejrs:
            yield Static("Ingen sejr fundet. Tryk 'n' for at oprette ny.", classes="library-category")
        else:
            for sejr in self.sejrs:
                yield SejrCard(sejr)
    
    def select_next(self):
        if self.sejrs:
            self.selected_index = min(self.selected_index + 1, len(self.sejrs) - 1)
    
    def select_prev(self):
        if self.sejrs:
            self.selected_index = max(self.selected_index - 1, 0)
    
    @property
    def selected_sejr(self) -> Optional[Sejr]:
        if self.sejrs and 0 <= self.selected_index < len(self.sejrs):
            return self.sejrs[self.selected_index]
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# PRODUCTION ROOM SCREEN - Active workspace
# ═══════════════════════════════════════════════════════════════════════════════

class DNALayerWidget(Static):
    """Shows the 7 DNA layers status"""
    
    DNA_LAYERS = [
        ("1", "SELF-AWARE", "DNA.yaml"),
        ("2", "SELF-DOCUMENTING", "auto_track.py"),
        ("3", "SELF-VERIFYING", "auto_verify.py"),
        ("4", "SELF-IMPROVING", "auto_learn.py"),
        ("5", "SELF-ARCHIVING", "auto_archive.py"),
        ("6", "PREDICTIVE", "auto_predict.py"),
        ("7", "SELF-OPTIMIZING", "generate_sejr.py"),
    ]
    
    active_layer = reactive(0)
    
    def compose(self) -> ComposeResult:
        yield Static("🧬 DNA LAYERS", id="dna-header")
        yield Rule()
        for num, name, script in self.DNA_LAYERS:
            status = "✅" if int(num) <= self.active_layer else "⬜"
            yield Static(f"{status} {num}. {name}", classes="dna-layer")


class TaskListWidget(ScrollableContainer):
    """Shows tasks from SEJR_LISTE.md with checkboxes"""
    
    def __init__(self, sejr_path: Path) -> None:
        super().__init__()
        self.sejr_path = sejr_path
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        sejr_file = self.sejr_path / "SEJR_LISTE.md"
        if sejr_file.exists():
            content = sejr_file.read_text()
            self.tasks = []
            for line in content.split("\n"):
                if "- [ ]" in line:
                    task = line.replace("- [ ]", "").strip()
                    self.tasks.append(("pending", task))
                elif "- [x]" in line:
                    task = line.replace("- [x]", "").strip()
                    self.tasks.append(("done", task))
    
    def compose(self) -> ComposeResult:
        yield Static("📋 TASK LIST", id="task-header")
        yield Rule()
        for status, task in self.tasks[:20]:  # Limit to 20 visible
            icon = "✅" if status == "done" else "⬜"
            cls = "task-done" if status == "done" else "task-pending"
            yield Static(f"{icon} {task[:50]}", classes=f"task-item {cls}")


class LogStreamWidget(RichLog):
    """Live stream of AUTO_LOG.jsonl"""
    
    def __init__(self, sejr_path: Path) -> None:
        super().__init__(highlight=True, markup=True)
        self.sejr_path = sejr_path
    
    def load_recent_logs(self, count: int = 10):
        log_file = self.sejr_path / "AUTO_LOG.jsonl"
        if log_file.exists():
            lines = log_file.read_text().strip().split("\n")[-count:]
            for line in lines:
                try:
                    entry = json.loads(line)
                    ts = entry.get("timestamp", "")[:19]
                    action = entry.get("action", "unknown")
                    self.write(f"[dim]{ts}[/] [cyan]{action}[/]")
                except Exception:
                    pass


class ProductionRoom(Container):
    """The active workspace when working on a Sejr"""
    
    def __init__(self, sejr: Sejr) -> None:
        super().__init__()
        self.sejr = sejr
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            # Main content area
            with Vertical(id="production-main"):
                yield Static(f"🎮 PRODUCTION ROOM: {self.sejr.name}", id="production-header")
                yield Rule()
                
                # Progress overview
                progress = self.sejr.progress / 100
                yield Static(f"Progress: {self.sejr.progress:.0f}% | Score: {self.sejr.score}")
                yield ProgressBar(total=100, show_eta=False)
                yield Rule()
                
                # Task list
                yield TaskListWidget(self.sejr.path)
                
                yield Rule()
                
                # Log stream
                yield Static("📡 LIVE LOG STREAM", id="log-header")
                log_widget = LogStreamWidget(self.sejr.path)
                log_widget.id = "log-stream"
                yield log_widget
            
            # DNA Layers sidebar
            with Container(id="dna-panel"):
                yield DNALayerWidget()
                yield Rule()
                yield Static("⌨️ ACTIONS")
                yield Button("v: Verify", id="btn-verify", variant="primary")
                yield Button("a: Archive", id="btn-archive", variant="success")
                yield Button("p: Predict", id="btn-predict", variant="default")
                yield Button("Esc: Back", id="btn-back", variant="warning")


# ═══════════════════════════════════════════════════════════════════════════════
# HELP SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

class HelpScreen(Screen):
    """Help overlay with keyboard shortcuts"""
    
    BINDINGS = [
        Binding("escape", "dismiss", "Back"),
        Binding("?", "dismiss", "Close Help"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Container(
            Static("""
# ⌨️ KEYBOARD SHORTCUTS

## Navigation
- **j/k** or **↓/↑**: Navigate up/down
- **Enter**: Open selected Sejr (Production Room)
- **Tab**: Switch between panels
- **Escape**: Back to Library

## Actions
- **v**: Run verification (auto_verify.py)
- **a**: Archive completed sejr (auto_archive.py)
- **p**: Generate predictions (auto_predict.py)
- **n**: Create new sejr (generate_sejr.py)
- **r**: Refresh all data

## App
- **q**: Quit
- **?**: Toggle this help

---
*Press Escape or ? to close*
            """, id="help-content"),
            id="help-panel"
        )
    
    def action_dismiss(self):
        self.app.pop_screen()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

class SejrlisteApp(App):
    """
    SEJRLISTE VISUAL APP
    ====================
    Steam-style TUI for tracking victories
    
    Features:
    - LIBRARY: View all your sejr like games
    - PRODUCTION ROOM: Work on active sejr
    - DNA LAYERS: 7 automated processes
    - LIVE UPDATES: Real-time file watching
    """
    
    CSS = STEAM_CSS
    TITLE = "SEJRLISTE"
    SUB_TITLE = "Admiral Command Center"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("?", "toggle_help", "Help"),
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
        Binding("down", "move_down", "Down", show=False),
        Binding("up", "move_up", "Up", show=False),
        Binding("enter", "select_sejr", "Select"),
        Binding("escape", "back_to_library", "Back"),
        Binding("tab", "switch_panel", "Switch Panel"),
        Binding("v", "run_verify", "Verify"),
        Binding("a", "run_archive", "Archive"),
        Binding("p", "run_predict", "Predict"),
        Binding("n", "new_sejr", "New Sejr"),
        Binding("r", "refresh", "Refresh"),
    ]
    
    # State
    current_view = reactive("library")
    selected_sejr: Optional[Sejr] = None
    sejrs: List[Sejr] = []
    show_archived = reactive(False)
    session_start: datetime = None

    def __init__(self):
        super().__init__()
        self.session_start = datetime.now()
        self.load_sejrs()

    def on_mount(self) -> None:
        """Called when app is mounted - safe to use set_interval here."""
        self.set_interval(1.0, self.update_session_timer)

    def get_session_duration(self) -> str:
        """Get formatted session duration"""
        if self.session_start:
            delta = datetime.now() - self.session_start
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                return f"{hours}t {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        return "0s"

    def update_session_timer(self) -> None:
        """Update the session timer display"""
        self.sub_title = f"Admiral Command Center | Session: {self.get_session_duration()}"

    def play_sound(self, sound_type: str = "success") -> None:
        """Play notification sound (optional - can be disabled)"""
        try:
            if sound_type == "success":
                # Terminal bell for success
                print('\a', end='', flush=True)
            elif sound_type == "error":
                # Double bell for error
                print('\a\a', end='', flush=True)
        except Exception:
            pass  # Sound is optional, don't fail if it doesn't work
    
    def load_sejrs(self):
        """Load all sejr from 10_ACTIVE and 90_ARCHIVE"""
        self.sejrs = []
        
        # Active sejr
        if ACTIVE_PATH.exists():
            for folder in ACTIVE_PATH.iterdir():
                if folder.is_dir() and not folder.name.startswith("."):
                    self.sejrs.append(Sejr(folder, is_archived=False))
        
        # Archived sejr (if showing)
        if self.show_archived and ARCHIVE_PATH.exists():
            for folder in sorted(ARCHIVE_PATH.iterdir(), reverse=True)[:10]:  # Last 10
                if folder.is_dir() and not folder.name.startswith("."):
                    self.sejrs.append(Sejr(folder, is_archived=True))
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal():
            # Left sidebar - Library
            yield LibrarySidebar()
            
            # Main content area
            with Container(id="main-content"):
                if self.current_view == "library":
                    yield SejrGrid(self.sejrs)
                elif self.current_view == "production" and self.selected_sejr:
                    yield ProductionRoom(self.selected_sejr)
        
        yield Footer()
    
    def action_toggle_help(self):
        """Show/hide help screen"""
        self.push_screen(HelpScreen())
    
    def action_move_down(self):
        """Move selection down"""
        grid = self.query_one(SejrGrid, SejrGrid) if self.query(SejrGrid) else None
        if grid:
            grid.select_next()
            self.refresh()
    
    def action_move_up(self):
        """Move selection up"""
        grid = self.query_one(SejrGrid, SejrGrid) if self.query(SejrGrid) else None
        if grid:
            grid.select_prev()
            self.refresh()
    
    def action_select_sejr(self):
        """Open selected sejr in Production Room"""
        grid = self.query_one(SejrGrid, SejrGrid) if self.query(SejrGrid) else None
        if grid and grid.selected_sejr:
            self.selected_sejr = grid.selected_sejr
            self.current_view = "production"
            self.refresh()
    
    def action_back_to_library(self):
        """Return to library view"""
        self.current_view = "library"
        self.refresh()
    
    def action_switch_panel(self):
        """Switch focus between panels"""
        self.focus_next()
    
    @work(exclusive=True)
    async def action_run_verify(self):
        """Run auto_verify.py"""
        script = SCRIPTS_PATH / "auto_verify.py"
        if script.exists():
            self.notify("Running verification...", severity="information")
            result = subprocess.run(
                ["python3", str(script)],
                cwd=str(BASE_PATH),
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.notify("✅ Verification complete!", severity="information")
                self.play_sound("success")
            else:
                self.notify(f"❌ Verification failed: {result.stderr[:100]}", severity="error")
                self.play_sound("error")
            self.load_sejrs()
            self.refresh()
    
    @work(exclusive=True)
    async def action_run_archive(self):
        """Run auto_archive.py"""
        script = SCRIPTS_PATH / "auto_archive.py"
        if script.exists():
            self.notify("Running archive...", severity="information")
            result = subprocess.run(
                ["python3", str(script)],
                cwd=str(BASE_PATH),
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.notify("🏆 Archive complete!", severity="information")
                self.play_sound("success")
            else:
                self.notify(f"❌ Archive failed: {result.stderr[:100]}", severity="error")
                self.play_sound("error")
            self.load_sejrs()
            self.refresh()
    
    @work(exclusive=True)
    async def action_run_predict(self):
        """Run auto_predict.py"""
        script = SCRIPTS_PATH / "auto_predict.py"
        if script.exists():
            self.notify("Generating predictions...", severity="information")
            result = subprocess.run(
                ["python3", str(script)],
                cwd=str(BASE_PATH),
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.notify("🔮 Predictions generated!", severity="information")
                self.play_sound("success")
            else:
                self.notify(f"❌ Predict failed: {result.stderr[:100]}", severity="error")
                self.play_sound("error")
    
    @work(exclusive=True)
    async def action_new_sejr(self):
        """Run generate_sejr.py to create new sejr"""
        script = SCRIPTS_PATH / "generate_sejr.py"
        if script.exists():
            self.notify("Creating new sejr...", severity="information")
            # This would normally prompt for name, but for now:
            result = subprocess.run(
                ["python3", str(script), "--name", f"NEW_SEJR_{datetime.now().strftime('%Y%m%d_%H%M')}"],
                cwd=str(BASE_PATH),
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.notify("✨ New sejr created!", severity="information")
                self.play_sound("success")
            else:
                self.notify(f"❌ Create failed: {result.stderr[:100]}", severity="error")
                self.play_sound("error")
            self.load_sejrs()
            self.refresh()
    
    def action_refresh(self):
        """Refresh all data"""
        self.load_sejrs()
        self.notify("🔄 Data refreshed", severity="information")
        self.refresh()
    
    @on(Button.Pressed, "#btn-active")
    def show_active(self):
        self.show_archived = False
        self.load_sejrs()
        self.refresh()
    
    @on(Button.Pressed, "#btn-archived")
    def show_archived_sejr(self):
        self.show_archived = True
        self.load_sejrs()
        self.refresh()
    
    @on(Button.Pressed, "#btn-verify")
    def button_verify(self):
        self.action_run_verify()
    
    @on(Button.Pressed, "#btn-archive")
    def button_archive(self):
        self.action_run_archive()
    
    @on(Button.Pressed, "#btn-predict")
    def button_predict(self):
        self.action_run_predict()
    
    @on(Button.Pressed, "#btn-back")
    def button_back(self):
        self.action_back_to_library()


# ═══════════════════════════════════════════════════════════════════════════════
# FILE WATCHER (for real-time updates)
# ═══════════════════════════════════════════════════════════════════════════════

async def run_app():
    """Run the app with optional file watching"""
    app = SejrlisteApp()
    await app.run_async()


def main():
    """Entry point"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    SEJRLISTE VISUAL APP                       ║
║                   Steam-Style TUI v2026.1                     ║
╠═══════════════════════════════════════════════════════════════╣
║  LIBRARY: Browse your victories like games                    ║
║  PRODUCTION ROOM: Active workspace for current sejr           ║
║  DNA LAYERS: 7 automated processes                            ║
╠═══════════════════════════════════════════════════════════════╣
║  Shortcuts: j/k=navigate, Enter=open, v=verify, ?=help        ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    app = SejrlisteApp()
    app.run()


if __name__ == "__main__":
    main()
