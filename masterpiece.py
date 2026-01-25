#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║             SEJRLISTE MESTERVÆRK - GTK4 + LIBADWAITA NATIVE                   ║
║                                                                               ║
║   A modern, native GNOME application for the Sejrliste system                 ║
║   Built with GTK4 and Libadwaita for a truly contemporary look                ║
║                                                                               ║
║   Features:                                                                   ║
║   • AdwNavigationSplitView - Modern sidebar navigation                        ║
║   • AdwStatusPage - Beautiful empty/welcome states                            ║
║   • AdwActionRow - Polished list items with progress                          ║
║   • 7 DNA Layers - Visual status indicators                                   ║
║   • Real-time updates - Auto-refresh from filesystem                          ║
║                                                                               ║
║   Author: Kv1nt (Claude Opus 4.5) for Rasmus                                  ║
║   Date: 2026-01-25                                                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Pango, Gdk
from pathlib import Path
import re
import json
from datetime import datetime
import subprocess

# ═══════════════════════════════════════════════════════════════════════════════
# MODERNE 2026 CSS STYLING - PASS 2 UPGRADE
# ═══════════════════════════════════════════════════════════════════════════════

MODERN_CSS = """
/* ══════════════════════════════════════════════════════════════════
   SEJRLISTE MESTERVÆRK - MODERNE 2026 DESIGN
   Features: Gradients, Glassmorphism, Animations, Modern Typography
   ══════════════════════════════════════════════════════════════════ */

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

def load_custom_css():
    """Load modern CSS styling"""
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(MODERN_CSS.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

def send_notification(title: str, body: str, icon: str = "emblem-ok-symbolic"):
    """Send desktop notification"""
    try:
        subprocess.run([
            "notify-send",
            "-i", icon,
            "-a", "Sejrliste Mesterværk",
            title,
            body
        ], check=False)
    except:
        pass

def get_system_stats() -> dict:
    """Get overall system statistics"""
    stats = {
        "total_sejrs": 0,
        "active": 0,
        "archived": 0,
        "total_checkboxes": 0,
        "completed_checkboxes": 0,
        "grand_admirals": 0,
    }

    if ACTIVE_DIR.exists():
        for folder in ACTIVE_DIR.iterdir():
            if folder.is_dir() and not folder.name.startswith("."):
                stats["active"] += 1
                stats["total_sejrs"] += 1
                sejr_file = folder / "SEJR_LISTE.md"
                if sejr_file.exists():
                    done, total = count_checkboxes(sejr_file.read_text())
                    stats["total_checkboxes"] += total
                    stats["completed_checkboxes"] += done

    if ARCHIVE_DIR.exists():
        for folder in ARCHIVE_DIR.iterdir():
            if folder.is_dir() and not folder.name.startswith("."):
                stats["archived"] += 1
                stats["total_sejrs"] += 1
                # Check for Grand Admiral (27+ score)
                conclusion = folder / "CONCLUSION.md"
                if conclusion.exists():
                    content = conclusion.read_text()
                    if "GRAND ADMIRAL" in content or "27/30" in content or "30/30" in content:
                        stats["grand_admirals"] += 1

    return stats

# ═══════════════════════════════════════════════════════════════════════════════
# INTELLIGENT SEARCH ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# UNIVERSAL SEJR CONVERTER - FRA ALT TIL SEJR STRUKTUR
# ═══════════════════════════════════════════════════════════════════════════════

class SejrConverter:
    """
    Universal converter: Enhver mappe, fil, PDF, tekst, kommando → SEJR struktur

    MULTI-KONTROLBART:
    - Manual mode: Rasmus styrer alt
    - Kv1nt mode: AI-assisteret med forslag
    - Admiral mode: Fuldt automatisk med verifikation

    5W KONTROL:
    - HVAD: Hvad konverteres
    - HVOR: Hvor gemmes det
    - HVORFOR: Formål med sejren
    - HVORDAN: Hvilken tilgang
    - HVORNÅR: Timeline og milestones
    """

    INPUT_TYPES = {
        "folder": "📁 Mappe",
        "file": "📄 Fil",
        "pdf": "📕 PDF",
        "text": "📝 Tekst",
        "command": "💻 Kommando",
    }

    CONTROL_MODES = {
        "manual": "✋ Manuel - Du styrer ALT",
        "kv1nt": "🤖 Kv1nt - AI-assisteret med forslag",
        "admiral": "🎖️ Admiral - Fuld automatisk",
    }

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.active_dir = system_path / "10_ACTIVE"
        self.templates_dir = system_path / "00_TEMPLATES"

    def analyze_input(self, input_path: str, input_type: str) -> dict:
        """Analyze input and suggest SEJR structure"""
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

            # Detect structure
            for f in files[:20]:  # First 20 files
                if f.is_file():
                    analysis["suggested_tasks"].append(f"Behandl {f.name}")

        elif input_type == "file" and path.exists() and path.is_file():
            analysis["exists"] = True
            analysis["suggested_name"] = path.stem.upper().replace(" ", "_")
            analysis["file_count"] = 1
            analysis["total_size"] = path.stat().st_size

            # Read and analyze content
            if path.suffix in [".md", ".txt"]:
                try:
                    content = path.read_text()
                    # Find headers as tasks
                    for line in content.split("\n"):
                        if line.startswith("# ") or line.startswith("## "):
                            analysis["detected_sections"].append(line.strip("#").strip())
                except:
                    pass

        elif input_type == "text":
            analysis["exists"] = True
            analysis["suggested_name"] = "TEKST_PROJEKT"
            # Parse text for structure
            lines = input_path.split("\n")
            for line in lines:
                if line.strip():
                    analysis["suggested_tasks"].append(f"[ ] {line.strip()[:50]}")

        elif input_type == "command":
            analysis["exists"] = True
            analysis["suggested_name"] = "KOMMANDO_SEJR"
            analysis["suggested_tasks"] = [
                "[ ] Kør kommando",
                "[ ] Verificer output",
                "[ ] Dokumenter resultat",
            ]

        return analysis

    def create_sejr_from_input(self, config: dict) -> Path:
        """
        Create SEJR structure from analyzed input

        config = {
            "name": "PROJEKT_NAVN",
            "input_path": "/path/to/input",
            "input_type": "folder|file|pdf|text|command",
            "mode": "manual|kv1nt|admiral",
            "hvad": "Beskrivelse af hvad",
            "hvor": "Destination folder",
            "hvorfor": "Formål",
            "hvordan": "Tilgang",
            "hvornaar": "Timeline",
            "tasks": ["Task 1", "Task 2", ...],
        }
        """
        # Generate folder name with date
        date_str = datetime.now().strftime("%Y-%m-%d")
        folder_name = f"{config['name']}_{date_str}"
        sejr_path = self.active_dir / folder_name

        # Create folder
        sejr_path.mkdir(parents=True, exist_ok=True)

        # Generate SEJR_LISTE.md content
        sejr_content = f"""# SEJR: {config['name']}

**Oprettet:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Status:** 🔵 PASS 1 - IN PROGRESS
**Ejer:** Rasmus + Kv1nt
**Current Pass:** 1/3

**Kilde:** {config.get('input_type', 'unknown')} → {config.get('input_path', 'N/A')}
**Mode:** {config.get('mode', 'manual')}

---

## 5W KONTROL

| Kontrol | Værdi |
|---------|-------|
| **HVAD** | {config.get('hvad', 'Konvertering til sejr struktur')} |
| **HVOR** | {sejr_path} |
| **HVORFOR** | {config.get('hvorfor', 'Systematisk eksekvering')} |
| **HVORDAN** | {config.get('hvordan', '3-pass system')} |
| **HVORNÅR** | {config.get('hvornaar', 'Nu → Færdig')} |

---

## ⚠️ 3-PASS KONKURRENCE SYSTEM (OBLIGATORISK)

```
PASS 1: FUNGERENDE     → "Get it working"      → REVIEW REQUIRED
PASS 2: FORBEDRET      → "Make it better"      → REVIEW REQUIRED
PASS 3: OPTIMERET      → "Make it best"        → FINAL VERIFICATION
                                                        ↓
                                               ✅ KAN ARKIVERES
```

---

# 🥉 PASS 1: FUNGERENDE ("Get It Working")

## Tasks

"""
        # Add tasks
        for task in config.get('tasks', []):
            if not task.startswith("- [ ]"):
                task = f"- [ ] {task}"
            sejr_content += f"{task}\n"

        sejr_content += """
---

## Verification

- [ ] Alle tasks completeret
- [ ] Output verificeret
- [ ] Ready for Pass 2

---

# 🥈 PASS 2: FORBEDRET ("Make It Better")

*Udfyldes efter Pass 1 er færdig*

---

# 🥇 PASS 3: OPTIMERET ("Make It Best")

*Udfyldes efter Pass 2 er færdig*
"""

        # Write SEJR_LISTE.md
        (sejr_path / "SEJR_LISTE.md").write_text(sejr_content)

        # Create CLAUDE.md focus lock
        claude_content = f"""# CLAUDE FOKUS LOCK - LÆS DETTE FØRST

> **DU ER I EN SEJR LISTE MAPPE. DU HAR ÉN OPGAVE. FOKUSÉR.**

---

## 🔒 CURRENT STATE

**Sejr:** {config['name']}
**Current Pass:** 1/3
**Status:** Pass 1 - Fungerende
**Input:** {config.get('input_type', 'unknown')}

---

## 🎯 DIN ENESTE OPGAVE LIGE NU

```
Læs SEJR_LISTE.md og arbejd på første task
```

**INTET ANDET.** Færdiggør dette før du gør noget andet.
"""
        (sejr_path / "CLAUDE.md").write_text(claude_content)

        # Create STATUS.yaml
        status_content = f"""# SEJR STATUS
name: {config['name']}
created: {datetime.now().isoformat()}
current_pass: 1
status: in_progress

input:
  type: {config.get('input_type', 'unknown')}
  path: {config.get('input_path', 'N/A')}

control:
  mode: {config.get('mode', 'manual')}
  hvad: {config.get('hvad', '')}
  hvor: {str(sejr_path)}
  hvorfor: {config.get('hvorfor', '')}
  hvordan: {config.get('hvordan', '')}
  hvornaar: {config.get('hvornaar', '')}

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
        (sejr_path / "STATUS.yaml").write_text(status_content)

        # Initialize AUTO_LOG.jsonl
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "sejr_created",
            "source": config.get('input_type', 'unknown'),
            "mode": config.get('mode', 'manual'),
            "detail": f"Oprettet fra {config.get('input_path', 'N/A')}"
        }
        (sejr_path / "AUTO_LOG.jsonl").write_text(json.dumps(log_entry) + "\n")

        return sejr_path


class IntelligentSearch:
    """
    Intelligent search across all sejr files, code, and details.
    Searches: filenames, file contents, checkboxes, logs, code patterns
    """

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.active_dir = system_path / "10_ACTIVE"
        self.archive_dir = system_path / "90_ARCHIVE"

    def search(self, query: str, max_results: int = 50) -> list:
        """
        Search for query across all sejr folders.
        Returns list of dicts with: sejr, file, line_num, context, match_type
        """
        if not query or len(query) < 2:
            return []

        results = []
        query_lower = query.lower()

        # Search active sejrs
        if self.active_dir.exists():
            for sejr_folder in self.active_dir.iterdir():
                if sejr_folder.is_dir() and not sejr_folder.name.startswith("."):
                    results.extend(self._search_sejr(sejr_folder, query_lower))

        # Search archived sejrs
        if self.archive_dir.exists():
            for sejr_folder in self.archive_dir.iterdir():
                if sejr_folder.is_dir() and not sejr_folder.name.startswith("."):
                    results.extend(self._search_sejr(sejr_folder, query_lower))

        # Sort by relevance (exact matches first, then partial)
        results.sort(key=lambda x: (0 if query_lower in x["match"].lower() else 1, x["sejr"]))

        return results[:max_results]

    def _search_sejr(self, sejr_folder: Path, query: str) -> list:
        """Search within a single sejr folder"""
        results = []

        # Search folder name
        if query in sejr_folder.name.lower():
            results.append({
                "sejr": sejr_folder.name,
                "file": "(folder name)",
                "line_num": 0,
                "context": sejr_folder.name,
                "match": sejr_folder.name,
                "match_type": "folder"
            })

        # Search files
        for file_path in sejr_folder.iterdir():
            if file_path.is_file():
                results.extend(self._search_file(file_path, sejr_folder.name, query))

        return results

    def _search_file(self, file_path: Path, sejr_name: str, query: str) -> list:
        """Search within a single file"""
        results = []

        # Search filename
        if query in file_path.name.lower():
            results.append({
                "sejr": sejr_name,
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
                        # Get context (surrounding text)
                        context = line.strip()[:100]
                        if len(line.strip()) > 100:
                            context += "..."

                        results.append({
                            "sejr": sejr_name,
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
                        except:
                            context = line[:100]

                        results.append({
                            "sejr": sejr_name,
                            "file": file_path.name,
                            "line_num": i,
                            "context": context[:100],
                            "match": self._extract_match(line, query),
                            "match_type": "log"
                        })
        except Exception as e:
            pass

        return results

    def _extract_match(self, line: str, query: str) -> str:
        """Extract the matching portion with some context"""
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

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"

DNA_LAYERS = [
    ("1", "SELF-AWARE", "System kender sig selv", "emblem-system-symbolic"),
    ("2", "SELF-DOCUMENTING", "Auto-logger handlinger", "document-edit-symbolic"),
    ("3", "SELF-VERIFYING", "Auto-verificerer", "emblem-ok-symbolic"),
    ("4", "SELF-IMPROVING", "Lærer patterns", "view-refresh-symbolic"),
    ("5", "SELF-ARCHIVING", "Arkiverer semantisk", "folder-symbolic"),
    ("6", "PREDICTIVE", "Forudsiger næste", "weather-clear-symbolic"),
    ("7", "SELF-OPTIMIZING", "3 alternativer", "applications-engineering-symbolic"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def count_checkboxes(content: str) -> tuple:
    """Count checked and total checkboxes"""
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked

def get_sejr_info(path: Path) -> dict:
    """Get comprehensive info about a sejr"""
    sejr_file = path / "SEJR_LISTE.md"
    status_file = path / "STATUS.yaml"

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
        except:
            pass

    # Count checkboxes
    if sejr_file.exists():
        content = sejr_file.read_text()
        done, total = count_checkboxes(content)
        info["done"] = done
        info["total"] = total
        info["progress"] = int((done / total * 100) if total > 0 else 0)

        # Find current pass
        if "Pass 3" in content and "PASS 3" in content.upper():
            info["current_pass"] = "3"
        elif "Pass 2" in content and "PASS 2" in content.upper():
            info["current_pass"] = "2"

    # List files
    if path.exists():
        info["files"] = [f.name for f in path.iterdir() if f.is_file()]

    return info

def get_all_sejrs() -> list:
    """Get all sejrs sorted by date"""
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
# CUSTOM WIDGETS
# ═══════════════════════════════════════════════════════════════════════════════

class SejrRow(Adw.ActionRow):
    """A row representing a sejr in the sidebar"""

    def __init__(self, sejr_info: dict):
        super().__init__()
        self.sejr_info = sejr_info

        self.set_title(sejr_info["display_name"])
        self.set_subtitle(f"Pass {sejr_info['current_pass']}/3 • {sejr_info['date']}")

        # Icon based on status
        if sejr_info["is_archived"]:
            icon = Gtk.Image.new_from_icon_name("emblem-ok-symbolic")
            icon.add_css_class("success")
        elif sejr_info["progress"] >= 80:
            icon = Gtk.Image.new_from_icon_name("emblem-important-symbolic")
            icon.add_css_class("warning")
        else:
            icon = Gtk.Image.new_from_icon_name("folder-open-symbolic")

        self.add_prefix(icon)

        # Progress indicator
        progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        progress_box.set_valign(Gtk.Align.CENTER)

        progress_label = Gtk.Label(label=f"{sejr_info['progress']}%")
        progress_label.add_css_class("caption")
        progress_box.append(progress_label)

        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(sejr_info["progress"] / 100)
        progress_bar.set_size_request(60, 4)

        if sejr_info["progress"] >= 80:
            progress_bar.add_css_class("success")
        elif sejr_info["progress"] >= 50:
            progress_bar.add_css_class("warning")

        progress_box.append(progress_bar)
        self.add_suffix(progress_box)

        # Make it activatable
        self.set_activatable(True)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAT STREAM WIDGET - MESSENGER-STYLE INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

class ChatMessage(Gtk.Box):
    """A single chat message in the stream - like Messenger"""

    def __init__(self, sender: str, content: str, timestamp: str = None,
                 msg_type: str = "info", file_link: str = None, verification: dict = None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        self.file_link = file_link

        # Determine if this is user message (right side) or system (left side)
        is_user = sender.lower() in ["rasmus", "bruger", "dig", "user"]

        if is_user:
            self.set_halign(Gtk.Align.END)
        else:
            self.set_halign(Gtk.Align.START)

        self.set_margin_start(12 if not is_user else 60)
        self.set_margin_end(12 if is_user else 60)
        self.set_margin_top(4)
        self.set_margin_bottom(4)

        # Avatar (only for non-user messages)
        if not is_user:
            avatar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            avatar_box.set_valign(Gtk.Align.START)

            # Emoji avatar based on sender
            avatar_emojis = {
                "system": "🖥️",
                "kv1nt": "🤖",
                "admiral": "🎖️",
                "dna": "🧬",
                "verify": "✅",
                "error": "❌",
                "info": "💬",
            }
            emoji = avatar_emojis.get(sender.lower(), "💬")

            avatar_label = Gtk.Label(label=emoji)
            avatar_label.set_markup(f'<span size="large">{emoji}</span>')
            avatar_box.append(avatar_label)

            self.append(avatar_box)

        # Message bubble
        bubble = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        bubble.add_css_class("chat-bubble")
        if is_user:
            bubble.add_css_class("chat-bubble-user")
        else:
            bubble.add_css_class("chat-bubble-system")

        # Sender name (only for non-user)
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

        # File link if provided
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

        # Verification status if provided
        if verification:
            verify_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            verify_box.add_css_class("chat-verification")

            status_icon = "emblem-ok-symbolic" if verification.get("passed") else "dialog-warning-symbolic"
            verify_box.append(Gtk.Image.new_from_icon_name(status_icon))

            verify_label = Gtk.Label(label=verification.get("message", "Verificeret"))
            verify_label.add_css_class("caption")
            if verification.get("passed"):
                verify_label.add_css_class("success")
            else:
                verify_label.add_css_class("warning")
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

        # Avatar for user (on right side)
        if is_user:
            avatar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            avatar_box.set_valign(Gtk.Align.START)
            avatar_label = Gtk.Label()
            avatar_label.set_markup('<span size="large">👤</span>')
            avatar_box.append(avatar_label)
            self.append(avatar_box)

    def _on_file_clicked(self, button):
        """Open the linked file"""
        if self.file_link:
            try:
                subprocess.Popen(["xdg-open", self.file_link])
            except:
                pass


class ChatStream(Gtk.Box):
    """A scrollable chat stream showing activity like Messenger"""

    def __init__(self, sejr_path: Path = None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.sejr_path = sejr_path
        self.messages = []

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
        clear_btn.set_tooltip_text("Ryd stream")
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

        # Load existing messages from AUTO_LOG.jsonl if available
        if sejr_path:
            self._load_from_log(sejr_path)

    def _load_from_log(self, sejr_path: Path):
        """Load messages from AUTO_LOG.jsonl"""
        log_file = sejr_path / "AUTO_LOG.jsonl"
        if not log_file.exists():
            # Add welcome message
            self.add_message(
                sender="Kv1nt",
                content=f"Velkommen til {sejr_path.name.split('_2026')[0].replace('_', ' ')}! Jeg holder øje med alt der sker her.",
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
                            "message": data.get("result", "Verificeret")
                        }

                    self.add_message(
                        sender=sender,
                        content=detail[:200],
                        timestamp=timestamp,
                        file_link=file_link,
                        verification=verification
                    )
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            self.add_message(
                sender="System",
                content=f"Kunne ikke læse log: {e}",
                msg_type="error"
            )

    def add_message(self, sender: str, content: str, timestamp: str = None,
                    msg_type: str = "info", file_link: str = None, verification: dict = None):
        """Add a new message to the stream"""
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

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        adj = self.scroll_window.get_vadjustment()
        adj.set_value(adj.get_upper())
        return False

    def clear_messages(self):
        """Clear all messages"""
        while child := self.message_box.get_first_child():
            self.message_box.remove(child)
        self.messages = []

        # Add cleared message
        self.add_message(
            sender="System",
            content="Stream ryddet",
            msg_type="info"
        )


class DNALayerRow(Gtk.Box):
    """A row showing a DNA layer status"""

    def __init__(self, layer_num, name, description, icon_name, active=False):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(8)
        self.set_margin_bottom(8)

        # Status indicator
        status_icon = Gtk.Image.new_from_icon_name(
            "emblem-ok-symbolic" if active else "content-loading-symbolic"
        )
        if active:
            status_icon.add_css_class("success")
        else:
            status_icon.add_css_class("dim-label")
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


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class MasterpieceWindow(Adw.ApplicationWindow):
    """The main application window"""

    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Sejrliste Mesterværk")
        self.set_default_size(1200, 800)

        self.selected_sejr = None
        self.sejrs = []
        self.search_engine = IntelligentSearch(SYSTEM_PATH)
        self.search_mode = False

        self._build_ui()
        self._load_sejrs()

        # Auto-refresh every 5 seconds
        GLib.timeout_add_seconds(5, self._auto_refresh)

    def _build_ui(self):
        """Build the user interface"""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        # Header bar
        header = Adw.HeaderBar()

        # Title widget
        title_widget = Adw.WindowTitle()
        title_widget.set_title("Sejrliste")
        title_widget.set_subtitle("Mesterværk Edition")
        header.set_title_widget(title_widget)

        # Refresh button
        refresh_btn = Gtk.Button(icon_name="view-refresh-symbolic")
        refresh_btn.set_tooltip_text("Refresh")
        refresh_btn.connect("clicked", lambda b: self._load_sejrs())
        header.pack_start(refresh_btn)

        # New Sejr button
        new_btn = Gtk.Button(icon_name="list-add-symbolic")
        new_btn.set_tooltip_text("Ny Sejr (Ctrl+N)")
        new_btn.add_css_class("suggested-action")
        new_btn.connect("clicked", self._on_new_sejr)
        header.pack_start(new_btn)

        # Universal Converter button
        convert_btn = Gtk.Button(icon_name="document-import-symbolic")
        convert_btn.set_tooltip_text("Konverter til Sejr (fra mappe/fil/tekst)")
        convert_btn.connect("clicked", self._on_convert_to_sejr)
        header.pack_start(convert_btn)

        # Search toggle button
        self.search_btn = Gtk.ToggleButton(icon_name="system-search-symbolic")
        self.search_btn.set_tooltip_text("Intelligent Søgning (Ctrl+F)")
        self.search_btn.connect("toggled", self._on_search_toggled)
        header.pack_end(self.search_btn)

        # Menu button
        menu_btn = Gtk.MenuButton(icon_name="open-menu-symbolic")
        header.pack_end(menu_btn)

        main_box.append(header)

        # Navigation split view (sidebar + content)
        self.split_view = Adw.NavigationSplitView()
        self.split_view.set_vexpand(True)
        main_box.append(self.split_view)

        # === SIDEBAR ===
        sidebar_page = Adw.NavigationPage()
        sidebar_page.set_title("Library")

        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Sidebar header
        sidebar_header = Adw.HeaderBar()
        sidebar_header.add_css_class("flat")
        sidebar_box.append(sidebar_header)

        # Search bar (hidden by default)
        self.search_bar = Gtk.SearchBar()
        self.search_bar.set_show_close_button(True)

        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        search_box.set_margin_start(6)
        search_box.set_margin_end(6)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Søg i filer, kode, detaljer...")
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self._on_search_changed)
        self.search_entry.connect("activate", self._on_search_activate)
        search_box.append(self.search_entry)

        self.search_bar.set_child(search_box)
        self.search_bar.connect_entry(self.search_entry)
        sidebar_box.append(self.search_bar)

        # Search results container (hidden by default)
        self.search_results_scroll = Gtk.ScrolledWindow()
        self.search_results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.search_results_scroll.set_vexpand(True)
        self.search_results_scroll.set_visible(False)

        self.search_results_list = Gtk.ListBox()
        self.search_results_list.add_css_class("boxed-list")
        self.search_results_list.connect("row-activated", self._on_search_result_activated)
        self.search_results_scroll.set_child(self.search_results_list)
        sidebar_box.append(self.search_results_scroll)

        # Scrollable list (regular sejr list)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)

        self.sejr_list = Gtk.ListBox()
        self.sejr_list.add_css_class("navigation-sidebar")
        self.sejr_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.sejr_list.connect("row-activated", self._on_sejr_selected)
        scroll.set_child(self.sejr_list)

        sidebar_box.append(scroll)

        # Stats at bottom of sidebar
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

        # === CONTENT AREA ===
        content_page = Adw.NavigationPage()
        content_page.set_title("Details")

        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        # Welcome page (when no sejr selected)
        welcome = self._build_welcome_page()
        self.content_stack.add_named(welcome, "welcome")

        # Detail page (when sejr selected)
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

    def _build_welcome_page(self):
        """Build the welcome/empty state page with live stats"""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        main_box.set_valign(Gtk.Align.CENTER)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_margin_top(48)
        main_box.set_margin_bottom(48)

        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        header_box.set_halign(Gtk.Align.CENTER)

        icon = Gtk.Image.new_from_icon_name("starred-symbolic")
        icon.set_pixel_size(64)
        icon.add_css_class("accent")
        header_box.append(icon)

        title = Gtk.Label(label="Sejrliste Mesterværk")
        title.add_css_class("title-1")
        header_box.append(title)

        subtitle = Gtk.Label(label="Din vej til Admiral niveau")
        subtitle.add_css_class("dim-label")
        header_box.append(subtitle)

        main_box.append(header_box)

        # Stats cards
        stats = get_system_stats()
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        stats_box.set_halign(Gtk.Align.CENTER)

        stat_items = [
            ("🎯", str(stats["total_sejrs"]), "Total Sejrs"),
            ("✅", str(stats["archived"]), "Arkiveret"),
            ("🏅", str(stats["grand_admirals"]), "Grand Admirals"),
            ("📊", f"{stats['completed_checkboxes']}/{stats['total_checkboxes']}", "Checkboxes"),
        ]

        for emoji, value, label in stat_items:
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            card.add_css_class("card")
            card.set_size_request(100, 80)

            emoji_label = Gtk.Label(label=emoji)
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

        # Progress to Grand Admiral
        if stats["total_sejrs"] > 0:
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

        new_btn = Gtk.Button(label="🚀 Opret Ny Sejr")
        new_btn.add_css_class("suggested-action")
        new_btn.add_css_class("pill")
        new_btn.connect("clicked", self._on_new_sejr)
        buttons_box.append(new_btn)

        open_btn = Gtk.Button(label="📁 Åbn Mappe")
        open_btn.add_css_class("pill")
        open_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", str(SYSTEM_PATH)]))
        buttons_box.append(open_btn)

        main_box.append(buttons_box)

        # Tip
        tip_label = Gtk.Label(label="💡 Tip: Brug Ctrl+N for hurtig ny sejr")
        tip_label.add_css_class("caption")
        tip_label.add_css_class("dim-label")
        main_box.append(tip_label)

        return main_box

    def _build_detail_page(self, sejr):
        """Build the detail view for a sejr"""
        # Clear existing
        while child := self.detail_box.get_first_child():
            self.detail_box.remove(child)

        # Header with title
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        icon = Gtk.Image.new_from_icon_name(
            "emblem-ok-symbolic" if sejr["is_archived"] else "folder-open-symbolic"
        )
        icon.set_pixel_size(48)
        if sejr["is_archived"]:
            icon.add_css_class("success")
        header_box.append(icon)

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title_box.set_hexpand(True)

        title = Gtk.Label(label=sejr["display_name"])
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-1")
        title_box.append(title)

        subtitle = Gtk.Label(label=f"Pass {sejr['current_pass']}/3 • {sejr['date']}")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("dim-label")
        title_box.append(subtitle)

        header_box.append(title_box)

        # Open folder button
        open_btn = Gtk.Button(icon_name="folder-open-symbolic")
        open_btn.set_tooltip_text("Åbn i Files")
        open_btn.set_valign(Gtk.Align.CENTER)
        open_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", sejr["path"]]))
        header_box.append(open_btn)

        self.detail_box.append(header_box)

        # Progress section
        progress_group = Adw.PreferencesGroup()
        progress_group.set_title("Progress")

        # Main progress bar
        progress_row = Adw.ActionRow()
        progress_row.set_title(f"Samlet fremdrift: {sejr['progress']}%")
        progress_row.set_subtitle(f"{sejr['done']}/{sejr['total']} checkboxes afkrydset")

        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(sejr["progress"] / 100)
        progress_bar.set_valign(Gtk.Align.CENTER)
        progress_bar.set_size_request(200, -1)
        if sejr["progress"] >= 80:
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
            if i <= int(sejr["current_pass"]):
                badge.add_css_class("success")
            else:
                badge.add_css_class("dim-label")
            badge.set_size_request(24, 24)
            passes_box.append(badge)

        passes_row.add_suffix(passes_box)
        progress_group.add(passes_row)

        self.detail_box.append(progress_group)

        # DNA Layers section
        dna_group = Adw.PreferencesGroup()
        dna_group.set_title("7 DNA Lag")
        dna_group.set_description("Systemets selvbevidsthed og automatisering")

        dna_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        dna_box.add_css_class("card")

        for i, (num, name, desc, icon) in enumerate(DNA_LAYERS):
            # Random active status for demo (in real version, check from STATUS.yaml)
            active = sejr["progress"] > (i * 12)
            row = DNALayerRow(num, name, desc, icon, active)
            dna_box.append(row)

            if i < len(DNA_LAYERS) - 1:
                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                dna_box.append(sep)

        dna_group.add(dna_box)
        self.detail_box.append(dna_group)

        # Quick Actions section
        quick_group = Adw.PreferencesGroup()
        quick_group.set_title("Hurtig Navigation")

        quick_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        quick_box.set_halign(Gtk.Align.START)
        quick_box.set_margin_top(8)
        quick_box.set_margin_bottom(8)

        # Open folder button
        folder_btn = Gtk.Button(label="📁 Åbn Mappe")
        folder_btn.add_css_class("pill")
        folder_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", sejr["path"]]))
        quick_box.append(folder_btn)

        # Open SEJR_LISTE.md
        sejr_file = Path(sejr["path"]) / "SEJR_LISTE.md"
        if sejr_file.exists():
            edit_btn = Gtk.Button(label="📝 Rediger Sejr")
            edit_btn.add_css_class("pill")
            edit_btn.connect("clicked", lambda b: subprocess.Popen(["xdg-open", str(sejr_file)]))
            quick_box.append(edit_btn)

        # Open terminal in folder
        term_btn = Gtk.Button(label="💻 Terminal")
        term_btn.add_css_class("pill")
        term_btn.connect("clicked", lambda b: subprocess.Popen(
            ["gnome-terminal", f"--working-directory={sejr['path']}"]
        ))
        quick_box.append(term_btn)

        quick_group.add(quick_box)
        self.detail_box.append(quick_group)

        # Files section
        files_group = Adw.PreferencesGroup()
        files_group.set_title("Filer")
        files_group.set_description(f"{len(sejr['files'])} filer - klik for at åbne")

        for filename in sejr["files"][:10]:
            icon_name = "text-x-generic-symbolic"
            if filename.endswith(".md"):
                icon_name = "text-x-markdown-symbolic"
            elif filename.endswith(".yaml"):
                icon_name = "text-x-script-symbolic"
            elif filename.endswith(".jsonl"):
                icon_name = "text-x-log-symbolic"

            file_row = Adw.ActionRow()
            file_row.set_title(filename)
            file_row.add_prefix(Gtk.Image.new_from_icon_name(icon_name))
            file_row.set_activatable(True)

            # Store file path for click handler
            file_path = Path(sejr["path"]) / filename
            file_row.connect("activated", lambda r, fp=file_path: subprocess.Popen(["xdg-open", str(fp)]))

            # Add open button
            open_icon = Gtk.Image.new_from_icon_name("document-open-symbolic")
            file_row.add_suffix(open_icon)

            files_group.add(file_row)

        self.detail_box.append(files_group)

        # Actions section
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

        # Chat Stream section - MESSENGER STYLE!
        chat_group = Adw.PreferencesGroup()
        chat_group.set_title("💬 Activity Stream")
        chat_group.set_description("Live samtale om hvad der sker")

        chat_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        chat_card.add_css_class("card")

        self.chat_stream = ChatStream(Path(sejr["path"]))
        chat_card.append(self.chat_stream)

        chat_group.add(chat_card)
        self.detail_box.append(chat_group)

    def _load_sejrs(self):
        """Load all sejrs into the sidebar"""
        self.sejrs = get_all_sejrs()

        # Clear list
        while row := self.sejr_list.get_first_child():
            self.sejr_list.remove(row)

        active_count = 0
        archived_count = 0

        # Active section header
        active_header = Gtk.Label(label="AKTIVE")
        active_header.add_css_class("caption")
        active_header.add_css_class("dim-label")
        active_header.set_halign(Gtk.Align.START)
        active_header.set_margin_start(12)
        active_header.set_margin_top(12)
        active_header.set_margin_bottom(6)
        self.sejr_list.append(active_header)

        for sejr in self.sejrs:
            if not sejr["is_archived"]:
                row = SejrRow(sejr)
                self.sejr_list.append(row)
                active_count += 1

        if active_count == 0:
            empty = Gtk.Label(label="Ingen aktive sejrs")
            empty.add_css_class("dim-label")
            empty.set_margin_start(12)
            empty.set_margin_bottom(12)
            self.sejr_list.append(empty)

        # Archived section header
        archive_header = Gtk.Label(label="ARKIVEREDE")
        archive_header.add_css_class("caption")
        archive_header.add_css_class("dim-label")
        archive_header.set_halign(Gtk.Align.START)
        archive_header.set_margin_start(12)
        archive_header.set_margin_top(18)
        archive_header.set_margin_bottom(6)
        self.sejr_list.append(archive_header)

        for sejr in self.sejrs:
            if sejr["is_archived"]:
                row = SejrRow(sejr)
                self.sejr_list.append(row)
                archived_count += 1

        if archived_count == 0:
            empty = Gtk.Label(label="Ingen arkiverede sejrs")
            empty.add_css_class("dim-label")
            empty.set_margin_start(12)
            empty.set_margin_bottom(12)
            self.sejr_list.append(empty)

        # Update stats
        self.active_label.set_label(f"{active_count} Active")
        self.archived_label.set_label(f"{archived_count} Archived")

        return True  # For timeout

    def _on_sejr_selected(self, listbox, row):
        """Handle sejr selection"""
        if hasattr(row, 'sejr_info'):
            self.selected_sejr = row.sejr_info
            self._build_detail_page(row.sejr_info)
            self.content_stack.set_visible_child_name("detail")
            self.split_view.set_show_content(True)

    def _on_new_sejr(self, button):
        """Create a new sejr with dialog for name input"""
        # Create dialog
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="Opret Ny Sejr",
            body="Indtast navn på din nye sejr:"
        )

        # Add entry
        entry = Gtk.Entry()
        entry.set_placeholder_text("F.eks. MIN_FEATURE")
        entry.set_margin_start(20)
        entry.set_margin_end(20)
        entry.set_margin_bottom(10)
        dialog.set_extra_child(entry)

        dialog.add_response("cancel", "Annuller")
        dialog.add_response("create", "Opret")
        dialog.set_response_appearance("create", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("create")
        dialog.set_close_response("cancel")

        def on_response(dialog, response):
            if response == "create":
                name = entry.get_text().strip()
                if name:
                    # Replace spaces with underscores
                    name = name.replace(" ", "_").upper()
                    self._create_sejr(name)
            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.present()

    def _on_convert_to_sejr(self, button):
        """Open universal converter dialog - 5W KONTROL"""
        dialog = Adw.Window(transient_for=self)
        dialog.set_title("🔄 Universal Sejr Converter")
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
        title_label = Gtk.Label(label="Konverter ALT til SEJR Struktur")
        title_label.add_css_class("title-1")
        content_box.append(title_label)

        subtitle_label = Gtk.Label(label="Vælg input type, kontrol mode, og definer 5W")
        subtitle_label.add_css_class("dim-label")
        content_box.append(subtitle_label)

        # === INPUT TYPE SELECTION ===
        input_group = Adw.PreferencesGroup()
        input_group.set_title("📥 INPUT TYPE")
        input_group.set_description("Hvad vil du konvertere?")

        self.convert_input_type = Gtk.ComboBoxText()
        for key, label in SejrConverter.INPUT_TYPES.items():
            self.convert_input_type.append(key, label)
        self.convert_input_type.set_active_id("folder")

        input_row = Adw.ActionRow()
        input_row.set_title("Type")
        input_row.add_suffix(self.convert_input_type)
        input_group.add(input_row)

        # Input path/text
        self.convert_input_entry = Gtk.Entry()
        self.convert_input_entry.set_placeholder_text("/sti/til/mappe/eller/fil")
        self.convert_input_entry.set_hexpand(True)

        path_row = Adw.ActionRow()
        path_row.set_title("Kilde")
        path_row.set_subtitle("Sti til mappe/fil, eller indtast tekst")
        path_row.add_suffix(self.convert_input_entry)

        browse_btn = Gtk.Button(icon_name="folder-open-symbolic")
        browse_btn.set_valign(Gtk.Align.CENTER)
        browse_btn.connect("clicked", lambda b: self._browse_for_input())
        path_row.add_suffix(browse_btn)

        input_group.add(path_row)
        content_box.append(input_group)

        # === CONTROL MODE SELECTION ===
        mode_group = Adw.PreferencesGroup()
        mode_group.set_title("🎛️ KONTROL MODE")
        mode_group.set_description("Hvordan vil du styre processen?")

        self.convert_mode = Gtk.ComboBoxText()
        for key, label in SejrConverter.CONTROL_MODES.items():
            self.convert_mode.append(key, label)
        self.convert_mode.set_active_id("manual")

        mode_row = Adw.ActionRow()
        mode_row.set_title("Mode")
        mode_row.add_suffix(self.convert_mode)
        mode_group.add(mode_row)
        content_box.append(mode_group)

        # === 5W KONTROL ===
        w5_group = Adw.PreferencesGroup()
        w5_group.set_title("🎯 5W KONTROL")
        w5_group.set_description("Du har TOTAL KONTROL over alt")

        # HVAD
        self.convert_hvad = Gtk.Entry()
        self.convert_hvad.set_placeholder_text("Hvad skal konverteres/bygges?")
        hvad_row = Adw.ActionRow()
        hvad_row.set_title("HVAD")
        hvad_row.set_subtitle("Beskrivelse af opgaven")
        hvad_row.add_suffix(self.convert_hvad)
        w5_group.add(hvad_row)

        # HVORFOR
        self.convert_hvorfor = Gtk.Entry()
        self.convert_hvorfor.set_placeholder_text("Formål med denne sejr")
        hvorfor_row = Adw.ActionRow()
        hvorfor_row.set_title("HVORFOR")
        hvorfor_row.set_subtitle("Formålet/værdien")
        hvorfor_row.add_suffix(self.convert_hvorfor)
        w5_group.add(hvorfor_row)

        # HVORDAN
        self.convert_hvordan = Gtk.Entry()
        self.convert_hvordan.set_placeholder_text("3-pass system")
        hvordan_row = Adw.ActionRow()
        hvordan_row.set_title("HVORDAN")
        hvordan_row.set_subtitle("Tilgangen/metoden")
        hvordan_row.add_suffix(self.convert_hvordan)
        w5_group.add(hvordan_row)

        # HVORNÅR
        self.convert_hvornaar = Gtk.Entry()
        self.convert_hvornaar.set_placeholder_text("Nu → Færdig")
        hvornaar_row = Adw.ActionRow()
        hvornaar_row.set_title("HVORNÅR")
        hvornaar_row.set_subtitle("Timeline/deadline")
        hvornaar_row.add_suffix(self.convert_hvornaar)
        w5_group.add(hvornaar_row)

        content_box.append(w5_group)

        # === SEJR NAME ===
        name_group = Adw.PreferencesGroup()
        name_group.set_title("📛 SEJR NAVN")

        self.convert_name = Gtk.Entry()
        self.convert_name.set_placeholder_text("PROJEKT_NAVN")
        name_row = Adw.ActionRow()
        name_row.set_title("Navn")
        name_row.set_subtitle("Navn på den nye sejr (VERSALER)")
        name_row.add_suffix(self.convert_name)
        name_group.add(name_row)
        content_box.append(name_group)

        scroll.set_child(content_box)
        main_box.append(scroll)

        # Bottom action bar
        action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        action_bar.set_margin_start(24)
        action_bar.set_margin_end(24)
        action_bar.set_margin_top(16)
        action_bar.set_margin_bottom(16)
        action_bar.set_halign(Gtk.Align.END)

        cancel_btn = Gtk.Button(label="Annuller")
        cancel_btn.connect("clicked", lambda b: dialog.close())
        action_bar.append(cancel_btn)

        create_btn = Gtk.Button(label="🚀 Opret Sejr")
        create_btn.add_css_class("suggested-action")
        create_btn.connect("clicked", lambda b: self._execute_conversion(dialog))
        action_bar.append(create_btn)

        main_box.append(action_bar)

        dialog.present()

    def _browse_for_input(self):
        """Open file chooser for input selection"""
        # Use Nautilus to let user copy path
        subprocess.Popen(["nautilus", str(SYSTEM_PATH)])
        send_notification("📁 File Browser", "Kopiér stien til det du vil konvertere")

    def _execute_conversion(self, dialog):
        """Execute the conversion based on dialog inputs"""
        converter = SejrConverter(SYSTEM_PATH)

        config = {
            "name": self.convert_name.get_text().strip().upper().replace(" ", "_") or "NY_SEJR",
            "input_path": self.convert_input_entry.get_text().strip(),
            "input_type": self.convert_input_type.get_active_id(),
            "mode": self.convert_mode.get_active_id(),
            "hvad": self.convert_hvad.get_text().strip(),
            "hvorfor": self.convert_hvorfor.get_text().strip(),
            "hvordan": self.convert_hvordan.get_text().strip() or "3-pass system",
            "hvornaar": self.convert_hvornaar.get_text().strip() or "Nu → Færdig",
            "tasks": [],
        }

        # Analyze input and get suggested tasks
        if config["input_path"]:
            analysis = converter.analyze_input(config["input_path"], config["input_type"])
            config["tasks"] = analysis.get("suggested_tasks", [])

            # Use suggested name if not provided
            if config["name"] == "NY_SEJR" and analysis.get("suggested_name"):
                config["name"] = analysis["suggested_name"]

        # Add default tasks if none detected
        if not config["tasks"]:
            config["tasks"] = [
                "Analysér input",
                "Planlæg struktur",
                "Implementér løsning",
                "Verificér resultat",
                "Dokumentér",
            ]

        # Create the sejr
        sejr_path = converter.create_sejr_from_input(config)

        # Close dialog
        dialog.close()

        # Reload and show the new sejr
        self._load_sejrs()

        # Find and display the new sejr
        for sejr in self.sejrs:
            if config["name"] in sejr["name"]:
                self.selected_sejr = sejr
                self._build_detail_page(sejr)
                self.content_stack.set_visible_child_name("detail")
                self.split_view.set_show_content(True)

                # Open in Nautilus
                subprocess.Popen(["nautilus", str(sejr_path)])

                # Send notification
                send_notification(
                    "✅ Sejr Oprettet!",
                    f"{config['name']} er klar med 5W kontrol"
                )

                # Add to chat stream if available
                if hasattr(self, 'chat_stream') and self.chat_stream:
                    self.chat_stream.add_message(
                        sender="System",
                        content=f"Ny sejr oprettet: {config['name']}",
                        msg_type="info",
                        file_link=str(sejr_path / "SEJR_LISTE.md")
                    )
                break

    def _create_sejr(self, name):
        """Actually create the sejr"""
        script_path = SCRIPTS_DIR / "generate_sejr.py"
        if script_path.exists():
            try:
                result = subprocess.run(
                    ["python3", str(script_path), "--name", name],
                    cwd=str(SYSTEM_PATH),
                    capture_output=True,
                    text=True
                )
                self._load_sejrs()

                # Find and select the new sejr
                for sejr in self.sejrs:
                    if name in sejr["name"]:
                        self._build_detail_page(sejr)
                        self.content_stack.set_visible_child_name("detail")
                        self.split_view.set_show_content(True)
                        # Open in Nautilus too
                        subprocess.Popen(["nautilus", sejr["path"]])
                        break
            except Exception as e:
                print(f"Error: {e}")

    def _run_script(self, script_name):
        """Run a DNA layer script with notifications and chat updates"""
        script_path = SCRIPTS_DIR / script_name

        # Script metadata for chat
        script_info = {
            "auto_verify.py": {
                "sender": "Verify",
                "start_msg": "Kører verification...",
                "success_msg": "✅ Alle tests passed!",
                "title": "✅ Verification",
                "body": "Sejr verificeret!"
            },
            "auto_learn.py": {
                "sender": "DNA",
                "start_msg": "Analyserer patterns...",
                "success_msg": "🧠 Nye patterns lært og gemt!",
                "title": "🧠 Patterns",
                "body": "Nye patterns lært!"
            },
            "auto_predict.py": {
                "sender": "Kv1nt",
                "start_msg": "Genererer forudsigelser...",
                "success_msg": "🔮 Næste skridt beregnet!",
                "title": "🔮 Predictions",
                "body": "Forudsigelser genereret!"
            },
            "auto_archive.py": {
                "sender": "Admiral",
                "start_msg": "Arkiverer sejr...",
                "success_msg": "🏆 SEJR ARKIVERET! Du er fantastisk!",
                "title": "🏆 Arkiveret",
                "body": "Sejr arkiveret med succes!"
            },
        }

        info = script_info.get(script_name, {
            "sender": "System",
            "start_msg": f"Kører {script_name}...",
            "success_msg": "Script færdig",
            "title": "Script",
            "body": "Færdig"
        })

        # Add starting message to chat
        if hasattr(self, 'chat_stream') and self.chat_stream:
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
                self._load_sejrs()

                # Add success message to chat
                if hasattr(self, 'chat_stream') and self.chat_stream:
                    # Check if there was output
                    output = result.stdout.strip() if result.stdout else info["success_msg"]
                    if len(output) > 200:
                        output = output[:200] + "..."

                    self.chat_stream.add_message(
                        sender=info["sender"],
                        content=output if output else info["success_msg"],
                        msg_type="info",
                        verification={"passed": result.returncode == 0, "message": "Verified" if result.returncode == 0 else "Fejl"}
                    )

                # Send desktop notification
                send_notification(info["title"], info["body"])

                # Special celebration for archive
                if script_name == "auto_archive.py":
                    self._show_celebration()

            except Exception as e:
                # Add error to chat
                if hasattr(self, 'chat_stream') and self.chat_stream:
                    self.chat_stream.add_message(
                        sender="Error",
                        content=f"Script fejlede: {e}",
                        msg_type="error",
                        verification={"passed": False, "message": str(e)}
                    )
                send_notification("❌ Fejl", f"Script fejlede: {e}")
                print(f"Error: {e}")

    def _show_celebration(self):
        """Show celebration dialog when sejr is archived"""
        stats = get_system_stats()

        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="🏆 SEJR ARKIVERET!",
            body=f"""Tillykke! Din sejr er nu arkiveret.

📊 System Status:
• Total sejrs: {stats['total_sejrs']}
• Aktive: {stats['active']}
• Arkiverede: {stats['archived']}
• Grand Admirals: {stats['grand_admirals']} 🏅

Du er på vej mod Admiral niveau!"""
        )

        dialog.add_response("ok", "Fantastisk! 🎉")
        dialog.set_default_response("ok")
        dialog.present()

    def _open_current_folder(self):
        """Open current sejr folder in Nautilus"""
        if self.selected_sejr:
            subprocess.Popen(["nautilus", self.selected_sejr["path"]])
        else:
            subprocess.Popen(["nautilus", str(SYSTEM_PATH)])

    def _auto_refresh(self):
        """Auto-refresh every 5 seconds"""
        self._load_sejrs()
        if self.selected_sejr:
            # Refresh current view
            for sejr in self.sejrs:
                if sejr["path"] == self.selected_sejr["path"]:
                    self._build_detail_page(sejr)
                    break
        return True

    # ═══════════════════════════════════════════════════════════════════════════
    # INTELLIGENT SEARCH HANDLERS
    # ═══════════════════════════════════════════════════════════════════════════

    def _on_search_toggled(self, button):
        """Toggle search mode on/off"""
        self.search_mode = button.get_active()
        self.search_bar.set_search_mode(self.search_mode)

        if self.search_mode:
            # Show search results, hide regular list
            self.search_results_scroll.set_visible(True)
            self.search_entry.grab_focus()
        else:
            # Hide search results, show regular list
            self.search_results_scroll.set_visible(False)
            self._clear_search_results()
            self.search_entry.set_text("")

    def _on_search_changed(self, entry):
        """Handle live search as user types"""
        query = entry.get_text().strip()

        if len(query) < 2:
            self._clear_search_results()
            return

        # Perform search
        results = self.search_engine.search(query, max_results=30)
        self._display_search_results(results, query)

    def _on_search_activate(self, entry):
        """Handle Enter press in search - perform full search"""
        query = entry.get_text().strip()

        if len(query) < 2:
            return

        results = self.search_engine.search(query, max_results=50)
        self._display_search_results(results, query)

    def _clear_search_results(self):
        """Clear all search result rows"""
        while row := self.search_results_list.get_first_child():
            self.search_results_list.remove(row)

    def _display_search_results(self, results, query):
        """Display search results in the list"""
        self._clear_search_results()

        if not results:
            # Show no results message
            empty_row = Adw.ActionRow()
            empty_row.set_title("Ingen resultater")
            empty_row.set_subtitle(f'Ingen match for "{query}"')
            empty_row.add_prefix(Gtk.Image.new_from_icon_name("dialog-question-symbolic"))
            self.search_results_list.append(empty_row)
            return

        # Add header showing result count
        header = Gtk.Label(label=f"RESULTATER ({len(results)})")
        header.add_css_class("caption")
        header.add_css_class("dim-label")
        header.set_halign(Gtk.Align.START)
        header.set_margin_start(12)
        header.set_margin_top(12)
        header.set_margin_bottom(6)
        self.search_results_list.append(header)

        # Group by sejr
        current_sejr = None

        for result in results:
            # Add sejr separator if new sejr
            if result["sejr"] != current_sejr:
                current_sejr = result["sejr"]
                sejr_header = Gtk.Label(label=current_sejr.split("_2026")[0].replace("_", " "))
                sejr_header.add_css_class("heading")
                sejr_header.set_halign(Gtk.Align.START)
                sejr_header.set_margin_start(12)
                sejr_header.set_margin_top(8)
                sejr_header.set_margin_bottom(4)
                self.search_results_list.append(sejr_header)

            # Create result row
            row = Adw.ActionRow()
            row.result_data = result  # Store data for click handler

            # Icon based on match type
            icon_name = {
                "folder": "folder-symbolic",
                "filename": "text-x-generic-symbolic",
                "content": "format-text-rich-symbolic",
                "log": "text-x-log-symbolic"
            }.get(result["match_type"], "text-x-generic-symbolic")

            row.add_prefix(Gtk.Image.new_from_icon_name(icon_name))

            # Title with highlighted match
            title = result["context"][:80]
            if len(result["context"]) > 80:
                title += "..."
            row.set_title(title)

            # Subtitle with file info
            if result["line_num"] > 0:
                row.set_subtitle(f'{result["file"]} : linje {result["line_num"]}')
            else:
                row.set_subtitle(result["file"])

            # Type badge
            type_badge = Gtk.Label(label=result["match_type"].upper())
            type_badge.add_css_class("caption")
            type_badge.add_css_class("dim-label")
            row.add_suffix(type_badge)

            row.set_activatable(True)
            self.search_results_list.append(row)

    def _on_search_result_activated(self, listbox, row):
        """Handle click on a search result"""
        if not hasattr(row, 'result_data'):
            return

        result = row.result_data

        # Find the sejr folder path
        sejr_path = None

        # Check active
        active_path = ACTIVE_DIR / result["sejr"]
        if active_path.exists():
            sejr_path = active_path

        # Check archive
        if not sejr_path:
            archive_path = ARCHIVE_DIR / result["sejr"]
            if archive_path.exists():
                sejr_path = archive_path

        if not sejr_path:
            return

        # Get full sejr info and display it
        sejr_info = get_sejr_info(sejr_path)
        self.selected_sejr = sejr_info
        self._build_detail_page(sejr_info)
        self.content_stack.set_visible_child_name("detail")
        self.split_view.set_show_content(True)

        # If it's a file match, open the file
        if result["match_type"] in ["content", "filename", "log"]:
            file_path = sejr_path / result["file"]
            if file_path.exists():
                # Open in default text editor
                try:
                    subprocess.Popen(["xdg-open", str(file_path)])
                except Exception as e:
                    print(f"Kunne ikke åbne fil: {e}")

        # Close search mode
        self.search_btn.set_active(False)


# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

class MasterpieceApp(Adw.Application):
    """The main application"""

    def __init__(self):
        super().__init__(
            application_id="dk.cirkelline.sejrliste.masterpiece",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        # Force dark mode for modern look
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def do_activate(self):
        """Activate the application"""
        # Load modern 2026 CSS styling
        load_custom_css()

        win = MasterpieceWindow(self)

        # Add keyboard shortcuts
        self._setup_shortcuts(win)

        win.present()

    def _setup_shortcuts(self, win):
        """Setup keyboard shortcuts"""
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
        refresh_action.connect("activate", lambda a, p: win._load_sejrs())
        self.add_action(refresh_action)
        self.set_accels_for_action("app.refresh", ["<Control>r"])

        # Ctrl+O for open folder
        open_action = Gio.SimpleAction.new("open-folder", None)
        open_action.connect("activate", lambda a, p: win._open_current_folder())
        self.add_action(open_action)
        self.set_accels_for_action("app.open-folder", ["<Control>o"])

        # Ctrl+N for new sejr
        new_action = Gio.SimpleAction.new("new-sejr", None)
        new_action.connect("activate", lambda a, p: win._on_new_sejr(None))
        self.add_action(new_action)
        self.set_accels_for_action("app.new-sejr", ["<Control>n"])


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = MasterpieceApp()
    app.run(None)
