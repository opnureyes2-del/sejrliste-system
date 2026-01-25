#!/usr/bin/env python3
"""
Sejrliste Visual App - Main TUI Application
Built with Textual framework

Hotkeys:
  n - New sejr
  v - Verify current
  a - Archive (if ready)
  p - Generate predictions
  r - Refresh all
  q - Quit
"""

import json
import re
from pathlib import Path
from datetime import datetime

# Import our executor and dna_status modules
try:
    from app.executor import ScriptExecutor, get_executor
    from app.widgets.dna_status import DNAStatusWidget, DNA_LAGS
    EXECUTOR_AVAILABLE = True
except ImportError:
    EXECUTOR_AVAILABLE = False

# FASE 3: Import AI Model Handler
try:
    from app.models import ModelHandler, ModelResponse, ModelConfig
    MODEL_HANDLER_AVAILABLE = True
except ImportError:
    MODEL_HANDLER_AVAILABLE = False

# FASE 4: Import Visual Polish
try:
    from app.widgets.visual_polish import (
        Colors, StatusIndicator, SessionTimer, StatisticsView,
        ProgressAnimation, Theme, RankDisplay, VisualPolishWidget
    )
    VISUAL_POLISH_AVAILABLE = True
except ImportError:
    VISUAL_POLISH_AVAILABLE = False

# FASE 5: Import Integrations
try:
    from app.integrations import ContextSync, GitIntegration, TodoSync
    INTEGRATIONS_AVAILABLE = True
except ImportError:
    INTEGRATIONS_AVAILABLE = False

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
    from textual.widgets import Header, Footer, Static, ProgressBar, Label, ListView, ListItem, Button
    from textual.reactive import reactive
    from textual.binding import Binding
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    print("Textual not installed. Run: pip install textual")


# ============================================================================
# YAML PARSER (No external dependencies)
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
                    elif value == "null":
                        value = None
                    elif value.replace(".", "").replace("-", "").isdigit():
                        value = float(value) if "." in value else int(value)
                    result[key] = value
    except:
        pass
    return result


def count_checkboxes(content: str) -> tuple:
    """Count checkboxes in content. Returns (checked, total)."""
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked


# ============================================================================
# DATA LOADERS
# ============================================================================

class SejrData:
    """Load and manage sejrliste data."""

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.active_dir = system_path / "10_ACTIVE"
        self.archive_dir = system_path / "90_ARCHIVE"
        self.current_dir = system_path / "_CURRENT"

    def get_active_sejr(self) -> list:
        """Get all active sejr with their status."""
        if not self.active_dir.exists():
            return []

        sejr_list = []
        for folder in self.active_dir.iterdir():
            if not folder.is_dir() or folder.name.startswith('.'):
                continue

            status_file = folder / "STATUS.yaml"
            sejr_file = folder / "SEJR_LISTE.md"

            status = parse_yaml_simple(status_file) if status_file.exists() else {}

            # Count checkboxes
            if sejr_file.exists():
                content = sejr_file.read_text(encoding="utf-8")
                done, total = count_checkboxes(content)
            else:
                done, total = 0, 0

            sejr_list.append({
                "name": folder.name,
                "path": folder,
                "current_pass": status.get("current_pass", 1),
                "can_archive": status.get("can_archive", False),
                "checkboxes_done": done,
                "checkboxes_total": total,
                "total_score": status.get("score", 0),
                "rank": status.get("rank", "KADET"),
            })

        return sejr_list

    def get_archived_count(self) -> int:
        """Count archived sejr."""
        if not self.archive_dir.exists():
            return 0
        return len([d for d in self.archive_dir.iterdir() if d.is_dir()])

    def get_patterns(self) -> list:
        """Get learned patterns from PATTERNS.yaml."""
        patterns_file = self.current_dir / "PATTERNS.yaml"
        if not patterns_file.exists():
            return []

        data = parse_yaml_simple(patterns_file)
        return data.get("patterns", [])

    def get_predictions(self) -> str:
        """Get predictions from NEXT.md."""
        next_file = self.current_dir / "NEXT.md"
        if not next_file.exists():
            return "No predictions yet"

        content = next_file.read_text(encoding="utf-8")
        # Return first 500 chars
        return content[:500] + "..." if len(content) > 500 else content

    def get_recent_log(self, sejr_path: Path, limit: int = 10) -> list:
        """Get recent log entries from AUTO_LOG.jsonl."""
        log_file = sejr_path / "AUTO_LOG.jsonl"
        if not log_file.exists():
            return []

        entries = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except:
                    pass

        return entries[-limit:]


# ============================================================================
# TEXTUAL WIDGETS
# ============================================================================

if TEXTUAL_AVAILABLE:

    class StatusPanel(Static):
        """Shows overall system status."""

        def __init__(self, data: SejrData, **kwargs):
            super().__init__(**kwargs)
            self.data = data

        def compose(self) -> ComposeResult:
            yield Static(self.get_status_text(), id="status-text")

        def get_status_text(self) -> str:
            sejr_list = self.data.get_active_sejr()
            archived = self.data.get_archived_count()

            text = "═══ SEJRLISTE SYSTEM ═══\n\n"
            text += f"📂 Active: {len(sejr_list)}\n"
            text += f"📦 Archived: {archived}\n"
            text += f"🕐 Updated: {datetime.now().strftime('%H:%M:%S')}\n"

            # FASE 4: Session Timer Integration
            try:
                if self.app.session_timer:
                    elapsed = self.app.session_timer.format_elapsed()
                    text += f"⏱️ Session: {elapsed}\n"
            except:
                pass

            if sejr_list:
                sejr = sejr_list[0]
                text += f"\n─── Current Sejr ───\n"
                text += f"📋 {sejr['name'][:30]}\n"
                text += f"🔄 Pass: {sejr['current_pass']}/3\n"
                text += f"✅ Done: {sejr['checkboxes_done']}/{sejr['checkboxes_total']}\n"

                # FASE 4: Rank Display with visual indicator
                try:
                    if self.app.rank_display:
                        rank_text = self.app.rank_display.render_rank(sejr['total_score'])
                        text += f"🎖️ {rank_text}\n"
                    else:
                        text += f"🎖️ Rank: {sejr['rank']}\n"
                except:
                    text += f"🎖️ Rank: {sejr['rank']}\n"

                if sejr['can_archive']:
                    text += f"\n✅ READY TO ARCHIVE"

            # FASE 5: Integration status
            try:
                if self.app.context_sync:
                    text += f"\n\n─── Integrations ───\n"
                    text += f"📝 Context: ✓\n"
                if self.app.git_integration:
                    is_clean, msg = self.app.git_integration.verify_clean_state()
                    status = "✓" if is_clean else "⚠"
                    text += f"🔀 Git: {status}\n"
            except:
                pass

            return text

        def refresh_status(self):
            """Refresh the status display."""
            self.query_one("#status-text", Static).update(self.get_status_text())


    class SejrListPanel(Static):
        """Shows active sejr with progress."""

        def __init__(self, data: SejrData, **kwargs):
            super().__init__(**kwargs)
            self.data = data

        def compose(self) -> ComposeResult:
            yield Static(self.get_list_text(), id="sejr-list-text")

        def get_list_text(self) -> str:
            sejr_list = self.data.get_active_sejr()

            text = "═══ ACTIVE SEJR ═══\n\n"

            if not sejr_list:
                text += "(no active sejr)\n\n"
                text += "Press 'n' to create new"
                return text

            for sejr in sejr_list:
                pct = (sejr['checkboxes_done'] / sejr['checkboxes_total'] * 100) if sejr['checkboxes_total'] > 0 else 0
                bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))

                status_icon = "✅" if sejr['can_archive'] else "🔵"
                text += f"{status_icon} {sejr['name'][:25]}\n"
                text += f"   [{bar}] {pct:.0f}%\n"
                text += f"   Pass {sejr['current_pass']}/3 | Score: {sejr['total_score']}\n\n"

            return text

        def refresh_list(self):
            """Refresh the list display."""
            self.query_one("#sejr-list-text", Static).update(self.get_list_text())


    class DNAStatusPanel(Static):
        """Shows 7 DNA lag status with execution indicators."""

        def __init__(self, data: SejrData, **kwargs):
            super().__init__(**kwargs)
            self.data = data

        def compose(self) -> ComposeResult:
            yield Static(self.get_dna_text(), id="dna-text")

        def get_dna_text(self) -> str:
            text = "═══ 7 DNA LAG ═══\n\n"

            # Get the dna_widget from parent app if available
            dna_widget = None
            try:
                dna_widget = self.app.dna_widget
            except:
                pass

            dna_layers = [
                ("1", "SELF-AWARE", "DNA.yaml", None),
                ("2", "SELF-DOCUMENTING", "AUTO_LOG.jsonl", None),
                ("3", "SELF-VERIFYING", "(v) verify", "auto_verify"),
                ("4", "SELF-IMPROVING", "(l) learn", "auto_learn"),
                ("5", "SELF-ARCHIVING", "(a) archive", "auto_archive"),
                ("6", "PREDICTIVE", "(p) predict", "auto_predict"),
                ("7", "SELF-OPTIMIZING", "(n) new", "generate_sejr"),
            ]

            for num, name, component, script in dna_layers:
                # Get status indicator
                indicator = "[ ]"
                if dna_widget:
                    status = dna_widget.get_status(int(num))
                    if status == "running":
                        indicator = "[*]"
                    elif status == "complete":
                        indicator = "[OK]"
                    elif status == "error":
                        indicator = "[!]"

                text += f"{indicator} Lag {num}: {name}\n"
                text += f"       └─ {component}\n"

            return text

        def refresh_dna(self):
            """Refresh the DNA display."""
            self.query_one("#dna-text", Static).update(self.get_dna_text())


    class LogStreamPanel(Static):
        """Shows live log stream."""

        def __init__(self, data: SejrData, **kwargs):
            super().__init__(**kwargs)
            self.data = data

        def compose(self) -> ComposeResult:
            yield Static(self.get_log_text(), id="log-text")

        def get_log_text(self) -> str:
            sejr_list = self.data.get_active_sejr()

            text = "═══ AUTO_LOG STREAM ═══\n"

            if not sejr_list:
                text += "(no active sejr)"
                return text

            entries = self.data.get_recent_log(sejr_list[0]['path'], limit=5)

            for entry in entries:
                ts = entry.get('timestamp', 'unknown')[:19]
                action = entry.get('action', 'unknown')
                text += f"{ts} | {action}\n"

            if not entries:
                text += "(no log entries yet)"

            return text

        def refresh_log(self):
            """Refresh the log display."""
            self.query_one("#log-text", Static).update(self.get_log_text())


    # ========================================================================
    # MAIN APP
    # ========================================================================

    class SejrlisteApp(App):
        """Main Sejrliste Visual App."""

        CSS = """
        Screen {
            layout: grid;
            grid-size: 3 2;
            grid-gutter: 1;
        }

        .panel {
            border: solid green;
            padding: 1;
            height: 100%;
        }

        #status-panel {
            column-span: 1;
        }

        #sejr-panel {
            column-span: 1;
        }

        #dna-panel {
            column-span: 1;
        }

        #log-panel {
            column-span: 3;
            height: 8;
        }

        Header {
            background: $primary;
        }

        Footer {
            background: $primary;
        }
        """

        BINDINGS = [
            Binding("q", "quit", "Quit"),
            Binding("n", "new_sejr", "New Sejr"),
            Binding("v", "verify", "Verify"),
            Binding("a", "archive", "Archive"),
            Binding("p", "predict", "Predict"),
            Binding("l", "learn", "Learn"),
            Binding("r", "refresh", "Refresh"),
        ]

        def __init__(self, system_path: Path):
            super().__init__()
            self.system_path = system_path
            self.data = SejrData(system_path)
            self.executor = ScriptExecutor(system_path) if EXECUTOR_AVAILABLE else None
            self.dna_widget = DNAStatusWidget() if EXECUTOR_AVAILABLE else None

            # FASE 3: Model Handler for AI tasks
            self.model_handler = ModelHandler() if MODEL_HANDLER_AVAILABLE else None

            # FASE 4: Visual Polish - Session Timer & Rank Display
            self.session_timer = SessionTimer() if VISUAL_POLISH_AVAILABLE else None
            self.rank_display = RankDisplay() if VISUAL_POLISH_AVAILABLE else None
            self.theme = Theme.DEFAULT if VISUAL_POLISH_AVAILABLE else None

            # FASE 5: Integrations - Context Sync
            self.context_sync = ContextSync() if INTEGRATIONS_AVAILABLE else None
            self.todo_sync = TodoSync(system_path) if INTEGRATIONS_AVAILABLE else None
            self.git_integration = GitIntegration(system_path) if INTEGRATIONS_AVAILABLE else None

            # Start session timer
            if self.session_timer:
                self.session_timer.start()

        def compose(self) -> ComposeResult:
            yield Header(show_clock=True)
            yield StatusPanel(self.data, classes="panel", id="status-panel")
            yield SejrListPanel(self.data, classes="panel", id="sejr-panel")
            yield DNAStatusPanel(self.data, classes="panel", id="dna-panel")
            yield LogStreamPanel(self.data, classes="panel", id="log-panel")
            yield Footer()

        def action_refresh(self):
            """Refresh all panels."""
            self.query_one("#status-panel", StatusPanel).refresh_status()
            self.query_one("#sejr-panel", SejrListPanel).refresh_list()
            self.query_one("#dna-panel", DNAStatusPanel).refresh_dna()
            self.query_one("#log-panel", LogStreamPanel).refresh_log()
            self.notify("Refreshed!")

        def action_new_sejr(self):
            """Create new sejr (placeholder)."""
            self.notify("Use: python scripts/generate_sejr.py --name 'Name'")

        def action_verify(self):
            """Run verification (DNA Lag 3)."""
            self.notify("Running auto_verify.py (DNA Lag 3)...")
            if self.dna_widget:
                self.dna_widget.set_active(3)
                self.query_one("#dna-panel", DNAStatusPanel).refresh_dna()

            if self.executor:
                success, output = self.executor.run_script("auto_verify", ["--all"])
                if self.dna_widget:
                    if success:
                        self.dna_widget.set_complete(3)
                    else:
                        self.dna_widget.set_error(3)
                self.action_refresh()
                if success:
                    self.notify("Verification complete!")
                else:
                    self.notify(f"Error: {output[:100]}")
            else:
                # Fallback without executor
                import subprocess
                result = subprocess.run(
                    ["python3", str(self.system_path / "scripts" / "auto_verify.py"), "--all"],
                    capture_output=True, text=True, timeout=30
                )
                self.action_refresh()
                if result.returncode == 0:
                    self.notify("Verification complete!")
                else:
                    self.notify(f"Error: {result.stderr[:100]}")

        def action_archive(self):
            """Archive current sejr (DNA Lag 5)."""
            sejr_list = self.data.get_active_sejr()
            if not sejr_list:
                self.notify("No active sejr to archive")
                return

            sejr = sejr_list[0]
            if not sejr['can_archive']:
                self.notify("Cannot archive - 3-pass not complete")
                return

            self.notify(f"Archiving {sejr['name']} (DNA Lag 5)...")
            if self.dna_widget:
                self.dna_widget.set_active(5)
                self.query_one("#dna-panel", DNAStatusPanel).refresh_dna()

            if self.executor:
                success, output = self.executor.run_script("auto_archive", ["--sejr", sejr['name']])
                if self.dna_widget:
                    if success:
                        self.dna_widget.set_complete(5)
                    else:
                        self.dna_widget.set_error(5)
                self.action_refresh()
                if success:
                    # FASE 5: Update context on archive
                    if self.context_sync:
                        try:
                            self.context_sync.append_journal({
                                "name": sejr['name'],
                                "score": sejr['total_score'],
                                "rank": sejr['rank'],
                                "archived_at": datetime.now().isoformat()
                            })
                        except Exception as e:
                            pass  # Non-blocking
                    self.notify("Archived!")
                else:
                    self.notify(f"Error: {output[:100]}")
            else:
                import subprocess
                result = subprocess.run(
                    ["python3", str(self.system_path / "scripts" / "auto_archive.py"),
                     "--sejr", sejr['name']],
                    capture_output=True, text=True, timeout=30
                )
                self.action_refresh()
                if result.returncode == 0:
                    # FASE 5: Update context on archive
                    if self.context_sync:
                        try:
                            self.context_sync.append_journal({
                                "name": sejr['name'],
                                "score": sejr['total_score'],
                                "rank": sejr['rank'],
                                "archived_at": datetime.now().isoformat()
                            })
                        except Exception as e:
                            pass  # Non-blocking
                    self.notify("Archived!")
                else:
                    self.notify(f"Error: {result.stderr[:100]}")

        def action_predict(self):
            """Generate predictions (DNA Lag 6)."""
            self.notify("Generating predictions (DNA Lag 6)...")
            if self.dna_widget:
                self.dna_widget.set_active(6)
                self.query_one("#dna-panel", DNAStatusPanel).refresh_dna()

            if self.executor:
                success, output = self.executor.run_script("auto_predict")
                if self.dna_widget:
                    if success:
                        self.dna_widget.set_complete(6)
                    else:
                        self.dna_widget.set_error(6)
                self.action_refresh()
                if success:
                    self.notify("Predictions generated!")
                else:
                    self.notify(f"Error: {output[:100]}")
            else:
                import subprocess
                result = subprocess.run(
                    ["python3", str(self.system_path / "scripts" / "auto_predict.py")],
                    capture_output=True, text=True, timeout=30
                )
                self.action_refresh()
                if result.returncode == 0:
                    self.notify("Predictions generated!")
                else:
                    self.notify(f"Error: {result.stderr[:100]}")

        def action_learn(self):
            """Run pattern learning (DNA Lag 4)."""
            self.notify("Learning patterns (DNA Lag 4)...")
            if self.dna_widget:
                self.dna_widget.set_active(4)
                self.query_one("#dna-panel", DNAStatusPanel).refresh_dna()

            if self.executor:
                success, output = self.executor.run_script("auto_learn")
                if self.dna_widget:
                    if success:
                        self.dna_widget.set_complete(4)
                    else:
                        self.dna_widget.set_error(4)
                self.action_refresh()
                if success:
                    self.notify("Patterns learned!")
                else:
                    self.notify(f"Error: {output[:100]}")
            else:
                import subprocess
                result = subprocess.run(
                    ["python3", str(self.system_path / "scripts" / "auto_learn.py")],
                    capture_output=True, text=True, timeout=30
                )
                self.action_refresh()
                if result.returncode == 0:
                    self.notify("Patterns learned!")
                else:
                    self.notify(f"Error: {result.stderr[:100]}")


# ============================================================================
# FALLBACK: Rich-based simple view (if Textual not available)
# ============================================================================

def run_simple_view(system_path: Path):
    """Simple terminal view - NO EXTERNAL DEPENDENCIES."""
    import subprocess

    data = SejrData(system_path)

    # FASE 4: Initialize visual polish components
    session_timer = SessionTimer() if VISUAL_POLISH_AVAILABLE else None
    rank_display = RankDisplay() if VISUAL_POLISH_AVAILABLE else None
    colors = Colors if VISUAL_POLISH_AVAILABLE else None

    # FASE 5: Initialize integrations
    context_sync = ContextSync() if INTEGRATIONS_AVAILABLE else None

    if session_timer:
        session_timer.start()

    def clear_screen():
        print("\033[2J\033[H", end="")

    def print_box(title: str, content: str, width: int = 60):
        print("┌" + "─" * (width - 2) + "┐")
        print(f"│ {title.center(width - 4)} │")
        print("├" + "─" * (width - 2) + "┤")
        for line in content.split("\n"):
            print(f"│ {line[:width-4].ljust(width - 4)} │")
        print("└" + "─" * (width - 2) + "┘")

    def show_dashboard():
        clear_screen()

        # FASE 4: Use colors if available
        green = colors.GREEN if colors else ""
        yellow = colors.YELLOW if colors else ""
        blue = colors.BLUE if colors else ""
        reset = colors.RESET if colors else ""

        print(f"{green}{'=' * 70}{reset}")
        print(f"  {green}SEJRLISTE VISUAL SYSTEM{reset}".center(70 + len(green) + len(reset)))
        print(f"  Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(70))

        # FASE 4: Show session timer
        if session_timer:
            elapsed = session_timer.format_elapsed()
            print(f"  ⏱️ Session: {elapsed}".center(70))

        print(f"{green}{'=' * 70}{reset}")
        print()

        # Active Sejr
        sejr_list = data.get_active_sejr()
        archived = data.get_archived_count()

        print(f"📂 Active Sejr: {len(sejr_list)}  |  📦 Archived: {archived}")
        print("-" * 70)

        if sejr_list:
            for sejr in sejr_list:
                pct = (sejr['checkboxes_done'] / sejr['checkboxes_total'] * 100) if sejr['checkboxes_total'] > 0 else 0
                bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))

                # FASE 4: Color-coded status
                if sejr['can_archive']:
                    status = f"{green}✅ READY TO ARCHIVE{reset}"
                else:
                    status = f"{blue}🔵 Pass {sejr['current_pass']}/3{reset}"

                # FASE 4: Rank display with visual
                if rank_display:
                    rank_text = rank_display.render_rank(sejr['total_score'])
                else:
                    rank_text = f"Rank: {sejr['rank']}"

                print(f"\n📋 {sejr['name']}")
                print(f"   [{bar}] {pct:.0f}% ({sejr['checkboxes_done']}/{sejr['checkboxes_total']})")
                print(f"   {status} | {rank_text} | Score: {sejr['total_score']}")
        else:
            print("\n(No active sejr)")
            print("Press 'n' to create new sejr")

        # 7 DNA Lag
        print("\n" + "-" * 70)
        print("🧬 7 DNA LAG:")
        dna = ["SELF-AWARE", "SELF-DOCUMENTING", "SELF-VERIFYING",
               "SELF-IMPROVING", "SELF-ARCHIVING", "PREDICTIVE", "SELF-OPTIMIZING"]
        for i, name in enumerate(dna, 1):
            print(f"   [{i}] {name}")

        # FASE 5: Integration status
        if INTEGRATIONS_AVAILABLE:
            print("\n" + "-" * 70)
            print("🔗 INTEGRATIONS:")
            print(f"   📝 Context Sync: {'✓' if context_sync else '✗'}")
            print(f"   🤖 Model Handler: {'✓' if MODEL_HANDLER_AVAILABLE else '✗'}")
            print(f"   🎨 Visual Polish: {'✓' if VISUAL_POLISH_AVAILABLE else '✗'}")

        # Commands
        print("\n" + f"{green}{'=' * 70}{reset}")
        print("  [n]ew  [v]erify  [a]rchive  [p]redict  [r]efresh  [q]uit")
        print(f"{green}{'=' * 70}{reset}")

    def handle_command(cmd: str) -> bool:
        if cmd == 'q':
            return False
        elif cmd == 'r':
            pass  # Just refresh
        elif cmd == 'n':
            print("\nRun: python3 scripts/generate_sejr.py --name 'Name'")
            input("Press Enter to continue...")
        elif cmd == 'v':
            print("\nRunning verification...")
            result = subprocess.run(
                ["python3", str(system_path / "scripts" / "auto_verify.py"), "--all"],
                capture_output=True, text=True, timeout=30
            )
            print(result.stdout)
            input("Press Enter to continue...")
        elif cmd == 'a':
            sejr_list = data.get_active_sejr()
            if sejr_list and sejr_list[0]['can_archive']:
                sejr = sejr_list[0]
                print(f"\nArchiving {sejr['name']}...")
                result = subprocess.run(
                    ["python3", str(system_path / "scripts" / "auto_archive.py"),
                     "--sejr", sejr['name']],
                    capture_output=True, text=True, timeout=30
                )
                print(result.stdout)
                # FASE 5: Update context on archive
                if context_sync and result.returncode == 0:
                    try:
                        context_sync.append_journal({
                            "name": sejr['name'],
                            "score": sejr['total_score'],
                            "rank": sejr['rank'],
                            "archived_at": datetime.now().isoformat()
                        })
                        print(f"{green}✓ Journal updated{reset}")
                    except Exception as e:
                        pass
            else:
                print("\nNo sejr ready to archive (3-pass not complete)")
            input("Press Enter to continue...")
        elif cmd == 'p':
            print("\nGenerating predictions...")
            result = subprocess.run(
                ["python3", str(system_path / "scripts" / "auto_predict.py")],
                capture_output=True, text=True, timeout=30
            )
            print(result.stdout)
            input("Press Enter to continue...")

        return True

    # Main loop
    running = True
    while running:
        show_dashboard()
        try:
            cmd = input("\n> ").strip().lower()
            if cmd:
                running = handle_command(cmd)
        except KeyboardInterrupt:
            running = False
        except EOFError:
            running = False

    print("\nGoodbye!")


# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Sejrliste Visual App")
    parser.add_argument("--path", default=None, help="Path to sejrliste system")
    parser.add_argument("--simple", action="store_true", help="Use simple Rich view")
    args = parser.parse_args()

    if args.path:
        system_path = Path(args.path)
    else:
        # Default: parent of app/ folder
        system_path = Path(__file__).parent.parent

    if not system_path.exists():
        print(f"Error: System path not found: {system_path}")
        return

    print(f"Loading sejrliste from: {system_path}")

    if args.simple or not TEXTUAL_AVAILABLE:
        run_simple_view(system_path)
    else:
        app = SejrlisteApp(system_path)
        app.run()


if __name__ == "__main__":
    main()
