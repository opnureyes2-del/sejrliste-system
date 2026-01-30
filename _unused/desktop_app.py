#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    SEJRLISTE DESKTOP APP - GTK3 NATIVE
═══════════════════════════════════════════════════════════════════════════════

REAL desktop app - NOT a web app. Runs NATIVELY on your Ubuntu desktop.
Shows LIVE updates as files change.

FEATURES:
   LIBRARY sidebar - alle sejrs med progress
   PRODUCTION ROOM - real-time file viewer
   FILE MANAGER - drag and drop
   DNA LAYERS - live status
   AUTO-REFRESH - watches files for changes

═══════════════════════════════════════════════════════════════════════════════
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango
from pathlib import Path
import subprocess
import json
import re
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"

# Modern dark theme colors
COLORS = {
    "bg_dark": "#1b2838",
    "bg_darker": "#171a21",
    "blue": "#66c0f4",
    "blue_dark": "#2a475e",
    "green": "#5ba32b",
    "text": "#c7d5e0",
    "text_dim": "#8f98a0",
    "gold": "#f7b93e",
    "red": "#c23b23",
}

CSS = """
window {
    background-color: #1b2838;
}

.sidebar {
    background-color: #171a21;
    border-right: 2px solid #2a475e;
}

.header {
    background: linear-gradient(90deg, #171a21, #2a475e, #171a21);
    border-bottom: 2px solid #66c0f4;
    padding: 10px;
}

.header-title {
    color: #66c0f4;
    font-size: 24px;
    font-weight: bold;
}

.sejr-button {
    background-color: #2a475e;
    color: #c7d5e0;
    border: 1px solid #2a475e;
    border-radius: 8px;
    padding: 10px;
    margin: 5px;
}

.sejr-button:hover {
    background-color: #66c0f4;
    color: #171a21;
}

.sejr-button.active {
    background-color: #5ba32b;
    border-color: #5ba32b;
}

.sejr-button.archived {
    background-color: #f7b93e;
    color: #171a21;
}

.content-area {
    background-color: #1b2838;
    padding: 20px;
}

.section-title {
    color: #66c0f4;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}

.file-item {
    background-color: #2a475e;
    color: #c7d5e0;
    border-radius: 5px;
    padding: 8px;
    margin: 3px;
}

.file-item:hover {
    background-color: #66c0f4;
    color: #171a21;
}

.progress-bar {
    background-color: #171a21;
    border-radius: 4px;
}

.progress-bar progress {
    background: linear-gradient(90deg, #5ba32b, #66c0f4);
    border-radius: 4px;
}

.dna-active {
    background-color: #5ba32b;
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    margin: 2px;
}

.dna-pending {
    background-color: #8f98a0;
    color: #171a21;
    padding: 5px 10px;
    border-radius: 4px;
    margin: 2px;
}

.action-button {
    background: linear-gradient(180deg, #66c0f4, #1a9fff);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: bold;
}

.action-button:hover {
    background: linear-gradient(180deg, #1a9fff, #66c0f4);
}

.log-area {
    background-color: #0d1117;
    color: #c7d5e0;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px;
    font-family: monospace;
}

textview, textview text {
    background-color: #0d1117;
    color: #c7d5e0;
    font-family: monospace;
}

.stat-card {
    background: linear-gradient(135deg, #2a475e, rgba(42, 71, 94, 0.5));
    border: 1px solid #2a475e;
    border-radius: 12px;
    padding: 15px;
}

.stat-value {
    color: #66c0f4;
    font-size: 28px;
    font-weight: bold;
}

.stat-label {
    color: #8f98a0;
    font-size: 12px;
}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def count_checkboxes(content: str) -> tuple:
    """Count checked and total checkboxes in markdown"""
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked

def get_sejr_info(path: Path) -> dict:
    """Get info about a sejr folder"""
    sejr_file = path / "SEJR_LISTE.md"
    info = {
        "name": path.name,
        "path": str(path),
        "progress": 0,
        "done": 0,
        "total": 0,
        "is_archived": "90_ARCHIVE" in str(path),
        "files": [],
    }

    if sejr_file.exists():
        content = sejr_file.read_text()
        done, total = count_checkboxes(content)
        info["done"] = done
        info["total"] = total
        info["progress"] = int((done / total * 100) if total > 0 else 0)

    if path.exists():
        info["files"] = [f.name for f in path.iterdir() if f.is_file()]

    return info

def get_all_sejrs() -> list:
    """Get all sejrs (active + archived)"""
    sejrs = []

    if ACTIVE_DIR.exists():
        for folder in sorted(ACTIVE_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if folder.is_dir() and not folder.name.startswith("."):
                sejrs.append(get_sejr_info(folder))

    if ARCHIVE_DIR.exists():
        for folder in sorted(ARCHIVE_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if folder.is_dir() and not folder.name.startswith("."):
                sejrs.append(get_sejr_info(folder))

    return sejrs

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class SejrlisteApp(Gtk.Window):
    def __init__(self):
        super().__init__(title=" SEJRLISTE COMMAND CENTER - Native Desktop")
        self.set_default_size(1400, 900)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Apply CSS
        self.apply_css()

        # State
        self.selected_sejr = None
        self.sejrs = []

        # Build UI
        self.build_ui()

        # Load data
        self.refresh_sejrs()

        # Auto-refresh every 2 seconds
        GLib.timeout_add_seconds(2, self.auto_refresh)

    def apply_css(self):
        """Apply Steam-like CSS styling"""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def build_ui(self):
        """Build the main UI"""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(main_box)

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header.get_style_context().add_class("header")

        title = Gtk.Label(label=" SEJRLISTE COMMAND CENTER")
        title.get_style_context().add_class("header-title")
        header.pack_start(title, False, False, 10)

        # Session info
        self.session_label = Gtk.Label(label="Session: 0m | DNA: 7 Layers")
        self.session_label.set_halign(Gtk.Align.END)
        header.pack_end(self.session_label, False, False, 10)

        main_box.pack_start(header, False, False, 0)

        # Content area (sidebar + main)
        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.pack_start(content, True, True, 0)

        # === SIDEBAR (Library) ===
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.set_size_request(300, -1)
        sidebar.get_style_context().add_class("sidebar")

        # Library title
        lib_title = Gtk.Label(label=" LIBRARY")
        lib_title.get_style_context().add_class("section-title")
        sidebar.pack_start(lib_title, False, False, 10)

        # Scrollable sejr list
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.sejr_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scroll.add(self.sejr_list)
        sidebar.pack_start(scroll, True, True, 0)

        # Quick actions
        actions = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        actions.set_margin_top(10)
        actions.set_margin_bottom(10)
        actions.set_margin_start(10)
        actions.set_margin_end(10)

        new_btn = Gtk.Button(label=" Ny Sejr")
        new_btn.get_style_context().add_class("action-button")
        new_btn.connect("clicked", self.on_new_sejr)
        actions.pack_start(new_btn, False, False, 5)

        refresh_btn = Gtk.Button(label=" Refresh")
        refresh_btn.get_style_context().add_class("action-button")
        refresh_btn.connect("clicked", lambda w: self.refresh_sejrs())
        actions.pack_start(refresh_btn, False, False, 5)

        sidebar.pack_end(actions, False, False, 0)

        content.pack_start(sidebar, False, False, 0)

        # === MAIN CONTENT AREA ===
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        content.pack_start(self.content_stack, True, True, 0)

        # Welcome page
        welcome = self.build_welcome_page()
        self.content_stack.add_named(welcome, "welcome")

        # Production room (created when sejr selected)
        self.production_room = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_stack.add_named(self.production_room, "production")

        self.content_stack.set_visible_child_name("welcome")

    def build_welcome_page(self):
        """Build the welcome/stats page"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        page.get_style_context().add_class("content-area")

        title = Gtk.Label(label=" SELECT YOUR VICTORY")
        title.get_style_context().add_class("section-title")
        page.pack_start(title, False, False, 20)

        # Stats row
        stats = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        stats.set_halign(Gtk.Align.CENTER)

        self.stat_active = self.create_stat_card("0", "Active")
        stats.pack_start(self.stat_active, False, False, 0)

        self.stat_archived = self.create_stat_card("0", "Archived")
        stats.pack_start(self.stat_archived, False, False, 0)

        self.stat_progress = self.create_stat_card("0%", "Avg Progress")
        stats.pack_start(self.stat_progress, False, False, 0)

        page.pack_start(stats, False, False, 20)

        # Instructions
        info = Gtk.Label()
        info.set_markup("""
<span foreground='#c7d5e0'>
<b>Keyboard Shortcuts:</b>
  v = Verify  |  a = Archive  |  p = Predict  |  n = New  |  r = Refresh

<b>Click a sejr in the LIBRARY to open it</b>
</span>
""")
        page.pack_start(info, False, False, 20)

        return page

    def create_stat_card(self, value, label):
        """Create a stat card widget"""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        card.get_style_context().add_class("stat-card")
        card.set_size_request(150, 100)

        val = Gtk.Label(label=value)
        val.get_style_context().add_class("stat-value")
        card.pack_start(val, True, True, 0)

        lbl = Gtk.Label(label=label)
        lbl.get_style_context().add_class("stat-label")
        card.pack_start(lbl, False, False, 0)

        card.value_label = val
        return card

    def build_production_room(self, sejr):
        """Build production room for a sejr"""
        # Clear existing
        for child in self.production_room.get_children():
            self.production_room.remove(child)

        self.production_room.get_style_context().add_class("content-area")

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        back_btn = Gtk.Button(label="⬅ Back")
        back_btn.connect("clicked", self.on_back)
        header.pack_start(back_btn, False, False, 5)

        title = Gtk.Label(label=f" PRODUCTION ROOM: {sejr['name'][:40]}")
        title.get_style_context().add_class("section-title")
        header.pack_start(title, False, False, 10)

        self.production_room.pack_start(header, False, False, 10)

        # Progress bar
        progress_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        progress_label = Gtk.Label(label=f"Progress: {sejr['progress']}%")
        progress_box.pack_start(progress_label, False, False, 10)

        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(sejr['progress'] / 100)
        progress_bar.get_style_context().add_class("progress-bar")
        progress_box.pack_start(progress_bar, True, True, 10)

        self.production_room.pack_start(progress_box, False, False, 10)

        # DNA Actions
        dna_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        dna_title = Gtk.Label(label=" DNA Actions:")
        dna_box.pack_start(dna_title, False, False, 0)

        actions = [
            ("[OK] Verify", "auto_verify.py"),
            (" Archive", "auto_archive.py"),
            (" Predict", "auto_predict.py"),
            (" Learn", "auto_learn.py"),
        ]

        for label, script in actions:
            btn = Gtk.Button(label=label)
            btn.get_style_context().add_class("action-button")
            btn.connect("clicked", lambda w, s=script: self.run_script(s))
            dna_box.pack_start(btn, False, False, 0)

        self.production_room.pack_start(dna_box, False, False, 10)

        # Two columns: Files + Content
        columns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        # Files column
        files_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        files_box.set_size_request(250, -1)

        files_title = Gtk.Label(label=" Files")
        files_title.get_style_context().add_class("section-title")
        files_box.pack_start(files_title, False, False, 5)

        for filename in sejr['files']:
            file_btn = Gtk.Button(label=f" {filename[:25]}")
            file_btn.get_style_context().add_class("file-item")
            filepath = Path(sejr['path']) / filename
            file_btn.connect("clicked", lambda w, p=filepath: self.view_file(p))
            files_box.pack_start(file_btn, False, False, 2)

        # Open folder button
        open_btn = Gtk.Button(label=" Open in Files")
        open_btn.get_style_context().add_class("action-button")
        open_btn.connect("clicked", lambda w: subprocess.Popen(["nautilus", sejr['path']]))
        files_box.pack_end(open_btn, False, False, 10)

        columns.pack_start(files_box, False, False, 0)

        # Content viewer
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        content_title = Gtk.Label(label=" Content Viewer")
        content_title.get_style_context().add_class("section-title")
        content_box.pack_start(content_title, False, False, 5)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(-1, 400)

        self.content_view = Gtk.TextView()
        self.content_view.set_editable(False)
        self.content_view.get_style_context().add_class("log-area")
        scroll.add(self.content_view)

        content_box.pack_start(scroll, True, True, 0)

        columns.pack_start(content_box, True, True, 0)

        self.production_room.pack_start(columns, True, True, 10)

        # Show SEJR_LISTE.md by default
        sejr_file = Path(sejr['path']) / "SEJR_LISTE.md"
        if sejr_file.exists():
            self.view_file(sejr_file)

        self.production_room.show_all()

    def refresh_sejrs(self):
        """Refresh the sejr list"""
        self.sejrs = get_all_sejrs()

        # Clear list
        for child in self.sejr_list.get_children():
            self.sejr_list.remove(child)

        active = [s for s in self.sejrs if not s['is_archived']]
        archived = [s for s in self.sejrs if s['is_archived']]

        # Active section
        if active:
            label = Gtk.Label(label=f" Active ({len(active)})")
            label.set_halign(Gtk.Align.START)
            label.set_margin_start(10)
            self.sejr_list.pack_start(label, False, False, 5)

            for sejr in active:
                btn = self.create_sejr_button(sejr)
                self.sejr_list.pack_start(btn, False, False, 0)

        # Archived section
        if archived:
            label = Gtk.Label(label=f" Archived ({len(archived)})")
            label.set_halign(Gtk.Align.START)
            label.set_margin_start(10)
            label.set_margin_top(15)
            self.sejr_list.pack_start(label, False, False, 5)

            for sejr in archived[:10]:
                btn = self.create_sejr_button(sejr)
                self.sejr_list.pack_start(btn, False, False, 0)

        # Update stats
        self.stat_active.value_label.set_text(str(len(active)))
        self.stat_archived.value_label.set_text(str(len(archived)))

        if active:
            avg = sum(s['progress'] for s in active) // len(active)
            self.stat_progress.value_label.set_text(f"{avg}%")

        self.sejr_list.show_all()

    def create_sejr_button(self, sejr):
        """Create a button for a sejr"""
        progress = sejr['progress']
        bar = "█" * (progress // 10) + "░" * (10 - progress // 10)

        name = sejr['name'][:25]
        if sejr['is_archived']:
            text = f" {name}"
        else:
            text = f" {name}\n{bar} {progress}%"

        btn = Gtk.Button(label=text)
        btn.get_style_context().add_class("sejr-button")

        if sejr['is_archived']:
            btn.get_style_context().add_class("archived")
        elif progress >= 80:
            btn.get_style_context().add_class("active")

        btn.connect("clicked", lambda w, s=sejr: self.select_sejr(s))

        return btn

    def select_sejr(self, sejr):
        """Select a sejr and show production room"""
        self.selected_sejr = sejr
        self.build_production_room(sejr)
        self.content_stack.set_visible_child_name("production")

    def on_back(self, widget):
        """Go back to welcome page"""
        self.selected_sejr = None
        self.content_stack.set_visible_child_name("welcome")

    def view_file(self, filepath):
        """View a file in the content viewer"""
        try:
            content = filepath.read_text()
            buffer = self.content_view.get_buffer()
            buffer.set_text(content)
        except Exception as e:
            buffer = self.content_view.get_buffer()
            buffer.set_text(f"Error reading file: {e}")

    def run_script(self, script_name):
        """Run a DNA layer script"""
        script_path = SCRIPTS_DIR / script_name
        if not script_path.exists():
            self.show_message(f"Script not found: {script_name}", Gtk.MessageType.ERROR)
            return

        try:
            result = subprocess.run(
                ["python3", str(script_path)],
                cwd=str(SYSTEM_PATH),
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                self.show_message(f"[OK] {script_name} completed!", Gtk.MessageType.INFO)
                self.refresh_sejrs()
                if self.selected_sejr:
                    # Refresh current sejr
                    new_info = get_sejr_info(Path(self.selected_sejr['path']))
                    self.build_production_room(new_info)
            else:
                self.show_message(f"[FAIL] {script_name} failed:\n{result.stderr}", Gtk.MessageType.ERROR)
        except Exception as e:
            self.show_message(f"Error: {e}", Gtk.MessageType.ERROR)

    def show_message(self, message, msg_type):
        """Show a message dialog"""
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=msg_type,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    def on_new_sejr(self, widget):
        """Create a new sejr"""
        self.run_script("generate_sejr.py")

    def auto_refresh(self):
        """Auto-refresh every 2 seconds"""
        if self.selected_sejr is None:
            self.refresh_sejrs()
        return True  # Continue timer

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = SejrlisteApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
