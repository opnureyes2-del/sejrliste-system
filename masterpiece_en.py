#!/usr/bin/env python3
"""
================================================================================
                    VICTORY LIST MASTERPIECE - GTK4 + LIBADWAITA
================================================================================

A modern, native GNOME application for the Victory List (Sejrliste) system.
Built with GTK4 and Libadwaita for a truly contemporary Linux desktop experience.

FEATURES:
---------
    * Native GTK4 + Libadwaita design (GNOME HIG compliant)
    * AdwNavigationSplitView - Modern sidebar navigation
    * AdwStatusPage - Beautiful empty/welcome states
    * 7 DNA Layers visualization - System self-awareness
    * Intelligent Search - Search across all files and content
    * Chat Stream - Messenger-style activity feed
    * Universal Converter - Convert any input to Victory structure
    * 5W Control - WHAT, WHERE, WHY, HOW, WHEN
    * Desktop Notifications - Native Linux notifications
    * Real-time updates - Auto-refresh from filesystem
    * Dark mode forced - Modern aesthetic

ARCHITECTURE:
-------------
    masterpiece_en.py
    |
    +-- VictoryListApp (Adw.Application)
    |   |
    |   +-- MainWindow (Adw.ApplicationWindow)
    |       |
    |       +-- AdwNavigationSplitView
    |       |   +-- Sidebar (Victory list with progress)
    |       |   +-- Content (Detail view / Welcome page)
    |       |
    |       +-- AdwHeaderBar (with actions)
    |
    +-- Classes:
        +-- IntelligentSearch - Search engine
        +-- VictoryConverter - Universal input converter
        +-- ChatMessage - Messenger-style message widget
        +-- ChatStream - Activity feed container
        +-- VictoryRow - Sidebar list item
        +-- DNALayerRow - DNA layer status display

KEYBOARD SHORTCUTS:
-------------------
    Ctrl+N  - New Victory
    Ctrl+O  - Open current folder
    Ctrl+F  - Search
    Ctrl+R  - Refresh
    Escape  - Close search

REQUIREMENTS:
-------------
    - Python 3.10+
    - PyGObject (gi)
    - GTK 4.0
    - Libadwaita 1

AUTHOR:
-------
    Kv1nt (Claude Opus 4.5) for Rasmus
    Date: 2026-01-25
    Version: 2.0 (English Complete Edition)

LICENSE:
--------
    Part of the Cirkelline ecosystem
================================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GLib, Gio, Pango, Gdk
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any
import re
import json
import subprocess
import shutil

# ==============================================================================
# CONSTANTS
# ==============================================================================

# System paths
SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
TEMPLATES_DIR = SYSTEM_PATH / "00_TEMPLATES"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"

# Application metadata
APP_ID = "dk.cirkelline.victorylist.masterpiece"
APP_NAME = "Victory List Masterpiece"
APP_VERSION = "2.0"

# DNA Layers configuration
DNA_LAYERS: List[Tuple[str, str, str, str]] = [
    ("1", "SELF-AWARE", "System knows itself", "emblem-system-symbolic"),
    ("2", "SELF-DOCUMENTING", "Auto-logs all actions", "document-edit-symbolic"),
    ("3", "SELF-VERIFYING", "Auto-verifies work", "emblem-ok-symbolic"),
    ("4", "SELF-IMPROVING", "Learns patterns", "view-refresh-symbolic"),
    ("5", "SELF-ARCHIVING", "Archives semantically", "folder-symbolic"),
    ("6", "PREDICTIVE", "Predicts next steps", "weather-clear-symbolic"),
    ("7", "SELF-OPTIMIZING", "Considers 3 alternatives", "applications-engineering-symbolic"),
]

# ==============================================================================
# MODERN CSS STYLING - 2026 DESIGN
# ==============================================================================

MODERN_CSS = """
/* =============================================================================
   VICTORY LIST MASTERPIECE - MODERN 2026 DESIGN
   Features: Gradients, Glassmorphism, Animations, Modern Typography
   ============================================================================= */

/* === GLOBAL COLORS === */
@define-color accent_gradient_start #6366f1;
@define-color accent_gradient_end #8b5cf6;
@define-color success_glow #22c55e;
@define-color warning_glow #f59e0b;
@define-color bg_dark #0f0f23;
@define-color bg_card rgba(30, 30, 60, 0.8);
@define-color text_primary #f8fafc;
@define-color text_secondary #94a3b8;

/* === WINDOW BASE === */
window.background {
    background: linear-gradient(180deg,
        #0f0f23 0%,
        #1a1a3e 50%,
        #0f0f23 100%);
}

/* === HEADERBAR - TRANSPARENT GLASSMORPHISM === */
headerbar {
    background: linear-gradient(90deg,
        rgba(99, 102, 241, 0.15) 0%,
        rgba(139, 92, 246, 0.15) 100%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

headerbar title {
    font-weight: 800;
    letter-spacing: 0.5px;
    background: linear-gradient(90deg, #f8fafc 0%, #c4b5fd 100%);
    -gtk-icon-filter: none;
}

/* === NAVIGATION SIDEBAR === */
.navigation-sidebar {
    background: rgba(15, 15, 35, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.navigation-sidebar row {
    margin: 4px 8px;
    padding: 12px 16px;
    border-radius: 12px;
    background: rgba(30, 30, 60, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 200ms ease-out;
}

.navigation-sidebar row:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateX(4px);
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
}

.navigation-sidebar row:selected {
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.4) 0%,
        rgba(139, 92, 246, 0.4) 100%);
    border-color: rgba(139, 92, 246, 0.5);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* === CARDS & PREFERENCE GROUPS === */
.card, preferencesgroup {
    background: rgba(30, 30, 60, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
    padding: 16px;
    margin: 8px 0;
}

/* === ACTION ROWS === */
row.activatable {
    border-radius: 12px;
    margin: 4px 0;
    padding: 8px 12px;
    transition: all 150ms ease-out;
}

row.activatable:hover {
    background: rgba(99, 102, 241, 0.1);
}

/* === PROGRESS BARS - GRADIENT GLOW === */
progressbar trough {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    min-height: 8px;
}

progressbar progress {
    background: linear-gradient(90deg,
        #6366f1 0%,
        #8b5cf6 50%,
        #a855f7 100%);
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
}

progressbar.success progress {
    background: linear-gradient(90deg,
        #22c55e 0%,
        #16a34a 100%);
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
}

progressbar.warning progress {
    background: linear-gradient(90deg,
        #f59e0b 0%,
        #d97706 100%);
    box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
}

/* === DNA LAYER BADGES === */
.heading {
    color: #f8fafc;
    font-weight: 700;
}

.caption {
    color: #94a3b8;
    font-size: 11px;
    letter-spacing: 0.3px;
}

.accent {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 50%;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
}

.success {
    color: #22c55e;
    text-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

.warning {
    color: #f59e0b;
    text-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
}

/* === BUTTONS - MODERN STYLE === */
button {
    border-radius: 10px;
    padding: 8px 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
    transition: all 150ms ease-out;
}

button:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
}

button.suggested-action {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border: none;
    color: white;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

button.suggested-action:hover {
    background: linear-gradient(135deg, #818cf8, #a78bfa);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
    transform: translateY(-2px);
}

button.pill {
    border-radius: 20px;
    padding: 10px 24px;
}

/* === SEARCH BAR === */
searchbar {
    background: rgba(15, 15, 35, 0.9);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

searchentry {
    background: rgba(30, 30, 60, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 10px 16px;
    color: #f8fafc;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

searchentry:focus {
    border-color: rgba(139, 92, 246, 0.6);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2),
                0 4px 15px rgba(0, 0, 0, 0.2);
}

/* === STATUS PAGE === */
statuspage {
    background: transparent;
}

statuspage .icon-dropshadow {
    color: #8b5cf6;
}

statuspage .title {
    font-size: 28px;
    font-weight: 800;
    color: #c4b5fd;
}

/* === SCROLLBAR - MINIMAL === */
scrollbar {
    background: transparent;
}

scrollbar slider {
    background: rgba(139, 92, 246, 0.3);
    border-radius: 4px;
    min-width: 6px;
}

scrollbar slider:hover {
    background: rgba(139, 92, 246, 0.5);
}

/* === SEPARATORS === */
separator {
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(139, 92, 246, 0.3) 50%,
        transparent 100%);
    min-height: 1px;
}

/* === TITLE STYLES === */
.title-1 {
    font-size: 28px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.5px;
}

.title-2 {
    font-size: 22px;
    font-weight: 700;
    color: #f8fafc;
}

.dim-label {
    color: #64748b;
}

/* === BOXED LIST === */
.boxed-list {
    background: rgba(30, 30, 60, 0.4);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.boxed-list row {
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.boxed-list row:last-child {
    border-bottom: none;
}

/* === GLOW EFFECTS === */
.glow-purple {
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
}

.glow-green {
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
}

.glow-amber {
    box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
}

/* === PRIORITY DASHBOARD - COMMAND CENTER === */
.priority-urgent {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(185, 28, 28, 0.15) 100%);
    border-left: 4px solid #ef4444;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}

.priority-attention {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(180, 83, 9, 0.15) 100%);
    border-left: 4px solid #f59e0b;
    box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
}

.priority-next {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(29, 78, 216, 0.15) 100%);
    border-left: 4px solid #3b82f6;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
}

.priority-card {
    border-radius: 12px;
    padding: 12px 16px;
    margin: 4px 0;
    transition: all 200ms ease-out;
}

.priority-card:hover {
    transform: translateX(8px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
}

/* === CHAT STREAM - MESSENGER STYLE === */
.chat-stream-messages {
    background: rgba(15, 15, 35, 0.6);
    padding: 8px;
}

.chat-bubble {
    background: rgba(30, 30, 60, 0.9);
    border-radius: 18px;
    padding: 10px 14px;
    max-width: 400px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.chat-bubble-system {
    border-radius: 4px 18px 18px 18px;
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.2) 0%,
        rgba(30, 30, 60, 0.9) 100%);
    border-left: 3px solid rgba(99, 102, 241, 0.6);
}

.chat-bubble-user {
    border-radius: 18px 18px 4px 18px;
    background: linear-gradient(135deg,
        rgba(139, 92, 246, 0.4) 0%,
        rgba(99, 102, 241, 0.3) 100%);
    border-right: 3px solid rgba(139, 92, 246, 0.8);
}

.chat-sender {
    font-weight: 700;
    font-size: 10px;
    color: #8b5cf6;
    letter-spacing: 0.5px;
}

.chat-timestamp {
    font-size: 9px;
    margin-top: 4px;
}

.chat-link {
    margin-top: 6px;
    padding: 4px 8px;
    border-radius: 8px;
    background: rgba(99, 102, 241, 0.2);
}

.chat-link:hover {
    background: rgba(99, 102, 241, 0.4);
}

.chat-verification {
    margin-top: 6px;
    padding: 4px 8px;
    border-radius: 8px;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.2);
}
"""


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def load_custom_css() -> None:
    """
    Load modern CSS styling into GTK.

    This function loads the MODERN_CSS stylesheet and applies it
    to the current GTK display with application priority.
    """
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(MODERN_CSS.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


def send_notification(title: str, body: str, icon: str = "emblem-ok-symbolic") -> None:
    """
    Send a desktop notification using notify-send.

    Args:
        title: The notification title
        body: The notification body text
        icon: Icon name (default: emblem-ok-symbolic)
    """
    try:
        subprocess.run([
            "notify-send",
            "-i", icon,
            "-a", APP_NAME,
            title,
            body
        ], check=False)
    except Exception:
        pass  # Silently fail if notify-send not available


def count_checkboxes(content: str) -> Tuple[int, int]:
    """
    Count checked and unchecked checkboxes in markdown content.

    Args:
        content: The markdown content to analyze

    Returns:
        Tuple of (checked_count, total_count)
    """
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked


def get_system_stats() -> Dict[str, int]:
    """
    Get overall system statistics.

    Returns:
        Dictionary with keys:
        - total_victories: Total number of victories
        - active: Number of active victories
        - archived: Number of archived victories
        - total_checkboxes: Total checkbox count
        - completed_checkboxes: Completed checkbox count
        - grand_admirals: Number of Grand Admiral victories (score >= 27)
    """
    stats = {
        "total_victories": 0,
        "active": 0,
        "archived": 0,
        "total_checkboxes": 0,
        "completed_checkboxes": 0,
        "grand_admirals": 0,
    }

    # Count active victories
    if ACTIVE_DIR.exists():
        for folder in ACTIVE_DIR.iterdir():
            if folder.is_dir() and not folder.name.startswith("."):
                stats["active"] += 1
                stats["total_victories"] += 1

                victory_file = folder / "SEJR_LISTE.md"
                if victory_file.exists():
                    done, total = count_checkboxes(victory_file.read_text())
                    stats["total_checkboxes"] += total
                    stats["completed_checkboxes"] += done

    # Count archived victories
    if ARCHIVE_DIR.exists():
        for folder in ARCHIVE_DIR.iterdir():
            if folder.is_dir() and not folder.name.startswith("."):
                stats["archived"] += 1
                stats["total_victories"] += 1

                # Check for Grand Admiral (score >= 27/30)
                conclusion = folder / "CONCLUSION.md"
                if conclusion.exists():
                    content = conclusion.read_text()
                    if any(x in content for x in ["GRAND ADMIRAL", "27/30", "28/30", "29/30", "30/30"]):
                        stats["grand_admirals"] += 1

    return stats


def get_victory_info(path: Path) -> Dict[str, Any]:
    """
    Get comprehensive information about a victory.

    Args:
        path: Path to the victory folder

    Returns:
        Dictionary containing victory metadata and status
    """
    victory_file = path / "SEJR_LISTE.md"

    info = {
        "name": path.name,
        "path": str(path),
        "display_name": path.name.split("_2026")[0].replace("_", " "),
        "progress": 0,
        "done": 0,
        "total": 0,
        "current_pass": "1",
        "is_archived": "90_ARCHIVE" in str(path),
        "files": [],
        "date": "Unknown",
    }

    # Extract date from folder name
    if "2026-01-" in path.name:
        try:
            date_part = path.name.split("2026-01-")[1][:2]
            info["date"] = f"Jan {date_part}, 2026"
        except (IndexError, ValueError):
            pass

    # Count checkboxes and calculate progress
    if victory_file.exists():
        content = victory_file.read_text()
        done, total = count_checkboxes(content)
        info["done"] = done
        info["total"] = total
        info["progress"] = int((done / total * 100) if total > 0 else 0)

        # Determine current pass
        content_upper = content.upper()
        if "PASS 3" in content_upper:
            info["current_pass"] = "3"
        elif "PASS 2" in content_upper:
            info["current_pass"] = "2"

    # List files
    if path.exists():
        info["files"] = [f.name for f in path.iterdir() if f.is_file()]

    return info


def get_all_victories() -> List[Dict[str, Any]]:
    """
    Get all victories sorted by modification time.

    Returns:
        List of victory info dictionaries, newest first
    """
    victories = []

    # Active victories
    if ACTIVE_DIR.exists():
        for folder in sorted(ACTIVE_DIR.iterdir(),
                           key=lambda x: x.stat().st_mtime,
                           reverse=True):
            if folder.is_dir() and not folder.name.startswith("."):
                victories.append(get_victory_info(folder))

    # Archived victories
    if ARCHIVE_DIR.exists():
        for folder in sorted(ARCHIVE_DIR.iterdir(),
                           key=lambda x: x.stat().st_mtime,
                           reverse=True):
            if folder.is_dir() and not folder.name.startswith("."):
                victories.append(get_victory_info(folder))

    return victories


# ==============================================================================
# INTELLIGENT SEARCH ENGINE
# ==============================================================================

class IntelligentSearch:
    """
    Intelligent search engine for the Victory List system.

    Searches across:
    - Folder names
    - File names
    - File contents (.md, .yaml, .txt, .py)
    - JSONL log entries
    - Checkbox status

    Attributes:
        system_path: Base path of the victory list system
        active_dir: Path to active victories
        archive_dir: Path to archived victories
    """

    def __init__(self, system_path: Path):
        """
        Initialize the search engine.

        Args:
            system_path: Base path of the victory list system
        """
        self.system_path = system_path
        self.active_dir = system_path / "10_ACTIVE"
        self.archive_dir = system_path / "90_ARCHIVE"

    def search(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search for query across all victory folders.

        Args:
            query: Search query (case-insensitive)
            max_results: Maximum number of results to return

        Returns:
            List of result dictionaries containing:
            - victory: Victory folder name
            - file: File name
            - line_num: Line number (0 for folder/filename matches)
            - context: Matching context text
            - match: The actual match
            - match_type: Type of match (folder, filename, content, log)
        """
        if not query or len(query) < 2:
            return []

        results = []
        query_lower = query.lower()

        # Search active victories
        if self.active_dir.exists():
            for victory_folder in self.active_dir.iterdir():
                if victory_folder.is_dir() and not victory_folder.name.startswith("."):
                    results.extend(self._search_victory(victory_folder, query_lower))

        # Search archived victories
        if self.archive_dir.exists():
            for victory_folder in self.archive_dir.iterdir():
                if victory_folder.is_dir() and not victory_folder.name.startswith("."):
                    results.extend(self._search_victory(victory_folder, query_lower))

        # Sort by relevance (exact matches first)
        results.sort(key=lambda x: (0 if query_lower in x["match"].lower() else 1, x["victory"]))

        return results[:max_results]

    def _search_victory(self, victory_folder: Path, query: str) -> List[Dict[str, Any]]:
        """Search within a single victory folder."""
        results = []

        # Search folder name
        if query in victory_folder.name.lower():
            results.append({
                "victory": victory_folder.name,
                "file": "(folder name)",
                "line_num": 0,
                "context": victory_folder.name,
                "match": victory_folder.name,
                "match_type": "folder"
            })

        # Search files
        for file_path in victory_folder.iterdir():
            if file_path.is_file():
                results.extend(self._search_file(file_path, victory_folder.name, query))

        return results

    def _search_file(self, file_path: Path, victory_name: str, query: str) -> List[Dict[str, Any]]:
        """Search within a single file."""
        results = []

        # Search filename
        if query in file_path.name.lower():
            results.append({
                "victory": victory_name,
                "file": file_path.name,
                "line_num": 0,
                "context": f"Filename: {file_path.name}",
                "match": file_path.name,
                "match_type": "filename"
            })

        # Search file contents
        try:
            if file_path.suffix in [".md", ".yaml", ".txt", ".py"]:
                content = file_path.read_text(errors="ignore")
                for i, line in enumerate(content.split("\n"), 1):
                    if query in line.lower():
                        context = line.strip()[:100]
                        if len(line.strip()) > 100:
                            context += "..."

                        results.append({
                            "victory": victory_name,
                            "file": file_path.name,
                            "line_num": i,
                            "context": context,
                            "match": self._extract_match(line, query),
                            "match_type": "content"
                        })

            elif file_path.suffix == ".jsonl":
                # Parse JSONL logs
                content = file_path.read_text(errors="ignore")
                for i, line in enumerate(content.split("\n"), 1):
                    if line.strip() and query in line.lower():
                        try:
                            data = json.loads(line)
                            context = f"{data.get('action', 'unknown')}: {data.get('detail', line[:50])}"
                        except json.JSONDecodeError:
                            context = line[:100]

                        results.append({
                            "victory": victory_name,
                            "file": file_path.name,
                            "line_num": i,
                            "context": context[:100],
                            "match": self._extract_match(line, query),
                            "match_type": "log"
                        })
        except Exception:
            pass  # Skip files that can't be read

        return results

    def _extract_match(self, line: str, query: str) -> str:
        """Extract the matching portion with context."""
        line_lower = line.lower()
        idx = line_lower.find(query)
        if idx == -1:
            return query

        start = max(0, idx - 10)
        end = min(len(line), idx + len(query) + 10)

        match = line[start:end]
        if start > 0:
            match = "..." + match
        if end < len(line):
            match = match + "..."

        return match


# ==============================================================================
# UNIVERSAL VICTORY CONVERTER
# ==============================================================================

class VictoryConverter:
    """
    Universal converter: Convert any input to Victory structure.

    Supports input types:
    - folder: Directory with files
    - file: Single file
    - pdf: PDF document
    - text: Plain text
    - command: Shell command

    Control modes:
    - manual: User controls everything
    - kv1nt: AI-assisted with suggestions
    - admiral: Fully automatic with verification

    5W Control:
    - WHAT: What is being converted
    - WHERE: Destination folder
    - WHY: Purpose of the victory
    - HOW: Approach/methodology
    - WHEN: Timeline and milestones
    """

    INPUT_TYPES = {
        "folder": "Folder",
        "file": "File",
        "pdf": "PDF",
        "text": "Text",
        "command": "Command",
    }

    CONTROL_MODES = {
        "manual": "Manual - You control everything",
        "kv1nt": "Kv1nt - AI-assisted with suggestions",
        "admiral": "Admiral - Fully automatic",
    }

    def __init__(self, system_path: Path):
        """
        Initialize the converter.

        Args:
            system_path: Base path of the victory list system
        """
        self.system_path = system_path
        self.active_dir = system_path / "10_ACTIVE"
        self.templates_dir = system_path / "00_TEMPLATES"

    def analyze_input(self, input_path: str, input_type: str) -> Dict[str, Any]:
        """
        Analyze input and suggest Victory structure.

        Args:
            input_path: Path to input or text content
            input_type: Type of input (folder, file, pdf, text, command)

        Returns:
            Analysis dictionary containing:
            - input_path: Original input path
            - input_type: Type of input
            - exists: Whether input exists
            - suggested_name: Suggested victory name
            - suggested_tasks: List of detected/suggested tasks
            - file_count: Number of files (for folders)
            - total_size: Total size in bytes
            - detected_sections: Detected sections (for markdown)
        """
        analysis = {
            "input_path": input_path,
            "input_type": input_type,
            "exists": False,
            "suggested_name": "",
            "suggested_tasks": [],
            "file_count": 0,
            "total_size": 0,
            "detected_sections": [],
        }

        path = Path(input_path)

        if input_type == "folder" and path.exists() and path.is_dir():
            analysis["exists"] = True
            analysis["suggested_name"] = path.name.upper().replace(" ", "_")
            files = list(path.rglob("*"))
            analysis["file_count"] = len([f for f in files if f.is_file()])
            analysis["total_size"] = sum(f.stat().st_size for f in files if f.is_file())

            # Suggest tasks based on files
            for f in files[:20]:
                if f.is_file():
                    analysis["suggested_tasks"].append(f"Process {f.name}")

        elif input_type == "file" and path.exists() and path.is_file():
            analysis["exists"] = True
            analysis["suggested_name"] = path.stem.upper().replace(" ", "_")
            analysis["file_count"] = 1
            analysis["total_size"] = path.stat().st_size

            # Detect sections in markdown
            if path.suffix in [".md", ".txt"]:
                try:
                    content = path.read_text()
                    for line in content.split("\n"):
                        if line.startswith("# ") or line.startswith("## "):
                            analysis["detected_sections"].append(line.strip("#").strip())
                except Exception:
                    pass

        elif input_type == "text":
            analysis["exists"] = True
            analysis["suggested_name"] = "TEXT_PROJECT"
            lines = input_path.split("\n")
            for line in lines:
                if line.strip():
                    analysis["suggested_tasks"].append(f"[ ] {line.strip()[:50]}")

        elif input_type == "command":
            analysis["exists"] = True
            analysis["suggested_name"] = "COMMAND_VICTORY"
            analysis["suggested_tasks"] = [
                "[ ] Execute command",
                "[ ] Verify output",
                "[ ] Document result",
            ]

        return analysis

    def create_victory_from_input(self, config: Dict[str, Any]) -> Path:
        """
        Create Victory structure from analyzed input.

        Args:
            config: Configuration dictionary containing:
                - name: Victory name
                - input_path: Source input path
                - input_type: Type of input
                - mode: Control mode
                - what: Description of what
                - where: Destination (auto-filled)
                - why: Purpose
                - how: Approach
                - when: Timeline
                - tasks: List of tasks

        Returns:
            Path to created victory folder
        """
        # Generate folder name with date
        date_str = datetime.now().strftime("%Y-%m-%d")
        folder_name = f"{config['name']}_{date_str}"
        victory_path = self.active_dir / folder_name

        # Create folder
        victory_path.mkdir(parents=True, exist_ok=True)

        # Generate VICTORY_LIST.md (SEJR_LISTE.md) content
        victory_content = self._generate_victory_markdown(config, victory_path)
        (victory_path / "SEJR_LISTE.md").write_text(victory_content)

        # Create CLAUDE.md focus lock
        claude_content = self._generate_claude_markdown(config)
        (victory_path / "CLAUDE.md").write_text(claude_content)

        # Create STATUS.yaml
        status_content = self._generate_status_yaml(config, victory_path)
        (victory_path / "STATUS.yaml").write_text(status_content)

        # Initialize AUTO_LOG.jsonl
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "victory_created",
            "source": config.get("input_type", "unknown"),
            "mode": config.get("mode", "manual"),
            "detail": f"Created from {config.get('input_path', 'N/A')}"
        }
        (victory_path / "AUTO_LOG.jsonl").write_text(json.dumps(log_entry) + "\n")

        return victory_path

    def _generate_victory_markdown(self, config: Dict[str, Any], victory_path: Path) -> str:
        """Generate the main victory list markdown content."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        content = f"""# VICTORY: {config['name']}

**Created:** {timestamp}
**Status:** PASS 1 - IN PROGRESS
**Owner:** Rasmus + Kv1nt
**Current Pass:** 1/3

**Source:** {config.get('input_type', 'unknown')} -> {config.get('input_path', 'N/A')}
**Mode:** {config.get('mode', 'manual')}

---

## 5W CONTROL

| Control | Value |
|---------|-------|
| **WHAT** | {config.get('what', 'Convert to victory structure')} |
| **WHERE** | {victory_path} |
| **WHY** | {config.get('why', 'Systematic execution')} |
| **HOW** | {config.get('how', '3-pass system')} |
| **WHEN** | {config.get('when', 'Now -> Complete')} |

---

## 3-PASS COMPETITION SYSTEM (MANDATORY)

```
PASS 1: WORKING       -> "Get it working"      -> REVIEW REQUIRED
PASS 2: IMPROVED      -> "Make it better"      -> REVIEW REQUIRED
PASS 3: OPTIMIZED     -> "Make it best"        -> FINAL VERIFICATION
                                                        |
                                               CAN BE ARCHIVED
```

---

# PASS 1: WORKING ("Get It Working")

## Tasks

"""
        # Add tasks
        for task in config.get("tasks", []):
            if not task.startswith("- [ ]"):
                task = f"- [ ] {task}"
            content += f"{task}\n"

        content += """
---

## Verification

- [ ] All tasks completed
- [ ] Output verified
- [ ] Ready for Pass 2

---

# PASS 2: IMPROVED ("Make It Better")

*To be filled after Pass 1 is complete*

---

# PASS 3: OPTIMIZED ("Make It Best")

*To be filled after Pass 2 is complete*
"""

        return content

    def _generate_claude_markdown(self, config: Dict[str, Any]) -> str:
        """Generate the CLAUDE.md focus lock content."""
        return f"""# CLAUDE FOCUS LOCK - READ THIS FIRST

> **YOU ARE IN A VICTORY LIST FOLDER. YOU HAVE ONE TASK. FOCUS.**

---

## CURRENT STATE

**Victory:** {config['name']}
**Current Pass:** 1/3
**Status:** Pass 1 - Working
**Input:** {config.get('input_type', 'unknown')}

---

## YOUR ONLY TASK RIGHT NOW

```
Read SEJR_LISTE.md and work on the first task
```

**NOTHING ELSE.** Complete this before doing anything else.
"""

    def _generate_status_yaml(self, config: Dict[str, Any], victory_path: Path) -> str:
        """Generate the STATUS.yaml content."""
        return f"""# VICTORY STATUS
name: {config['name']}
created: {datetime.now().isoformat()}
current_pass: 1
status: in_progress

input:
  type: {config.get('input_type', 'unknown')}
  path: {config.get('input_path', 'N/A')}

control:
  mode: {config.get('mode', 'manual')}
  what: {config.get('what', '')}
  where: {str(victory_path)}
  why: {config.get('why', '')}
  how: {config.get('how', '')}
  when: {config.get('when', '')}

passes:
  pass_1:
    status: in_progress
    score: 0
  pass_2:
    status: pending
    score: 0
  pass_3:
    status: pending
    score: 0
"""


# ==============================================================================
# CHAT STREAM WIDGETS - MESSENGER STYLE
# ==============================================================================

class ChatMessage(Gtk.Box):
    """
    A single chat message widget styled like Messenger.

    Messages are displayed with:
    - Avatar (emoji-based)
    - Sender name (for system messages)
    - Message content
    - Optional file link button
    - Optional verification status badge
    - Timestamp

    User messages appear on the right, system messages on the left.

    Attributes:
        file_link: Path to linked file (if any)
    """

    # Emoji avatars for different senders
    AVATARS = {
        "system": "🖥️",
        "kv1nt": "🤖",
        "admiral": "🎖️",
        "dna": "🧬",
        "verify": "✅",
        "error": "❌",
        "info": "💬",
    }

    def __init__(
        self,
        sender: str,
        content: str,
        timestamp: Optional[str] = None,
        msg_type: str = "info",
        file_link: Optional[str] = None,
        verification: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a chat message.

        Args:
            sender: Message sender name
            content: Message text content
            timestamp: Optional timestamp string (HH:MM format)
            msg_type: Message type for styling (info, error, etc.)
            file_link: Optional path to linked file
            verification: Optional dict with 'passed' (bool) and 'message' (str)
        """
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        self.file_link = file_link

        # Determine if user message (right aligned) or system (left aligned)
        is_user = sender.lower() in ["rasmus", "user", "you", "me"]

        if is_user:
            self.set_halign(Gtk.Align.END)
        else:
            self.set_halign(Gtk.Align.START)

        self.set_margin_start(12 if not is_user else 60)
        self.set_margin_end(12 if is_user else 60)
        self.set_margin_top(4)
        self.set_margin_bottom(4)

        # Avatar (only for system messages)
        if not is_user:
            avatar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            avatar_box.set_valign(Gtk.Align.START)

            emoji = self.AVATARS.get(sender.lower(), "💬")
            avatar_label = Gtk.Label()
            avatar_label.set_markup(f'<span size="large">{emoji}</span>')
            avatar_box.append(avatar_label)

            self.append(avatar_box)

        # Message bubble
        bubble = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        bubble.add_css_class("chat-bubble")
        bubble.add_css_class("chat-bubble-user" if is_user else "chat-bubble-system")

        # Sender name (only for system messages)
        if not is_user:
            sender_label = Gtk.Label(label=sender.upper())
            sender_label.set_halign(Gtk.Align.START)
            sender_label.add_css_class("caption")
            sender_label.add_css_class("chat-sender")
            bubble.append(sender_label)

        # Main content
        content_label = Gtk.Label(label=content)
        content_label.set_halign(Gtk.Align.START if not is_user else Gtk.Align.END)
        content_label.set_wrap(True)
        content_label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        content_label.set_max_width_chars(50)
        content_label.set_selectable(True)
        bubble.append(content_label)

        # File link button
        if file_link:
            link_btn = Gtk.Button()
            link_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            link_box.append(Gtk.Image.new_from_icon_name("document-open-symbolic"))
            link_box.append(Gtk.Label(label=Path(file_link).name))
            link_btn.set_child(link_box)
            link_btn.add_css_class("flat")
            link_btn.add_css_class("chat-link")
            link_btn.connect("clicked", self._on_file_clicked)
            bubble.append(link_btn)

        # Verification status badge
        if verification:
            verify_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            verify_box.add_css_class("chat-verification")

            status_icon = "emblem-ok-symbolic" if verification.get("passed") else "dialog-warning-symbolic"
            verify_box.append(Gtk.Image.new_from_icon_name(status_icon))

            verify_label = Gtk.Label(label=verification.get("message", "Verified"))
            verify_label.add_css_class("caption")
            verify_label.add_css_class("success" if verification.get("passed") else "warning")
            verify_box.append(verify_label)

            bubble.append(verify_box)

        # Timestamp
        if timestamp:
            time_label = Gtk.Label(label=timestamp)
            time_label.set_halign(Gtk.Align.END if is_user else Gtk.Align.START)
            time_label.add_css_class("caption")
            time_label.add_css_class("dim-label")
            time_label.add_css_class("chat-timestamp")
            bubble.append(time_label)

        self.append(bubble)

        # User avatar (on right side)
        if is_user:
            avatar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            avatar_box.set_valign(Gtk.Align.START)
            avatar_label = Gtk.Label()
            avatar_label.set_markup('<span size="large">👤</span>')
            avatar_box.append(avatar_label)
            self.append(avatar_box)

    def _on_file_clicked(self, button: Gtk.Button) -> None:
        """Open the linked file with default application."""
        if self.file_link:
            try:
                subprocess.Popen(["xdg-open", self.file_link])
            except Exception:
                pass


class ChatStream(Gtk.Box):
    """
    A scrollable chat stream showing activity like Messenger.

    Features:
    - Scrollable message container
    - Auto-scroll to bottom on new messages
    - Clear button to reset stream
    - Loads history from AUTO_LOG.jsonl

    Attributes:
        victory_path: Path to victory folder for log loading
        messages: List of ChatMessage widgets
        scroll_window: Scroll container reference
        message_box: Container for messages
    """

    def __init__(self, victory_path: Optional[Path] = None):
        """
        Initialize the chat stream.

        Args:
            victory_path: Optional path to victory folder for loading logs
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.victory_path = victory_path
        self.messages: List[ChatMessage] = []

        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header_box.set_margin_start(12)
        header_box.set_margin_end(12)
        header_box.set_margin_top(8)
        header_box.set_margin_bottom(8)

        chat_icon = Gtk.Image.new_from_icon_name("chat-symbolic")
        header_box.append(chat_icon)

        header_label = Gtk.Label(label="Activity Stream")
        header_label.add_css_class("heading")
        header_box.append(header_label)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        header_box.append(spacer)

        # Clear button
        clear_btn = Gtk.Button(icon_name="edit-clear-symbolic")
        clear_btn.add_css_class("flat")
        clear_btn.set_tooltip_text("Clear stream")
        clear_btn.connect("clicked", lambda b: self.clear_messages())
        header_box.append(clear_btn)

        self.append(header_box)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(sep)

        # Scrollable message area
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_min_content_height(200)

        self.message_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.message_box.add_css_class("chat-stream-messages")
        scroll.set_child(self.message_box)

        self.append(scroll)
        self.scroll_window = scroll

        # Load existing messages from log
        if victory_path:
            self._load_from_log(victory_path)

    def _load_from_log(self, victory_path: Path) -> None:
        """Load messages from AUTO_LOG.jsonl."""
        log_file = victory_path / "AUTO_LOG.jsonl"

        if not log_file.exists():
            # Add welcome message
            display_name = victory_path.name.split("_2026")[0].replace("_", " ")
            self.add_message(
                sender="Kv1nt",
                content=f"Welcome to {display_name}! I'm monitoring everything that happens here.",
                msg_type="info"
            )
            return

        try:
            content = log_file.read_text()
            for line in content.strip().split("\n")[-20:]:  # Last 20 entries
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)

                    # Determine sender based on action
                    action = data.get("action", "unknown")
                    if "verify" in action.lower():
                        sender = "Verify"
                    elif "dna" in action.lower():
                        sender = "DNA"
                    elif "user" in action.lower() or "rasmus" in action.lower():
                        sender = "Rasmus"
                    else:
                        sender = "System"

                    # Extract content
                    detail = data.get("detail", data.get("message", str(data)))
                    timestamp = data.get("timestamp", "")
                    if timestamp and len(timestamp) > 16:
                        timestamp = timestamp[11:16]  # Just HH:MM

                    # File link if present
                    file_link = data.get("file", data.get("path"))

                    # Verification if present
                    verification = None
                    if "verify" in action.lower() or "test" in action.lower():
                        verification = {
                            "passed": data.get("passed", data.get("success", True)),
                            "message": data.get("result", "Verified")
                        }

                    self.add_message(
                        sender=sender,
                        content=str(detail)[:200],
                        timestamp=timestamp,
                        file_link=file_link,
                        verification=verification
                    )
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            self.add_message(
                sender="System",
                content=f"Could not read log: {e}",
                msg_type="error"
            )

    def add_message(
        self,
        sender: str,
        content: str,
        timestamp: Optional[str] = None,
        msg_type: str = "info",
        file_link: Optional[str] = None,
        verification: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a new message to the stream.

        Args:
            sender: Message sender name
            content: Message text
            timestamp: Optional timestamp (defaults to current time)
            msg_type: Message type for styling
            file_link: Optional file path to link
            verification: Optional verification status dict
        """
        if not timestamp:
            timestamp = datetime.now().strftime("%H:%M")

        msg = ChatMessage(
            sender=sender,
            content=content,
            timestamp=timestamp,
            msg_type=msg_type,
            file_link=file_link,
            verification=verification
        )

        self.message_box.append(msg)
        self.messages.append(msg)

        # Auto-scroll to bottom
        GLib.idle_add(self._scroll_to_bottom)

    def _scroll_to_bottom(self) -> bool:
        """Scroll to the bottom of the chat."""
        adj = self.scroll_window.get_vadjustment()
        adj.set_value(adj.get_upper())
        return False

    def clear_messages(self) -> None:
        """Clear all messages from the stream."""
        while child := self.message_box.get_first_child():
            self.message_box.remove(child)
        self.messages = []

        # Add cleared message
        self.add_message(
            sender="System",
            content="Stream cleared",
            msg_type="info"
        )


# ==============================================================================
# CUSTOM WIDGETS
# ==============================================================================

class VictoryRow(Adw.ActionRow):
    """
    A row representing a victory in the sidebar.

    Displays:
    - Victory name
    - Current pass and date
    - Status icon (archived, near-complete, or active)
    - Progress percentage and bar

    Attributes:
        victory_info: Dictionary containing victory metadata
    """

    def __init__(self, victory_info: Dict[str, Any]):
        """
        Initialize a victory row.

        Args:
            victory_info: Dictionary from get_victory_info()
        """
        super().__init__()
        self.victory_info = victory_info

        self.set_title(victory_info["display_name"])
        self.set_subtitle(f"Pass {victory_info['current_pass']}/3 • {victory_info['date']}")

        # Status icon
        if victory_info["is_archived"]:
            icon = Gtk.Image.new_from_icon_name("emblem-ok-symbolic")
            icon.add_css_class("success")
        elif victory_info["progress"] >= 80:
            icon = Gtk.Image.new_from_icon_name("emblem-important-symbolic")
            icon.add_css_class("warning")
        else:
            icon = Gtk.Image.new_from_icon_name("folder-open-symbolic")

        self.add_prefix(icon)

        # Progress indicator
        progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        progress_box.set_valign(Gtk.Align.CENTER)

        progress_label = Gtk.Label(label=f"{victory_info['progress']}%")
        progress_label.add_css_class("caption")
        progress_box.append(progress_label)

        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(victory_info["progress"] / 100)
        progress_bar.set_size_request(60, 4)

        if victory_info["progress"] >= 80:
            progress_bar.add_css_class("success")
        elif victory_info["progress"] >= 50:
            progress_bar.add_css_class("warning")

        progress_box.append(progress_bar)
        self.add_suffix(progress_box)

        # Make activatable
        self.set_activatable(True)


class DNALayerRow(Gtk.Box):
    """
    A row showing a DNA layer status.

    Displays:
    - Status icon (active or loading)
    - Layer number badge
    - Layer icon
    - Name and description
    """

    def __init__(
        self,
        layer_num: str,
        name: str,
        description: str,
        icon_name: str,
        active: bool = False
    ):
        """
        Initialize a DNA layer row.

        Args:
            layer_num: Layer number (1-7)
            name: Layer name
            description: Layer description
            icon_name: GTK icon name
            active: Whether layer is currently active
        """
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(8)
        self.set_margin_bottom(8)

        # Status indicator
        status_icon = Gtk.Image.new_from_icon_name(
            "emblem-ok-symbolic" if active else "content-loading-symbolic"
        )
        status_icon.add_css_class("success" if active else "dim-label")
        self.append(status_icon)

        # Layer number badge
        badge = Gtk.Label(label=layer_num)
        badge.add_css_class("caption")
        badge.add_css_class("accent")
        badge.set_size_request(24, 24)
        self.append(badge)

        # Layer icon
        icon = Gtk.Image.new_from_icon_name(icon_name)
        self.append(icon)

        # Name and description
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        text_box.set_hexpand(True)

        name_label = Gtk.Label(label=name)
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("heading")
        text_box.append(name_label)

        desc_label = Gtk.Label(label=description)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.add_css_class("caption")
        desc_label.add_css_class("dim-label")
        text_box.append(desc_label)

        self.append(text_box)


class VictoryFileManager(Gtk.Box):
    """
    A comprehensive file manager widget for victory folders.

    Features:
    - Display all files and folders in victory directory
    - Import files/folders from external sources
    - Copy files into victory folder
    - Visual file type icons
    - Size and modification time display
    - Drag & drop support indication
    - Auto-refresh on file changes

    Attributes:
        victory_path: Path to the victory folder
        file_store: Gio.ListStore for file entries
    """

    def __init__(self, victory_path: Path):
        """
        Initialize the file manager.

        Args:
            victory_path: Path to the victory folder
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        self.victory_path = Path(victory_path)
        self.file_store = Gio.ListStore()

        self._build_ui()
        self._load_files()

    def _build_ui(self) -> None:
        """Build the file manager UI."""
        # Action bar
        action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        action_bar.set_margin_start(12)
        action_bar.set_margin_end(12)
        action_bar.set_margin_top(8)

        # Import button
        import_btn = Gtk.Button()
        import_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        import_box.append(Gtk.Image.new_from_icon_name("document-open-symbolic"))
        import_box.append(Gtk.Label(label="Import"))
        import_btn.set_child(import_box)
        import_btn.add_css_class("suggested-action")
        import_btn.connect("clicked", self._on_import_clicked)
        import_btn.set_tooltip_text("Import files or folders to this victory")
        action_bar.append(import_btn)

        # Refresh button
        refresh_btn = Gtk.Button(icon_name="view-refresh-symbolic")
        refresh_btn.connect("clicked", lambda b: self._load_files())
        refresh_btn.set_tooltip_text("Refresh file list")
        action_bar.append(refresh_btn)

        # Open folder button
        open_btn = Gtk.Button(icon_name="folder-open-symbolic")
        open_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", str(self.victory_path)]))
        open_btn.set_tooltip_text("Open in file manager")
        action_bar.append(open_btn)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        action_bar.append(spacer)

        # File count label
        self.file_count_label = Gtk.Label()
        self.file_count_label.add_css_class("dim-label")
        self.file_count_label.add_css_class("caption")
        action_bar.append(self.file_count_label)

        self.append(action_bar)

        # File list
        self.file_list = Gtk.ListBox()
        self.file_list.add_css_class("boxed-list")
        self.file_list.set_selection_mode(Gtk.SelectionMode.NONE)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(200)
        scroll.set_max_content_height(400)
        scroll.set_child(self.file_list)

        self.append(scroll)

        # Drop hint
        drop_hint = Gtk.Label(label="📂 Drag & drop files here or use Import button")
        drop_hint.add_css_class("caption")
        drop_hint.add_css_class("dim-label")
        drop_hint.set_margin_top(4)
        drop_hint.set_margin_bottom(8)
        self.append(drop_hint)

    def _load_files(self) -> None:
        """Load files and folders from victory directory."""
        # Clear existing
        while row := self.file_list.get_first_child():
            self.file_list.remove(row)

        if not self.victory_path.exists():
            return

        # Get all items (files and folders)
        items = []
        for item in self.victory_path.iterdir():
            if item.name.startswith('.'):
                continue  # Skip hidden files

            stat = item.stat()
            items.append({
                "name": item.name,
                "path": item,
                "is_dir": item.is_dir(),
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime),
            })

        # Sort: folders first, then by name
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))

        # Update count
        folder_count = sum(1 for i in items if i["is_dir"])
        file_count = len(items) - folder_count
        self.file_count_label.set_label(f"{folder_count} folders, {file_count} files")

        # Add items to list
        for item in items:
            row = self._create_file_row(item)
            self.file_list.append(row)

    def _create_file_row(self, item: Dict[str, Any]) -> Adw.ActionRow:
        """Create a row for a file or folder."""
        row = Adw.ActionRow()
        row.set_title(item["name"])

        # Icon based on type
        if item["is_dir"]:
            icon_name = "folder-symbolic"
            subtitle = "Folder"
        else:
            ext = item["path"].suffix.lower()
            icon_map = {
                ".md": ("text-x-markdown-symbolic", "Markdown"),
                ".yaml": ("text-x-script-symbolic", "YAML"),
                ".yml": ("text-x-script-symbolic", "YAML"),
                ".json": ("text-x-script-symbolic", "JSON"),
                ".jsonl": ("text-x-log-symbolic", "JSON Lines"),
                ".py": ("text-x-python-symbolic", "Python"),
                ".sh": ("text-x-script-symbolic", "Shell"),
                ".txt": ("text-x-generic-symbolic", "Text"),
                ".log": ("text-x-log-symbolic", "Log"),
                ".pdf": ("x-office-document-symbolic", "PDF"),
                ".png": ("image-x-generic-symbolic", "Image"),
                ".jpg": ("image-x-generic-symbolic", "Image"),
                ".jpeg": ("image-x-generic-symbolic", "Image"),
            }
            icon_name, file_type = icon_map.get(ext, ("text-x-generic-symbolic", "File"))
            size_str = self._format_size(item["size"])
            subtitle = f"{file_type} • {size_str}"

        row.add_prefix(Gtk.Image.new_from_icon_name(icon_name))
        row.set_subtitle(subtitle)

        # Time badge
        time_label = Gtk.Label(label=item["mtime"].strftime("%H:%M"))
        time_label.add_css_class("caption")
        time_label.add_css_class("dim-label")
        row.add_suffix(time_label)

        # Open button
        open_btn = Gtk.Button(icon_name="document-open-symbolic")
        open_btn.add_css_class("flat")
        open_btn.set_valign(Gtk.Align.CENTER)
        open_btn.connect("clicked", lambda b: subprocess.Popen(["xdg-open", str(item["path"])]))
        open_btn.set_tooltip_text("Open file")
        row.add_suffix(open_btn)

        # Make entire row clickable
        row.set_activatable(True)
        row.connect("activated", lambda r: subprocess.Popen(["xdg-open", str(item["path"])]))

        return row

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def _on_import_clicked(self, button: Gtk.Button) -> None:
        """Show file chooser dialog to import files."""
        dialog = Gtk.FileChooserDialog(
            title="Import Files to Victory",
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.set_transient_for(button.get_root())
        dialog.set_modal(True)
        dialog.set_select_multiple(True)

        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Import", Gtk.ResponseType.ACCEPT)

        dialog.connect("response", self._on_import_response)
        dialog.present()

    def _on_import_response(self, dialog: Gtk.FileChooserDialog, response: int) -> None:
        """Handle file chooser response."""
        if response == Gtk.ResponseType.ACCEPT:
            files = dialog.get_files()
            imported_count = 0

            for gfile in files:
                source_path = Path(gfile.get_path())
                dest_path = self.victory_path / source_path.name

                try:
                    if source_path.is_dir():
                        # Copy entire directory
                        shutil.copytree(source_path, dest_path)
                    else:
                        # Copy file
                        shutil.copy2(source_path, dest_path)
                    imported_count += 1
                except Exception as e:
                    print(f"Failed to import {source_path}: {e}")

            # Refresh file list
            self._load_files()

            # Send notification
            if imported_count > 0:
                send_notification(
                    "Files Imported",
                    f"Successfully imported {imported_count} item(s) to victory folder",
                    "emblem-ok-symbolic"
                )

        dialog.close()


class PriorityDashboard(Gtk.Box):
    """
    An intelligent priority dashboard that shows what needs attention NOW.

    Features:
    - URGENT: Critical items requiring immediate action (red glow)
    - ATTENTION: Items that should be addressed soon (amber glow)
    - NEXT: AI-predicted next steps (blue glow)
    - ONE-CLICK: Direct navigation to problem areas
    - LIVE: Auto-updates every 5 seconds

    This is the FIRST thing the user sees - it guides them directly
    to where they need to be.
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_start(24)
        self.set_margin_end(24)
        self.set_margin_top(16)
        self.set_margin_bottom(16)

        self._build_ui()
        self._update_priorities()

        # Auto-refresh every 5 seconds
        GLib.timeout_add_seconds(5, self._update_priorities)

    def _build_ui(self) -> None:
        """Build the priority dashboard UI."""
        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        icon = Gtk.Image.new_from_icon_name("dialog-warning-symbolic")
        icon.set_pixel_size(32)
        icon.add_css_class("warning")
        header.append(icon)

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        title = Gtk.Label(label="⚡ Priority Dashboard")
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-2")
        title_box.append(title)

        subtitle = Gtk.Label(label="What needs your attention RIGHT NOW")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("dim-label")
        subtitle.add_css_class("caption")
        title_box.append(subtitle)

        header.append(title_box)
        self.append(header)

        # Priority sections container
        self.sections_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.append(self.sections_box)

    def _update_priorities(self) -> bool:
        """Update priority items from current system state."""
        # Clear existing
        while child := self.sections_box.get_first_child():
            self.sections_box.remove(child)

        priorities = self._analyze_system()

        if not any(priorities.values()):
            # All clear!
            clear_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            clear_box.set_halign(Gtk.Align.CENTER)
            clear_box.add_css_class("card")
            clear_box.set_margin_top(16)
            clear_box.set_margin_bottom(16)

            icon = Gtk.Image.new_from_icon_name("emblem-ok-symbolic")
            icon.set_pixel_size(48)
            icon.add_css_class("success")
            clear_box.append(icon)

            label = Gtk.Label(label="✨ All Clear!")
            label.add_css_class("title-3")
            clear_box.append(label)

            desc = Gtk.Label(label="No urgent items. You're on track!")
            desc.add_css_class("dim-label")
            clear_box.append(desc)

            self.sections_box.append(clear_box)
        else:
            # Build priority sections
            if priorities["urgent"]:
                self._add_section("🔴 URGENT", priorities["urgent"], "error")
            if priorities["attention"]:
                self._add_section("🟡 ATTENTION", priorities["attention"], "warning")
            if priorities["next"]:
                self._add_section("🔵 NEXT STEPS", priorities["next"], "accent")

        return True  # Continue timeout

    def _analyze_system(self) -> Dict[str, List[Dict]]:
        """Analyze system state and return priority items."""
        priorities = {"urgent": [], "attention": [], "next": []}

        # Check for incomplete active victories
        if ACTIVE_DIR.exists():
            for victory_dir in ACTIVE_DIR.iterdir():
                if not victory_dir.is_dir():
                    continue

                sejr_file = victory_dir / "SEJR_LISTE.md"
                if sejr_file.exists():
                    content = sejr_file.read_text()
                    done, total = count_checkboxes(content)

                    if total > 0:
                        progress = (done / total) * 100

                        if progress < 30:
                            priorities["urgent"].append({
                                "title": f"Victory stalled: {victory_dir.name}",
                                "subtitle": f"Only {progress:.0f}% complete ({done}/{total})",
                                "action": "Open Victory",
                                "path": str(victory_dir),
                                "icon": "emblem-important-symbolic"
                            })
                        elif progress < 80:
                            priorities["attention"].append({
                                "title": f"Continue: {victory_dir.name}",
                                "subtitle": f"{progress:.0f}% complete - push to finish!",
                                "action": "Resume",
                                "path": str(victory_dir),
                                "icon": "media-playback-start-symbolic"
                            })

        # Check for missing verification
        if ACTIVE_DIR.exists():
            for victory_dir in ACTIVE_DIR.iterdir():
                if not victory_dir.is_dir():
                    continue

                verify_file = victory_dir / "VERIFY_STATUS.yaml"
                if not verify_file.exists():
                    priorities["attention"].append({
                        "title": f"Missing verification: {victory_dir.name}",
                        "subtitle": "Run verification to track progress",
                        "action": "Verify Now",
                        "path": str(victory_dir),
                        "icon": "emblem-ok-symbolic"
                    })

        # Check NEXT.md for predictions
        next_file = SYSTEM_PATH / "_CURRENT" / "NEXT.md"
        if next_file.exists():
            content = next_file.read_text()
            lines = [l.strip() for l in content.split('\n') if l.strip().startswith('- ')]
            for line in lines[:3]:
                priorities["next"].append({
                    "title": line[2:50] + "..." if len(line) > 52 else line[2:],
                    "subtitle": "AI predicted next action",
                    "action": "View Details",
                    "path": str(next_file),
                    "icon": "weather-clear-symbolic"
                })

        # If no next steps, suggest creating new victory
        if not priorities["next"] and not priorities["urgent"]:
            priorities["next"].append({
                "title": "Create a new victory",
                "subtitle": "Start fresh with a new goal",
                "action": "New Victory",
                "path": "new",
                "icon": "list-add-symbolic"
            })

        return priorities

    def _add_section(self, title: str, items: List[Dict], css_class: str) -> None:
        """Add a priority section with items."""
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        # Section header
        header = Gtk.Label(label=title)
        header.set_halign(Gtk.Align.START)
        header.add_css_class("heading")
        header.add_css_class(css_class)
        section.append(header)

        # Items
        for item in items[:3]:  # Max 3 per section
            row = self._create_priority_row(item, css_class)
            section.append(row)

        self.sections_box.append(section)

    def _create_priority_row(self, item: Dict, css_class: str) -> Gtk.Box:
        """Create a clickable priority row."""
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.add_css_class("card")
        row.set_margin_start(8)
        row.set_margin_end(8)

        # Icon
        icon = Gtk.Image.new_from_icon_name(item.get("icon", "dialog-information-symbolic"))
        icon.set_pixel_size(24)
        icon.add_css_class(css_class)
        row.append(icon)

        # Text
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        text_box.set_hexpand(True)

        title = Gtk.Label(label=item["title"])
        title.set_halign(Gtk.Align.START)
        title.add_css_class("heading")
        title.set_ellipsize(Pango.EllipsizeMode.END)
        text_box.append(title)

        subtitle = Gtk.Label(label=item["subtitle"])
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("caption")
        subtitle.add_css_class("dim-label")
        text_box.append(subtitle)

        row.append(text_box)

        # Action button
        btn = Gtk.Button(label=item["action"])
        btn.add_css_class("suggested-action")
        btn.add_css_class("pill")
        btn.set_valign(Gtk.Align.CENTER)

        path = item["path"]
        if path == "new":
            btn.connect("clicked", lambda b: self._create_new_victory())
        else:
            btn.connect("clicked", lambda b, p=path: subprocess.Popen(["nautilus", p]))

        row.append(btn)

        return row

    def _create_new_victory(self) -> None:
        """Trigger new victory creation."""
        script = SCRIPTS_DIR / "generate_sejr.py"
        if script.exists():
            subprocess.Popen(["python3", str(script)])
            send_notification("New Victory", "Creating new victory...", "list-add-symbolic")


# ==============================================================================
# MAIN WINDOW
# ==============================================================================

class MainWindow(Adw.ApplicationWindow):
    """
    The main application window.

    Contains:
    - Header bar with actions (refresh, new, convert, search, menu)
    - Navigation split view (sidebar + content)
    - Sidebar with victory list and stats
    - Content area (welcome page or victory detail)
    - Search functionality

    Attributes:
        selected_victory: Currently selected victory info
        victories: List of all victories
        search_engine: IntelligentSearch instance
        search_mode: Whether search is active
        chat_stream: Current ChatStream instance (if viewing victory)
    """

    def __init__(self, app: Adw.Application):
        """
        Initialize the main window.

        Args:
            app: The parent application
        """
        super().__init__(application=app)

        self.set_title(APP_NAME)
        self.set_default_size(1200, 800)

        self.selected_victory: Optional[Dict[str, Any]] = None
        self.victories: List[Dict[str, Any]] = []
        self.search_engine = IntelligentSearch(SYSTEM_PATH)
        self.search_mode = False
        self.chat_stream: Optional[ChatStream] = None

        self._build_ui()
        self._load_victories()

        # Auto-refresh every 5 seconds
        GLib.timeout_add_seconds(5, self._auto_refresh)

    def _build_ui(self) -> None:
        """Build the complete user interface."""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        # Header bar
        header = self._build_header()
        main_box.append(header)

        # Navigation split view
        self.split_view = Adw.NavigationSplitView()
        self.split_view.set_vexpand(True)
        main_box.append(self.split_view)

        # Build sidebar and content
        self._build_sidebar()
        self._build_content()

    def _build_header(self) -> Adw.HeaderBar:
        """Build the header bar with all actions."""
        header = Adw.HeaderBar()

        # Title widget
        title_widget = Adw.WindowTitle()
        title_widget.set_title("Victory List")
        title_widget.set_subtitle("Masterpiece Edition")
        header.set_title_widget(title_widget)

        # Left side buttons
        refresh_btn = Gtk.Button(icon_name="view-refresh-symbolic")
        refresh_btn.set_tooltip_text("Refresh (Ctrl+R)")
        refresh_btn.connect("clicked", lambda b: self._load_victories())
        header.pack_start(refresh_btn)

        new_btn = Gtk.Button(icon_name="list-add-symbolic")
        new_btn.set_tooltip_text("New Victory (Ctrl+N)")
        new_btn.add_css_class("suggested-action")
        new_btn.connect("clicked", self._on_new_victory)
        header.pack_start(new_btn)

        convert_btn = Gtk.Button(icon_name="document-import-symbolic")
        convert_btn.set_tooltip_text("Convert to Victory (from folder/file/text)")
        convert_btn.connect("clicked", self._on_convert_to_victory)
        header.pack_start(convert_btn)

        # Right side buttons
        self.search_btn = Gtk.ToggleButton(icon_name="system-search-symbolic")
        self.search_btn.set_tooltip_text("Intelligent Search (Ctrl+F)")
        self.search_btn.connect("toggled", self._on_search_toggled)
        header.pack_end(self.search_btn)

        menu_btn = Gtk.MenuButton(icon_name="open-menu-symbolic")
        header.pack_end(menu_btn)

        return header

    def _build_sidebar(self) -> None:
        """Build the sidebar with victory list."""
        sidebar_page = Adw.NavigationPage()
        sidebar_page.set_title("Library")

        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Sidebar header
        sidebar_header = Adw.HeaderBar()
        sidebar_header.add_css_class("flat")
        sidebar_box.append(sidebar_header)

        # Search bar
        self.search_bar = Gtk.SearchBar()
        self.search_bar.set_show_close_button(True)

        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        search_box.set_margin_start(6)
        search_box.set_margin_end(6)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search files, code, details...")
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self._on_search_changed)
        self.search_entry.connect("activate", self._on_search_activate)
        search_box.append(self.search_entry)

        self.search_bar.set_child(search_box)
        self.search_bar.connect_entry(self.search_entry)
        sidebar_box.append(self.search_bar)

        # Search results container
        self.search_results_scroll = Gtk.ScrolledWindow()
        self.search_results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.search_results_scroll.set_vexpand(True)
        self.search_results_scroll.set_visible(False)

        self.search_results_list = Gtk.ListBox()
        self.search_results_list.add_css_class("boxed-list")
        self.search_results_list.connect("row-activated", self._on_search_result_activated)
        self.search_results_scroll.set_child(self.search_results_list)
        sidebar_box.append(self.search_results_scroll)

        # Victory list
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)

        self.victory_list = Gtk.ListBox()
        self.victory_list.add_css_class("navigation-sidebar")
        self.victory_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.victory_list.connect("row-activated", self._on_victory_selected)
        scroll.set_child(self.victory_list)

        sidebar_box.append(scroll)

        # Stats at bottom
        self.stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.stats_box.set_margin_start(12)
        self.stats_box.set_margin_end(12)
        self.stats_box.set_margin_top(12)
        self.stats_box.set_margin_bottom(12)
        self.stats_box.set_halign(Gtk.Align.CENTER)

        self.active_label = Gtk.Label(label="0 Active")
        self.active_label.add_css_class("caption")
        self.stats_box.append(self.active_label)

        sep = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.stats_box.append(sep)

        self.archived_label = Gtk.Label(label="0 Archived")
        self.archived_label.add_css_class("caption")
        self.stats_box.append(self.archived_label)

        sidebar_box.append(self.stats_box)

        sidebar_page.set_child(sidebar_box)
        self.split_view.set_sidebar(sidebar_page)

    def _build_content(self) -> None:
        """Build the content area."""
        content_page = Adw.NavigationPage()
        content_page.set_title("Details")

        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        # Welcome page
        welcome = self._build_welcome_page()
        self.content_stack.add_named(welcome, "welcome")

        # Detail page
        self.detail_scroll = Gtk.ScrolledWindow()
        self.detail_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.detail_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        self.detail_box.set_margin_start(24)
        self.detail_box.set_margin_end(24)
        self.detail_box.set_margin_top(24)
        self.detail_box.set_margin_bottom(24)
        self.detail_scroll.set_child(self.detail_box)

        self.content_stack.add_named(self.detail_scroll, "detail")

        content_page.set_child(self.content_stack)
        self.split_view.set_content(content_page)

        self.content_stack.set_visible_child_name("welcome")

    def _build_welcome_page(self) -> Gtk.Box:
        """Build the welcome/empty state page with priority dashboard and live stats."""
        # Scrollable container for the whole page
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        main_box.set_margin_top(24)
        main_box.set_margin_bottom(48)

        # ⚡ PRIORITY DASHBOARD - FIRST THING USER SEES
        # Shows what needs attention RIGHT NOW
        self.priority_dashboard = PriorityDashboard()
        main_box.append(self.priority_dashboard)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_start(24)
        sep.set_margin_end(24)
        main_box.append(sep)

        # Header (moved below priority dashboard)
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        header_box.set_halign(Gtk.Align.CENTER)

        icon = Gtk.Image.new_from_icon_name("starred-symbolic")
        icon.set_pixel_size(64)
        icon.add_css_class("accent")
        header_box.append(icon)

        title = Gtk.Label(label="Victory List Masterpiece")
        title.add_css_class("title-1")
        header_box.append(title)

        subtitle = Gtk.Label(label="Your path to Admiral level")
        subtitle.add_css_class("dim-label")
        header_box.append(subtitle)

        main_box.append(header_box)

        # Stats cards
        stats = get_system_stats()
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        stats_box.set_halign(Gtk.Align.CENTER)

        stat_items = [
            ("🎯", str(stats["total_victories"]), "Total Victories"),
            ("✅", str(stats["archived"]), "Archived"),
            ("🏅", str(stats["grand_admirals"]), "Grand Admirals"),
            ("📊", f"{stats['completed_checkboxes']}/{stats['total_checkboxes']}", "Checkboxes"),
        ]

        for emoji, value, label in stat_items:
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            card.add_css_class("card")
            card.set_size_request(100, 80)

            emoji_label = Gtk.Label()
            emoji_label.set_markup(f'<span size="x-large">{emoji}</span>')
            card.append(emoji_label)

            value_label = Gtk.Label(label=value)
            value_label.add_css_class("title-2")
            card.append(value_label)

            desc_label = Gtk.Label(label=label)
            desc_label.add_css_class("caption")
            desc_label.add_css_class("dim-label")
            card.append(desc_label)

            stats_box.append(card)

        main_box.append(stats_box)

        # Admiral Rate progress
        if stats["total_victories"] > 0:
            progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            progress_box.set_halign(Gtk.Align.CENTER)

            admiral_pct = (stats["grand_admirals"] / max(stats["archived"], 1)) * 100
            progress_label = Gtk.Label(label=f"Admiral Rate: {admiral_pct:.0f}%")
            progress_label.add_css_class("caption")
            progress_box.append(progress_label)

            progress = Gtk.ProgressBar()
            progress.set_fraction(admiral_pct / 100)
            progress.set_size_request(300, -1)
            if admiral_pct >= 80:
                progress.add_css_class("success")
            progress_box.append(progress)

            main_box.append(progress_box)

        # Action buttons
        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        buttons_box.set_halign(Gtk.Align.CENTER)

        new_btn = Gtk.Button(label="🚀 Create New Victory")
        new_btn.add_css_class("suggested-action")
        new_btn.add_css_class("pill")
        new_btn.connect("clicked", self._on_new_victory)
        buttons_box.append(new_btn)

        open_btn = Gtk.Button(label="📁 Open Folder")
        open_btn.add_css_class("pill")
        open_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", str(SYSTEM_PATH)]))
        buttons_box.append(open_btn)

        main_box.append(buttons_box)

        # Tip
        tip_label = Gtk.Label(label="💡 Tip: Use Ctrl+N for quick new victory")
        tip_label.add_css_class("caption")
        tip_label.add_css_class("dim-label")
        main_box.append(tip_label)

        scroll.set_child(main_box)
        return scroll

    def _build_detail_page(self, victory: Dict[str, Any]) -> None:
        """Build the detail view for a victory."""
        # Clear existing content
        while child := self.detail_box.get_first_child():
            self.detail_box.remove(child)

        # Header with title
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        icon = Gtk.Image.new_from_icon_name(
            "emblem-ok-symbolic" if victory["is_archived"] else "folder-open-symbolic"
        )
        icon.set_pixel_size(48)
        if victory["is_archived"]:
            icon.add_css_class("success")
        header_box.append(icon)

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title_box.set_hexpand(True)

        title = Gtk.Label(label=victory["display_name"])
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-1")
        title_box.append(title)

        subtitle = Gtk.Label(label=f"Pass {victory['current_pass']}/3 • {victory['date']}")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("dim-label")
        title_box.append(subtitle)

        header_box.append(title_box)

        # Open folder button
        open_btn = Gtk.Button(icon_name="folder-open-symbolic")
        open_btn.set_tooltip_text("Open in Files")
        open_btn.set_valign(Gtk.Align.CENTER)
        open_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", victory["path"]]))
        header_box.append(open_btn)

        self.detail_box.append(header_box)

        # Progress section
        progress_group = Adw.PreferencesGroup()
        progress_group.set_title("Progress")

        # Main progress bar
        progress_row = Adw.ActionRow()
        progress_row.set_title(f"Overall Progress: {victory['progress']}%")
        progress_row.set_subtitle(f"{victory['done']}/{victory['total']} checkboxes completed")

        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(victory["progress"] / 100)
        progress_bar.set_valign(Gtk.Align.CENTER)
        progress_bar.set_size_request(200, -1)
        if victory["progress"] >= 80:
            progress_bar.add_css_class("success")
        progress_row.add_suffix(progress_bar)
        progress_group.add(progress_row)

        # 3-Pass status
        passes_row = Adw.ActionRow()
        passes_row.set_title("3-Pass System")

        passes_box = Gtk.Box(spacing=6)
        passes_box.set_valign(Gtk.Align.CENTER)
        for i in range(1, 4):
            badge = Gtk.Label(label=str(i))
            badge.add_css_class("caption")
            badge.add_css_class("success" if i <= int(victory["current_pass"]) else "dim-label")
            badge.set_size_request(24, 24)
            passes_box.append(badge)

        passes_row.add_suffix(passes_box)
        progress_group.add(passes_row)

        self.detail_box.append(progress_group)

        # DNA Layers section
        dna_group = Adw.PreferencesGroup()
        dna_group.set_title("7 DNA Layers")
        dna_group.set_description("System self-awareness and automation")

        dna_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        dna_box.add_css_class("card")

        for i, (num, name, desc, icon_name) in enumerate(DNA_LAYERS):
            active = victory["progress"] > (i * 12)
            row = DNALayerRow(num, name, desc, icon_name, active)
            dna_box.append(row)

            if i < len(DNA_LAYERS) - 1:
                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                dna_box.append(sep)

        dna_group.add(dna_box)
        self.detail_box.append(dna_group)

        # Quick Actions
        quick_group = Adw.PreferencesGroup()
        quick_group.set_title("Quick Navigation")

        quick_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        quick_box.set_halign(Gtk.Align.START)
        quick_box.set_margin_top(8)
        quick_box.set_margin_bottom(8)

        # Open folder
        folder_btn = Gtk.Button(label="📁 Open Folder")
        folder_btn.add_css_class("pill")
        folder_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", victory["path"]]))
        quick_box.append(folder_btn)

        # Edit victory file
        victory_file = Path(victory["path"]) / "SEJR_LISTE.md"
        if victory_file.exists():
            edit_btn = Gtk.Button(label="📝 Edit Victory")
            edit_btn.add_css_class("pill")
            edit_btn.connect("clicked", lambda b: subprocess.Popen(["xdg-open", str(victory_file)]))
            quick_box.append(edit_btn)

        # Open terminal
        term_btn = Gtk.Button(label="💻 Terminal")
        term_btn.add_css_class("pill")
        term_btn.connect("clicked", lambda b: subprocess.Popen(
            ["gnome-terminal", f"--working-directory={victory['path']}"]
        ))
        quick_box.append(term_btn)

        quick_group.add(quick_box)
        self.detail_box.append(quick_group)

        # Files section - Full file manager with import/copy
        files_group = Adw.PreferencesGroup()
        files_group.set_title("📁 Files & Folders")
        files_group.set_description("Import, copy, and manage files in this victory")

        # Use the full VictoryFileManager widget
        self.file_manager = VictoryFileManager(Path(victory["path"]))
        files_group.add(self.file_manager)

        self.detail_box.append(files_group)

        # DNA Actions
        actions_group = Adw.PreferencesGroup()
        actions_group.set_title("DNA Actions")

        actions = [
            ("Verify", "emblem-ok-symbolic", "auto_verify.py"),
            ("Learn", "view-refresh-symbolic", "auto_learn.py"),
            ("Predict", "weather-clear-symbolic", "auto_predict.py"),
            ("Archive", "folder-symbolic", "auto_archive.py"),
        ]

        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        actions_box.set_halign(Gtk.Align.CENTER)
        actions_box.set_margin_top(12)
        actions_box.set_margin_bottom(12)

        for label, icon, script in actions:
            btn = Gtk.Button()
            btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            btn_box.append(Gtk.Image.new_from_icon_name(icon))
            btn_box.append(Gtk.Label(label=label))
            btn.set_child(btn_box)
            btn.add_css_class("flat")
            btn.connect("clicked", lambda b, s=script: self._run_script(s))
            actions_box.append(btn)

        actions_group.add(actions_box)
        self.detail_box.append(actions_group)

        # Chat Stream
        chat_group = Adw.PreferencesGroup()
        chat_group.set_title("💬 Activity Stream")
        chat_group.set_description("Live conversation about what's happening")

        chat_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        chat_card.add_css_class("card")

        self.chat_stream = ChatStream(Path(victory["path"]))
        chat_card.append(self.chat_stream)

        chat_group.add(chat_card)
        self.detail_box.append(chat_group)

    def _load_victories(self) -> bool:
        """Load all victories into the sidebar."""
        self.victories = get_all_victories()

        # Clear list
        while row := self.victory_list.get_first_child():
            self.victory_list.remove(row)

        active_count = 0
        archived_count = 0

        # Active section header
        active_header = Gtk.Label(label="ACTIVE")
        active_header.add_css_class("caption")
        active_header.add_css_class("dim-label")
        active_header.set_halign(Gtk.Align.START)
        active_header.set_margin_start(12)
        active_header.set_margin_top(12)
        active_header.set_margin_bottom(6)
        self.victory_list.append(active_header)

        for victory in self.victories:
            if not victory["is_archived"]:
                row = VictoryRow(victory)
                self.victory_list.append(row)
                active_count += 1

        if active_count == 0:
            empty = Gtk.Label(label="No active victories")
            empty.add_css_class("dim-label")
            empty.set_margin_start(12)
            empty.set_margin_bottom(12)
            self.victory_list.append(empty)

        # Archived section header
        archive_header = Gtk.Label(label="ARCHIVED")
        archive_header.add_css_class("caption")
        archive_header.add_css_class("dim-label")
        archive_header.set_halign(Gtk.Align.START)
        archive_header.set_margin_start(12)
        archive_header.set_margin_top(18)
        archive_header.set_margin_bottom(6)
        self.victory_list.append(archive_header)

        for victory in self.victories:
            if victory["is_archived"]:
                row = VictoryRow(victory)
                self.victory_list.append(row)
                archived_count += 1

        if archived_count == 0:
            empty = Gtk.Label(label="No archived victories")
            empty.add_css_class("dim-label")
            empty.set_margin_start(12)
            empty.set_margin_bottom(12)
            self.victory_list.append(empty)

        # Update stats
        self.active_label.set_label(f"{active_count} Active")
        self.archived_label.set_label(f"{archived_count} Archived")

        return True  # For timeout

    def _on_victory_selected(self, listbox: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        """Handle victory selection."""
        if hasattr(row, 'victory_info'):
            self.selected_victory = row.victory_info
            self._build_detail_page(row.victory_info)
            self.content_stack.set_visible_child_name("detail")
            self.split_view.set_show_content(True)

    def _on_new_victory(self, button: Gtk.Button) -> None:
        """Create a new victory with dialog for name input."""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="Create New Victory",
            body="Enter a name for your new victory:"
        )

        entry = Gtk.Entry()
        entry.set_placeholder_text("e.g., MY_FEATURE")
        entry.set_margin_start(20)
        entry.set_margin_end(20)
        entry.set_margin_bottom(10)
        dialog.set_extra_child(entry)

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("create", "Create")
        dialog.set_response_appearance("create", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("create")
        dialog.set_close_response("cancel")

        def on_response(dialog: Adw.MessageDialog, response: str) -> None:
            if response == "create":
                name = entry.get_text().strip()
                if name:
                    name = name.replace(" ", "_").upper()
                    self._create_victory(name)
            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.present()

    def _create_victory(self, name: str) -> None:
        """Actually create the victory using generate_sejr.py script."""
        script_path = SCRIPTS_DIR / "generate_sejr.py"
        if script_path.exists():
            try:
                subprocess.run(
                    ["python3", str(script_path), "--name", name],
                    cwd=str(SYSTEM_PATH),
                    capture_output=True,
                    text=True
                )
                self._load_victories()

                # Find and select the new victory
                for victory in self.victories:
                    if name in victory["name"]:
                        self._build_detail_page(victory)
                        self.content_stack.set_visible_child_name("detail")
                        self.split_view.set_show_content(True)
                        subprocess.Popen(["nautilus", victory["path"]])
                        break
            except Exception as e:
                print(f"Error: {e}")

    def _on_convert_to_victory(self, button: Gtk.Button) -> None:
        """Open the universal converter dialog."""
        dialog = Adw.Window(transient_for=self)
        dialog.set_title("🔄 Universal Victory Converter")
        dialog.set_default_size(600, 700)
        dialog.set_modal(True)

        # Main content
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        dialog.set_content(main_box)

        # Header
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        main_box.append(header)

        # Content scroll
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)

        # Title
        title_label = Gtk.Label(label="Convert Anything to Victory Structure")
        title_label.add_css_class("title-1")
        content_box.append(title_label)

        subtitle_label = Gtk.Label(label="Select input type, control mode, and define 5W")
        subtitle_label.add_css_class("dim-label")
        content_box.append(subtitle_label)

        # Input type selection
        input_group = Adw.PreferencesGroup()
        input_group.set_title("📥 INPUT TYPE")
        input_group.set_description("What do you want to convert?")

        self.convert_input_type = Gtk.ComboBoxText()
        for key, label in VictoryConverter.INPUT_TYPES.items():
            self.convert_input_type.append(key, label)
        self.convert_input_type.set_active_id("folder")

        input_row = Adw.ActionRow()
        input_row.set_title("Type")
        input_row.add_suffix(self.convert_input_type)
        input_group.add(input_row)

        # Input path
        self.convert_input_entry = Gtk.Entry()
        self.convert_input_entry.set_placeholder_text("/path/to/folder/or/file")
        self.convert_input_entry.set_hexpand(True)

        path_row = Adw.ActionRow()
        path_row.set_title("Source")
        path_row.set_subtitle("Path to folder/file, or enter text")
        path_row.add_suffix(self.convert_input_entry)

        browse_btn = Gtk.Button(icon_name="folder-open-symbolic")
        browse_btn.set_valign(Gtk.Align.CENTER)
        browse_btn.connect("clicked", lambda b: self._browse_for_input())
        path_row.add_suffix(browse_btn)

        input_group.add(path_row)
        content_box.append(input_group)

        # Control mode selection
        mode_group = Adw.PreferencesGroup()
        mode_group.set_title("🎛️ CONTROL MODE")
        mode_group.set_description("How do you want to control the process?")

        self.convert_mode = Gtk.ComboBoxText()
        for key, label in VictoryConverter.CONTROL_MODES.items():
            self.convert_mode.append(key, label)
        self.convert_mode.set_active_id("manual")

        mode_row = Adw.ActionRow()
        mode_row.set_title("Mode")
        mode_row.add_suffix(self.convert_mode)
        mode_group.add(mode_row)
        content_box.append(mode_group)

        # 5W Control
        w5_group = Adw.PreferencesGroup()
        w5_group.set_title("🎯 5W CONTROL")
        w5_group.set_description("You have TOTAL CONTROL over everything")

        # WHAT
        self.convert_what = Gtk.Entry()
        self.convert_what.set_placeholder_text("What should be converted/built?")
        what_row = Adw.ActionRow()
        what_row.set_title("WHAT")
        what_row.set_subtitle("Description of the task")
        what_row.add_suffix(self.convert_what)
        w5_group.add(what_row)

        # WHY
        self.convert_why = Gtk.Entry()
        self.convert_why.set_placeholder_text("Purpose of this victory")
        why_row = Adw.ActionRow()
        why_row.set_title("WHY")
        why_row.set_subtitle("Purpose/value")
        why_row.add_suffix(self.convert_why)
        w5_group.add(why_row)

        # HOW
        self.convert_how = Gtk.Entry()
        self.convert_how.set_placeholder_text("3-pass system")
        how_row = Adw.ActionRow()
        how_row.set_title("HOW")
        how_row.set_subtitle("Approach/methodology")
        how_row.add_suffix(self.convert_how)
        w5_group.add(how_row)

        # WHEN
        self.convert_when = Gtk.Entry()
        self.convert_when.set_placeholder_text("Now -> Complete")
        when_row = Adw.ActionRow()
        when_row.set_title("WHEN")
        when_row.set_subtitle("Timeline/deadline")
        when_row.add_suffix(self.convert_when)
        w5_group.add(when_row)

        content_box.append(w5_group)

        # Victory name
        name_group = Adw.PreferencesGroup()
        name_group.set_title("📛 VICTORY NAME")

        self.convert_name = Gtk.Entry()
        self.convert_name.set_placeholder_text("PROJECT_NAME")
        name_row = Adw.ActionRow()
        name_row.set_title("Name")
        name_row.set_subtitle("Name of the new victory (UPPERCASE)")
        name_row.add_suffix(self.convert_name)
        name_group.add(name_row)
        content_box.append(name_group)

        scroll.set_child(content_box)
        main_box.append(scroll)

        # Action bar
        action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        action_bar.set_margin_start(24)
        action_bar.set_margin_end(24)
        action_bar.set_margin_top(16)
        action_bar.set_margin_bottom(16)
        action_bar.set_halign(Gtk.Align.END)

        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect("clicked", lambda b: dialog.close())
        action_bar.append(cancel_btn)

        create_btn = Gtk.Button(label="🚀 Create Victory")
        create_btn.add_css_class("suggested-action")
        create_btn.connect("clicked", lambda b: self._execute_conversion(dialog))
        action_bar.append(create_btn)

        main_box.append(action_bar)

        dialog.present()

    def _browse_for_input(self) -> None:
        """Open file browser for input selection."""
        subprocess.Popen(["nautilus", str(SYSTEM_PATH)])
        send_notification("📁 File Browser", "Copy the path of what you want to convert")

    def _execute_conversion(self, dialog: Adw.Window) -> None:
        """Execute the conversion based on dialog inputs."""
        converter = VictoryConverter(SYSTEM_PATH)

        config = {
            "name": self.convert_name.get_text().strip().upper().replace(" ", "_") or "NEW_VICTORY",
            "input_path": self.convert_input_entry.get_text().strip(),
            "input_type": self.convert_input_type.get_active_id(),
            "mode": self.convert_mode.get_active_id(),
            "what": self.convert_what.get_text().strip(),
            "why": self.convert_why.get_text().strip(),
            "how": self.convert_how.get_text().strip() or "3-pass system",
            "when": self.convert_when.get_text().strip() or "Now -> Complete",
            "tasks": [],
        }

        # Analyze input
        if config["input_path"]:
            analysis = converter.analyze_input(config["input_path"], config["input_type"])
            config["tasks"] = analysis.get("suggested_tasks", [])

            if config["name"] == "NEW_VICTORY" and analysis.get("suggested_name"):
                config["name"] = analysis["suggested_name"]

        # Default tasks
        if not config["tasks"]:
            config["tasks"] = [
                "Analyze input",
                "Plan structure",
                "Implement solution",
                "Verify result",
                "Document",
            ]

        # Create victory
        victory_path = converter.create_victory_from_input(config)

        dialog.close()
        self._load_victories()

        # Select and show new victory
        for victory in self.victories:
            if config["name"] in victory["name"]:
                self.selected_victory = victory
                self._build_detail_page(victory)
                self.content_stack.set_visible_child_name("detail")
                self.split_view.set_show_content(True)

                subprocess.Popen(["nautilus", str(victory_path)])

                send_notification(
                    "✅ Victory Created!",
                    f"{config['name']} is ready with 5W control"
                )

                if self.chat_stream:
                    self.chat_stream.add_message(
                        sender="System",
                        content=f"New victory created: {config['name']}",
                        msg_type="info",
                        file_link=str(victory_path / "SEJR_LISTE.md")
                    )
                break

    def _run_script(self, script_name: str) -> None:
        """Run a DNA layer script with notifications and chat updates."""
        script_path = SCRIPTS_DIR / script_name

        # Script metadata
        script_info = {
            "auto_verify.py": {
                "sender": "Verify",
                "start_msg": "Running verification...",
                "success_msg": "✅ All tests passed!",
                "title": "✅ Verification",
                "body": "Victory verified!"
            },
            "auto_learn.py": {
                "sender": "DNA",
                "start_msg": "Analyzing patterns...",
                "success_msg": "🧠 New patterns learned and saved!",
                "title": "🧠 Patterns",
                "body": "New patterns learned!"
            },
            "auto_predict.py": {
                "sender": "Kv1nt",
                "start_msg": "Generating predictions...",
                "success_msg": "🔮 Next steps calculated!",
                "title": "🔮 Predictions",
                "body": "Predictions generated!"
            },
            "auto_archive.py": {
                "sender": "Admiral",
                "start_msg": "Archiving victory...",
                "success_msg": "🏆 VICTORY ARCHIVED! You're amazing!",
                "title": "🏆 Archived",
                "body": "Victory archived successfully!"
            },
        }

        info = script_info.get(script_name, {
            "sender": "System",
            "start_msg": f"Running {script_name}...",
            "success_msg": "Script complete",
            "title": "Script",
            "body": "Complete"
        })

        # Add starting message to chat
        if self.chat_stream:
            self.chat_stream.add_message(
                sender=info["sender"],
                content=info["start_msg"],
                msg_type="info"
            )

        if script_path.exists():
            try:
                result = subprocess.run(
                    ["python3", str(script_path)],
                    cwd=str(SYSTEM_PATH),
                    capture_output=True,
                    text=True
                )
                self._load_victories()

                # Add success message to chat
                if self.chat_stream:
                    output = result.stdout.strip() if result.stdout else info["success_msg"]
                    if len(output) > 200:
                        output = output[:200] + "..."

                    self.chat_stream.add_message(
                        sender=info["sender"],
                        content=output if output else info["success_msg"],
                        msg_type="info",
                        verification={
                            "passed": result.returncode == 0,
                            "message": "Verified" if result.returncode == 0 else "Error"
                        }
                    )

                send_notification(info["title"], info["body"])

                # Celebration for archive
                if script_name == "auto_archive.py":
                    self._show_celebration()

            except Exception as e:
                if self.chat_stream:
                    self.chat_stream.add_message(
                        sender="Error",
                        content=f"Script failed: {e}",
                        msg_type="error",
                        verification={"passed": False, "message": str(e)}
                    )
                send_notification("❌ Error", f"Script failed: {e}")
                print(f"Error: {e}")

    def _show_celebration(self) -> None:
        """Show celebration dialog when victory is archived."""
        stats = get_system_stats()

        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="🏆 VICTORY ARCHIVED!",
            body=f"""Congratulations! Your victory is now archived.

📊 System Status:
• Total victories: {stats['total_victories']}
• Active: {stats['active']}
• Archived: {stats['archived']}
• Grand Admirals: {stats['grand_admirals']} 🏅

You're on your way to Admiral level!"""
        )

        dialog.add_response("ok", "Fantastic! 🎉")
        dialog.set_default_response("ok")
        dialog.present()

    def _open_current_folder(self) -> None:
        """Open current victory folder in file browser."""
        if self.selected_victory:
            subprocess.Popen(["nautilus", self.selected_victory["path"]])
        else:
            subprocess.Popen(["nautilus", str(SYSTEM_PATH)])

    def _auto_refresh(self) -> bool:
        """Auto-refresh every 5 seconds."""
        self._load_victories()
        if self.selected_victory:
            for victory in self.victories:
                if victory["path"] == self.selected_victory["path"]:
                    self._build_detail_page(victory)
                    break
        return True

    # =========================================================================
    # SEARCH HANDLERS
    # =========================================================================

    def _on_search_toggled(self, button: Gtk.ToggleButton) -> None:
        """Toggle search mode on/off."""
        self.search_mode = button.get_active()
        self.search_bar.set_search_mode(self.search_mode)

        if self.search_mode:
            self.search_results_scroll.set_visible(True)
            self.search_entry.grab_focus()
        else:
            self.search_results_scroll.set_visible(False)
            self._clear_search_results()
            self.search_entry.set_text("")

    def _on_search_changed(self, entry: Gtk.SearchEntry) -> None:
        """Handle live search as user types."""
        query = entry.get_text().strip()

        if len(query) < 2:
            self._clear_search_results()
            return

        results = self.search_engine.search(query, max_results=30)
        self._display_search_results(results, query)

    def _on_search_activate(self, entry: Gtk.SearchEntry) -> None:
        """Handle Enter press in search."""
        query = entry.get_text().strip()

        if len(query) < 2:
            return

        results = self.search_engine.search(query, max_results=50)
        self._display_search_results(results, query)

    def _clear_search_results(self) -> None:
        """Clear all search result rows."""
        while row := self.search_results_list.get_first_child():
            self.search_results_list.remove(row)

    def _display_search_results(self, results: List[Dict[str, Any]], query: str) -> None:
        """Display search results in the list."""
        self._clear_search_results()

        if not results:
            empty_row = Adw.ActionRow()
            empty_row.set_title("No results")
            empty_row.set_subtitle(f'No match for "{query}"')
            empty_row.add_prefix(Gtk.Image.new_from_icon_name("dialog-question-symbolic"))
            self.search_results_list.append(empty_row)
            return

        # Results header
        header = Gtk.Label(label=f"RESULTS ({len(results)})")
        header.add_css_class("caption")
        header.add_css_class("dim-label")
        header.set_halign(Gtk.Align.START)
        header.set_margin_start(12)
        header.set_margin_top(12)
        header.set_margin_bottom(6)
        self.search_results_list.append(header)

        # Group by victory
        current_victory = None

        for result in results:
            if result["victory"] != current_victory:
                current_victory = result["victory"]
                victory_header = Gtk.Label(
                    label=current_victory.split("_2026")[0].replace("_", " ")
                )
                victory_header.add_css_class("heading")
                victory_header.set_halign(Gtk.Align.START)
                victory_header.set_margin_start(12)
                victory_header.set_margin_top(8)
                victory_header.set_margin_bottom(4)
                self.search_results_list.append(victory_header)

            # Result row
            row = Adw.ActionRow()
            row.result_data = result

            icon_name = {
                "folder": "folder-symbolic",
                "filename": "text-x-generic-symbolic",
                "content": "format-text-rich-symbolic",
                "log": "text-x-log-symbolic"
            }.get(result["match_type"], "text-x-generic-symbolic")

            row.add_prefix(Gtk.Image.new_from_icon_name(icon_name))

            title = result["context"][:80]
            if len(result["context"]) > 80:
                title += "..."
            row.set_title(title)

            if result["line_num"] > 0:
                row.set_subtitle(f'{result["file"]} : line {result["line_num"]}')
            else:
                row.set_subtitle(result["file"])

            type_badge = Gtk.Label(label=result["match_type"].upper())
            type_badge.add_css_class("caption")
            type_badge.add_css_class("dim-label")
            row.add_suffix(type_badge)

            row.set_activatable(True)
            self.search_results_list.append(row)

    def _on_search_result_activated(self, listbox: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        """Handle click on a search result."""
        if not hasattr(row, 'result_data'):
            return

        result = row.result_data

        # Find victory folder
        victory_path = None

        active_path = ACTIVE_DIR / result["victory"]
        if active_path.exists():
            victory_path = active_path

        if not victory_path:
            archive_path = ARCHIVE_DIR / result["victory"]
            if archive_path.exists():
                victory_path = archive_path

        if not victory_path:
            return

        # Show victory detail
        victory_info = get_victory_info(victory_path)
        self.selected_victory = victory_info
        self._build_detail_page(victory_info)
        self.content_stack.set_visible_child_name("detail")
        self.split_view.set_show_content(True)

        # Open file if content match
        if result["match_type"] in ["content", "filename", "log"]:
            file_path = victory_path / result["file"]
            if file_path.exists():
                try:
                    subprocess.Popen(["xdg-open", str(file_path)])
                except Exception as e:
                    print(f"Could not open file: {e}")

        # Close search
        self.search_btn.set_active(False)


# ==============================================================================
# APPLICATION
# ==============================================================================

class VictoryListApp(Adw.Application):
    """
    The main application class.

    Handles:
    - Application lifecycle
    - CSS loading
    - Keyboard shortcuts
    - Window creation
    """

    def __init__(self):
        """Initialize the application."""
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        # Force dark mode for modern look
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def do_activate(self) -> None:
        """Activate the application."""
        # Load CSS
        load_custom_css()

        # Create window
        win = MainWindow(self)

        # Setup shortcuts
        self._setup_shortcuts(win)

        win.present()

    def _setup_shortcuts(self, win: MainWindow) -> None:
        """Setup keyboard shortcuts."""
        # Ctrl+F for search
        search_action = Gio.SimpleAction.new("search", None)
        search_action.connect("activate", lambda a, p: win.search_btn.set_active(True))
        self.add_action(search_action)
        self.set_accels_for_action("app.search", ["<Control>f"])

        # Escape to close search
        escape_action = Gio.SimpleAction.new("escape", None)
        escape_action.connect("activate", lambda a, p: win.search_btn.set_active(False))
        self.add_action(escape_action)
        self.set_accels_for_action("app.escape", ["Escape"])

        # Ctrl+R for refresh
        refresh_action = Gio.SimpleAction.new("refresh", None)
        refresh_action.connect("activate", lambda a, p: win._load_victories())
        self.add_action(refresh_action)
        self.set_accels_for_action("app.refresh", ["<Control>r"])

        # Ctrl+O for open folder
        open_action = Gio.SimpleAction.new("open-folder", None)
        open_action.connect("activate", lambda a, p: win._open_current_folder())
        self.add_action(open_action)
        self.set_accels_for_action("app.open-folder", ["<Control>o"])

        # Ctrl+N for new victory
        new_action = Gio.SimpleAction.new("new-victory", None)
        new_action.connect("activate", lambda a, p: win._on_new_victory(None))
        self.add_action(new_action)
        self.set_accels_for_action("app.new-victory", ["<Control>n"])


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main() -> int:
    """
    Main entry point for the application.

    Returns:
        Exit code (0 for success)
    """
    app = VictoryListApp()
    return app.run(None)


if __name__ == "__main__":
    main()
