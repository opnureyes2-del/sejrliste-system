#!/usr/bin/env python3
"""
SEJR LAUNCHER - Steam-Style App for Sejrliste System
=====================================================

En visuel launcher til at oprette og administrere sejrliste mapper.
Inspireret af Steam's game library interface.

INGEN EXTERNAL DEPENDENCIES - Kun Python standard library (tkinter)

Brug: python sejr_launcher.py

Author: Kv1nt + Rasmus
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# ============================================================================
# CONFIGURATION
# ============================================================================

SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
CURRENT_DIR = SYSTEM_PATH / "_CURRENT"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"
TEMPLATES_DIR = SYSTEM_PATH / "00_TEMPLATES"

# Colors (Steam-inspired dark theme)
COLORS = {
    "bg_dark": "#1b2838",        # Dark blue background
    "bg_medium": "#2a475e",      # Medium blue
    "bg_light": "#66c0f4",       # Light blue accent
    "text": "#c7d5e0",           # Light text
    "text_dim": "#7a8b8f",       # Dimmed text
    "accent": "#66c0f4",         # Steam blue
    "success": "#5ba32b",        # Green
    "warning": "#f0a000",        # Orange
    "error": "#cd5050",          # Red
    "card_bg": "#1e3a4c",        # Card background
    "card_hover": "#2a475e",     # Card hover
}

# ============================================================================
# DATA PARSING (No external dependencies)
# ============================================================================

def parse_yaml_simple(filepath: Path) -> dict:
    """Parse simple YAML without PyYAML."""
    if not filepath.exists():
        return {}

    result = {}
    try:
        content = filepath.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if ":" in line and not line.strip().startswith("#"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().strip('"').strip("'")
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    elif value.isdigit():
                        value = int(value)
                    result[key] = value
    except:
        pass
    return result

def parse_checkboxes(filepath: Path) -> tuple:
    """Parse checkboxes from markdown. Returns (done, total)."""
    if not filepath.exists():
        return 0, 0

    try:
        content = filepath.read_text(encoding="utf-8")
        checked = len(re.findall(r'- \[[xX]\]', content))
        unchecked = len(re.findall(r'- \[ \]', content))
        return checked, checked + unchecked
    except:
        return 0, 0

def get_sejr_info(sejr_path: Path) -> dict:
    """Get all info about a sejr including 3-PASS status."""
    status = parse_yaml_simple(sejr_path / "VERIFY_STATUS.yaml")
    done, total = parse_checkboxes(sejr_path / "SEJR_LISTE.md")

    completion = status.get("completion_percentage", 0)
    if isinstance(completion, str):
        try:
            completion = int(float(completion))
        except:
            completion = 0

    # Calculate from checkboxes if no status
    if completion == 0 and total > 0:
        completion = int((done / total) * 100)

    # 3-PASS info
    current_pass = status.get("current_pass", 1)
    pass_1_score = status.get("pass_1_score", 0)
    pass_2_score = status.get("pass_2_score", 0)
    pass_3_score = status.get("pass_3_score", 0)
    total_score = status.get("total_score", 0)
    can_archive = status.get("can_archive", False)

    return {
        "name": sejr_path.name,
        "path": sejr_path,
        "status": status.get("status", "unknown"),
        "completion": completion,
        "tasks_done": done,
        "tasks_total": total,
        "created": status.get("created", ""),
        "is_archived": False,
        "current_pass": current_pass,
        "pass_1_score": pass_1_score,
        "pass_2_score": pass_2_score,
        "pass_3_score": pass_3_score,
        "total_score": total_score,
        "can_archive": can_archive,
    }

def get_all_sejr() -> List[dict]:
    """Get all sejr (active and archived)."""
    sejr_list = []

    # Active sejr
    if ACTIVE_DIR.exists():
        for d in ACTIVE_DIR.iterdir():
            if d.is_dir() and (d / "SEJR_LISTE.md").exists():
                info = get_sejr_info(d)
                info["is_archived"] = False
                sejr_list.append(info)

    # Archived sejr
    if ARCHIVE_DIR.exists():
        for d in ARCHIVE_DIR.iterdir():
            if d.is_dir():
                info = {
                    "name": d.name,
                    "path": d,
                    "status": "archived",
                    "completion": 100,
                    "tasks_done": 0,
                    "tasks_total": 0,
                    "is_archived": True,
                }
                sejr_list.append(info)

    # Sort by name (newest first based on date in name)
    sejr_list.sort(key=lambda x: x["name"], reverse=True)
    return sejr_list

# ============================================================================
# STEAM-STYLE CARD WIDGET
# ============================================================================

class SejrCard(tk.Frame):
    """A Steam-style card representing a sejr."""

    def __init__(self, parent, sejr_info: dict, on_click=None, on_open=None):
        super().__init__(parent, bg=COLORS["card_bg"], cursor="hand2")

        self.sejr_info = sejr_info
        self.on_click = on_click
        self.on_open = on_open
        self.selected = False

        self.configure(
            highlightbackground=COLORS["bg_medium"],
            highlightthickness=2,
            padx=10,
            pady=10,
        )

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        info = self.sejr_info

        # Status icon (like game cover art area)
        icon_frame = tk.Frame(self, bg=self._get_status_color(), width=60, height=60)
        icon_frame.pack(side="left", padx=(0, 15))
        icon_frame.pack_propagate(False)

        # Status icon text
        icon_text = self._get_status_icon()
        tk.Label(
            icon_frame,
            text=icon_text,
            font=("Arial", 24),
            bg=self._get_status_color(),
            fg="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Info section
        info_frame = tk.Frame(self, bg=COLORS["card_bg"])
        info_frame.pack(side="left", fill="both", expand=True)

        # Title
        name_display = info["name"][:35] + "..." if len(info["name"]) > 35 else info["name"]
        tk.Label(
            info_frame,
            text=name_display,
            font=("Arial", 12, "bold"),
            fg=COLORS["text"],
            bg=COLORS["card_bg"],
            anchor="w"
        ).pack(fill="x")

        # Status text
        status_text = self._get_status_text()
        tk.Label(
            info_frame,
            text=status_text,
            font=("Arial", 9),
            fg=COLORS["text_dim"],
            bg=COLORS["card_bg"],
            anchor="w"
        ).pack(fill="x")

        # Progress bar
        if not info["is_archived"]:
            progress_frame = tk.Frame(info_frame, bg=COLORS["card_bg"], height=8)
            progress_frame.pack(fill="x", pady=(8, 0))

            # Background
            tk.Frame(
                progress_frame,
                bg=COLORS["bg_dark"],
                height=6
            ).place(relwidth=1.0, rely=0.5, anchor="w")

            # Fill
            completion = info["completion"] / 100
            color = COLORS["success"] if info["completion"] >= 100 else COLORS["accent"]
            tk.Frame(
                progress_frame,
                bg=color,
                height=6
            ).place(relwidth=completion, rely=0.5, anchor="w")

        # Right side - action buttons
        action_frame = tk.Frame(self, bg=COLORS["card_bg"])
        action_frame.pack(side="right", padx=10)

        if not info["is_archived"]:
            # Open button
            open_btn = tk.Button(
                action_frame,
                text="▶ ARBEJD",
                font=("Arial", 9, "bold"),
                bg=COLORS["success"],
                fg="white",
                activebackground=COLORS["accent"],
                activeforeground="white",
                relief="flat",
                padx=15,
                pady=5,
                cursor="hand2",
                command=lambda: self.on_open(info) if self.on_open else None
            )
            open_btn.pack()
        else:
            # View archive
            view_btn = tk.Button(
                action_frame,
                text="📁 SE",
                font=("Arial", 9),
                bg=COLORS["bg_medium"],
                fg=COLORS["text"],
                relief="flat",
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda: self.on_open(info) if self.on_open else None
            )
            view_btn.pack()

    def _get_status_color(self) -> str:
        info = self.sejr_info
        if info["is_archived"]:
            return COLORS["text_dim"]
        elif info["completion"] >= 100:
            return COLORS["success"]
        elif info["completion"] >= 50:
            return COLORS["warning"]
        else:
            return COLORS["accent"]

    def _get_status_icon(self) -> str:
        info = self.sejr_info
        if info["is_archived"]:
            return "📦"
        elif info["completion"] >= 100:
            return "✓"
        elif info["completion"] >= 50:
            return "◐"
        else:
            return "○"

    def _get_status_text(self) -> str:
        info = self.sejr_info
        if info["is_archived"]:
            return "Arkiveret"
        else:
            pass_info = f"Pass {info.get('current_pass', 1)}/3"
            score_info = f"Score: {info.get('total_score', 0)}/30"
            if info.get("can_archive", False):
                return f"✅ KLAR TIL ARKIV • {score_info}"
            else:
                return f"{pass_info} • {info['completion']}% • {score_info}"

    def _bind_events(self):
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

        for child in self.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.configure(bg=COLORS["card_hover"])
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=COLORS["card_hover"])
            elif isinstance(child, tk.Label):
                child.configure(bg=COLORS["card_hover"])

    def _on_leave(self, event):
        bg = COLORS["accent"] if self.selected else COLORS["card_bg"]
        self.configure(bg=bg)
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=bg)
            elif isinstance(child, tk.Label):
                child.configure(bg=bg)

    def _on_click(self, event):
        if self.on_click:
            self.on_click(self.sejr_info)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class SejrLauncher(tk.Tk):
    """Steam-style launcher for Sejrliste System."""

    def __init__(self):
        super().__init__()

        self.title("SEJR LAUNCHER")
        self.geometry("900x600")
        self.minsize(700, 400)
        self.configure(bg=COLORS["bg_dark"])

        # Set icon if available
        try:
            # Could add icon here
            pass
        except:
            pass

        self.current_filter = "all"  # all, active, archived
        self.sejr_list = []
        self.cards = []

        self._create_ui()
        self._refresh_sejr_list()

    def _create_ui(self):
        """Create the main UI."""

        # ===== TOP BAR =====
        top_bar = tk.Frame(self, bg=COLORS["bg_medium"], height=60)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        # Logo/Title
        tk.Label(
            top_bar,
            text="⚔️ SEJR LAUNCHER",
            font=("Arial", 18, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["bg_medium"]
        ).pack(side="left", padx=20, pady=15)

        # New Sejr button
        new_btn = tk.Button(
            top_bar,
            text="+ NY SEJR",
            font=("Arial", 11, "bold"),
            bg=COLORS["success"],
            fg="white",
            activebackground="#4a9020",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._create_new_sejr
        )
        new_btn.pack(side="right", padx=20, pady=12)

        # Refresh button
        refresh_btn = tk.Button(
            top_bar,
            text="↻",
            font=("Arial", 14),
            bg=COLORS["bg_dark"],
            fg=COLORS["text"],
            relief="flat",
            padx=10,
            cursor="hand2",
            command=self._refresh_sejr_list
        )
        refresh_btn.pack(side="right", pady=12)

        # ===== SIDEBAR =====
        sidebar = tk.Frame(self, bg=COLORS["bg_medium"], width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Sidebar title
        tk.Label(
            sidebar,
            text="BIBLIOTEK",
            font=("Arial", 10, "bold"),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_medium"]
        ).pack(pady=(20, 10), padx=15, anchor="w")

        # Filter buttons
        self.filter_buttons = {}
        filters = [
            ("all", "🏠 Alle"),
            ("active", "▶ Aktive"),
            ("archived", "📦 Arkiverede"),
        ]

        for filter_id, label in filters:
            btn = tk.Button(
                sidebar,
                text=label,
                font=("Arial", 11),
                bg=COLORS["bg_medium"],
                fg=COLORS["text"],
                activebackground=COLORS["accent"],
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=15,
                pady=8,
                cursor="hand2",
                command=lambda f=filter_id: self._set_filter(f)
            )
            btn.pack(fill="x", padx=5, pady=2)
            self.filter_buttons[filter_id] = btn

        # Separator
        tk.Frame(sidebar, bg=COLORS["bg_dark"], height=1).pack(fill="x", pady=20, padx=15)

        # Stats
        self.stats_label = tk.Label(
            sidebar,
            text="",
            font=("Arial", 9),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_medium"],
            justify="left"
        )
        self.stats_label.pack(padx=15, anchor="w")

        # Separator before tools
        tk.Frame(sidebar, bg=COLORS["bg_dark"], height=1).pack(fill="x", pady=10, padx=15)

        # Tools section
        tk.Label(
            sidebar,
            text="VÆRKTØJER",
            font=("Arial", 10, "bold"),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_medium"]
        ).pack(pady=(10, 5), padx=15, anchor="w")

        # Script buttons
        tool_buttons = [
            ("🔍 Verificer", self._run_verify, "Kør auto_verify.py"),
            ("📊 Opdater Status", self._run_track, "Kør auto_track.py"),
            ("🧠 Lær Patterns", self._run_learn, "Kør auto_learn.py"),
            ("🔮 Forudsig", self._run_predict, "Kør auto_predict.py"),
            ("📦 Arkiver", self._run_archive, "Kør auto_archive.py"),
        ]

        for text, command, tooltip in tool_buttons:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Arial", 9),
                bg=COLORS["bg_dark"],
                fg=COLORS["text"],
                activebackground=COLORS["accent"],
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=10,
                pady=5,
                cursor="hand2",
                command=command
            )
            btn.pack(fill="x", padx=10, pady=2)

        # Terminal output toggle
        tk.Frame(sidebar, bg=COLORS["bg_dark"], height=1).pack(fill="x", pady=10, padx=15)

        self.show_terminal = tk.BooleanVar(value=False)
        terminal_check = tk.Checkbutton(
            sidebar,
            text="Vis Terminal",
            variable=self.show_terminal,
            font=("Arial", 9),
            fg=COLORS["text"],
            bg=COLORS["bg_medium"],
            selectcolor=COLORS["bg_dark"],
            activebackground=COLORS["bg_medium"],
            command=self._toggle_terminal
        )
        terminal_check.pack(padx=15, anchor="w")

        # ===== MAIN CONTENT =====
        main_content = tk.Frame(self, bg=COLORS["bg_dark"])
        main_content.pack(side="left", fill="both", expand=True)

        # Content header
        self.content_header = tk.Label(
            main_content,
            text="ALLE SEJR",
            font=("Arial", 14, "bold"),
            fg=COLORS["text"],
            bg=COLORS["bg_dark"],
            anchor="w"
        )
        self.content_header.pack(fill="x", padx=20, pady=(20, 10))

        # Scrollable card container
        self.canvas = tk.Canvas(main_content, bg=COLORS["bg_dark"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(main_content, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["bg_dark"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20)
        self.scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # Update filter button state
        self._update_filter_buttons()

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def _set_filter(self, filter_id: str):
        """Set the current filter and refresh."""
        self.current_filter = filter_id
        self._update_filter_buttons()
        self._display_sejr_list()

        # Update header
        headers = {
            "all": "ALLE SEJR",
            "active": "AKTIVE SEJR",
            "archived": "ARKIVEREDE SEJR",
        }
        self.content_header.config(text=headers.get(filter_id, "SEJR"))

    def _update_filter_buttons(self):
        """Update filter button states."""
        for filter_id, btn in self.filter_buttons.items():
            if filter_id == self.current_filter:
                btn.configure(bg=COLORS["accent"], fg="white")
            else:
                btn.configure(bg=COLORS["bg_medium"], fg=COLORS["text"])

    def _refresh_sejr_list(self):
        """Refresh the sejr list from disk."""
        self.sejr_list = get_all_sejr()
        self._display_sejr_list()
        self._update_stats()

    def _update_stats(self):
        """Update sidebar stats."""
        active = sum(1 for s in self.sejr_list if not s["is_archived"])
        archived = sum(1 for s in self.sejr_list if s["is_archived"])

        stats_text = f"Aktive: {active}\nArkiverede: {archived}\nTotal: {len(self.sejr_list)}"
        self.stats_label.config(text=stats_text)

    def _display_sejr_list(self):
        """Display the sejr cards."""
        # Clear existing cards
        for card in self.cards:
            card.destroy()
        self.cards = []

        # Filter sejr
        filtered = []
        for sejr in self.sejr_list:
            if self.current_filter == "all":
                filtered.append(sejr)
            elif self.current_filter == "active" and not sejr["is_archived"]:
                filtered.append(sejr)
            elif self.current_filter == "archived" and sejr["is_archived"]:
                filtered.append(sejr)

        # Create cards
        if not filtered:
            empty_label = tk.Label(
                self.scrollable_frame,
                text="Ingen sejr fundet.\n\nKlik '+ NY SEJR' for at oprette en.",
                font=("Arial", 12),
                fg=COLORS["text_dim"],
                bg=COLORS["bg_dark"]
            )
            empty_label.pack(pady=50)
            self.cards.append(empty_label)
        else:
            for sejr in filtered:
                card = SejrCard(
                    self.scrollable_frame,
                    sejr,
                    on_click=self._on_card_click,
                    on_open=self._on_open_sejr
                )
                card.pack(fill="x", pady=5)
                self.cards.append(card)

    def _on_card_click(self, sejr_info: dict):
        """Handle card click."""
        # Could show details panel here
        pass

    def _on_open_sejr(self, sejr_info: dict):
        """Open a sejr for work."""
        path = sejr_info["path"]

        if sejr_info["is_archived"]:
            # Open archive folder
            self._open_folder(path)
        else:
            # Open SEJR_LISTE.md in default editor
            sejr_file = path / "SEJR_LISTE.md"
            if sejr_file.exists():
                self._open_file(sejr_file)
            else:
                messagebox.showerror("Fejl", f"SEJR_LISTE.md ikke fundet i:\n{path}")

    def _open_file(self, filepath: Path):
        """Open a file in default editor."""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", str(filepath)])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", str(filepath)], shell=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(filepath)])
        except Exception as e:
            messagebox.showerror("Fejl", f"Kunne ikke åbne fil:\n{e}")

    def _open_folder(self, folderpath: Path):
        """Open a folder in file manager."""
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", str(folderpath)])
            elif sys.platform == "win32":
                subprocess.run(["explorer", str(folderpath)])
            else:
                subprocess.run(["xdg-open", str(folderpath)])
        except Exception as e:
            messagebox.showerror("Fejl", f"Kunne ikke åbne mappe:\n{e}")

    def _toggle_terminal(self):
        """Toggle terminal output panel."""
        if self.show_terminal.get():
            self._show_terminal_panel()
        else:
            self._hide_terminal_panel()

    def _show_terminal_panel(self):
        """Show the terminal output panel."""
        if hasattr(self, 'terminal_frame') and self.terminal_frame.winfo_exists():
            return

        self.terminal_frame = tk.Frame(self, bg=COLORS["bg_dark"], height=150)
        self.terminal_frame.pack(side="bottom", fill="x")
        self.terminal_frame.pack_propagate(False)

        # Header
        header = tk.Frame(self.terminal_frame, bg=COLORS["bg_medium"])
        header.pack(fill="x")
        tk.Label(
            header,
            text="📟 TERMINAL OUTPUT",
            font=("Arial", 9, "bold"),
            fg=COLORS["text"],
            bg=COLORS["bg_medium"]
        ).pack(side="left", padx=10, pady=5)

        # Clear button
        tk.Button(
            header,
            text="Ryd",
            font=("Arial", 8),
            bg=COLORS["bg_dark"],
            fg=COLORS["text"],
            relief="flat",
            command=self._clear_terminal
        ).pack(side="right", padx=10, pady=3)

        # Text area
        self.terminal_text = tk.Text(
            self.terminal_frame,
            bg="#0d1117",
            fg="#58a6ff",
            font=("Courier", 9),
            height=8,
            wrap="word",
            state="disabled"
        )
        self.terminal_text.pack(fill="both", expand=True, padx=5, pady=5)

    def _hide_terminal_panel(self):
        """Hide the terminal output panel."""
        if hasattr(self, 'terminal_frame') and self.terminal_frame.winfo_exists():
            self.terminal_frame.destroy()

    def _clear_terminal(self):
        """Clear terminal output."""
        if hasattr(self, 'terminal_text'):
            self.terminal_text.config(state="normal")
            self.terminal_text.delete(1.0, tk.END)
            self.terminal_text.config(state="disabled")

    def _write_terminal(self, text: str):
        """Write text to terminal."""
        if not self.show_terminal.get():
            self.show_terminal.set(True)
            self._show_terminal_panel()

        if hasattr(self, 'terminal_text'):
            self.terminal_text.config(state="normal")
            self.terminal_text.insert(tk.END, text + "\n")
            self.terminal_text.see(tk.END)
            self.terminal_text.config(state="disabled")

    def _run_script(self, script_name: str, args: list = None):
        """Run a script and show output."""
        script = SCRIPTS_DIR / script_name
        if not script.exists():
            messagebox.showerror("Fejl", f"{script_name} ikke fundet!")
            return

        self._write_terminal(f"\n{'='*50}")
        self._write_terminal(f"▶ Kører: python {script_name} {' '.join(args or [])}")
        self._write_terminal(f"{'='*50}\n")

        try:
            cmd = [sys.executable, str(script)] + (args or [])
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(SYSTEM_PATH),
                timeout=60
            )

            if result.stdout:
                self._write_terminal(result.stdout)
            if result.stderr:
                self._write_terminal(f"[STDERR] {result.stderr}")

            if result.returncode == 0:
                self._write_terminal(f"\n✅ Færdig (exit code: 0)")
            else:
                self._write_terminal(f"\n❌ Fejl (exit code: {result.returncode})")

            # Refresh list after running script
            self._refresh_sejr_list()

        except subprocess.TimeoutExpired:
            self._write_terminal(f"\n⏱️ Timeout efter 60 sekunder")
        except Exception as e:
            self._write_terminal(f"\n❌ Fejl: {e}")

    def _run_verify(self):
        """Run auto_verify.py --all"""
        self._run_script("auto_verify.py", ["--all"])

    def _run_track(self):
        """Run auto_track.py"""
        self._run_script("auto_track.py")

    def _run_learn(self):
        """Run auto_learn.py"""
        self._run_script("auto_learn.py")

    def _run_predict(self):
        """Run auto_predict.py"""
        self._run_script("auto_predict.py")

    def _run_archive(self):
        """Run auto_archive.py --list to show what can be archived"""
        self._run_script("auto_archive.py", ["--list"])

    def _create_new_sejr(self):
        """Create a new sejr via dialog."""
        name = simpledialog.askstring(
            "Ny Sejr",
            "Indtast navn på ny sejr:\n\n(f.eks. 'Deploy Website', 'Fix Bug #123')",
            parent=self
        )

        if not name or not name.strip():
            return

        name = name.strip()

        # Run generate_sejr.py
        script = SCRIPTS_DIR / "generate_sejr.py"
        if not script.exists():
            messagebox.showerror("Fejl", "generate_sejr.py ikke fundet!")
            return

        try:
            result = subprocess.run(
                [sys.executable, str(script), "--name", name],
                capture_output=True,
                text=True,
                cwd=str(SYSTEM_PATH)
            )

            if result.returncode == 0:
                messagebox.showinfo("Succes", f"Sejr oprettet:\n{name}")
                self._refresh_sejr_list()
            else:
                messagebox.showerror("Fejl", f"Kunne ikke oprette sejr:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Fejl", f"Fejl ved oprettelse:\n{e}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the application."""
    app = SejrLauncher()
    app.mainloop()

if __name__ == "__main__":
    main()
