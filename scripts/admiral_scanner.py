#!/usr/bin/env python3
"""
ADMIRAL SCANNER — Cross-System Auto-Discovery & Morning Briefing
WHAT: Scans ALL 3 systems (Sejrliste, INTRO, ELLE) for problems, drift, and opportunities
WHY:  So Rasmus knows EXACTLY what needs attention every morning — without asking
WHO:  Runs daily via cron at 07:50 + on-demand
HOW:  python3 scripts/admiral_scanner.py [--fix] [--brief]
Version: 3.0.0
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
#  SYSTEM PATHS
# ═══════════════════════════════════════════════════════════════════════════════

SEJRLISTE_PATH = Path("/home/rasmus/Desktop/sejrliste systemet")
INTRO_PATH = Path("/home/rasmus/Desktop/MASTER FOLDERS(INTRO)")
ELLE_PATH = Path("/home/rasmus/Desktop/ELLE.md")
CONTEXT_PATH = Path("/home/rasmus/.claude/.context/core")
BRIEFING_PATH = SEJRLISTE_PATH / "_CURRENT" / "MORNING_BRIEFING.md"
SCANNER_LOG = SEJRLISTE_PATH / "_CURRENT" / "SCANNER_LOG.jsonl"

NOW = datetime.now()
STALE_DAYS = 7  # Files older than this are flagged


class Finding:
    """A single discovery from scanning."""

    def __init__(self, system: str, severity: str, category: str, message: str, file_path: str = "", fix_hint: str = ""):
        self.system = system  # SEJRLISTE / INTRO / ELLE / CONTEXT
        self.severity = severity  # CRITICAL / MEDIUM / LOW / INFO
        self.category = category  # STALE / BROKEN_REF / PARITY / DRIFT / OPPORTUNITY
        self.message = message
        self.file_path = file_path
        self.fix_hint = fix_hint
        self.timestamp = NOW.isoformat()

    def to_dict(self) -> dict:
        return {
            "system": self.system,
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "file_path": self.file_path,
            "fix_hint": self.fix_hint,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        icon = {"CRITICAL": "🔴", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "⚪"}.get(self.severity, "⚪")
        return f"{icon} [{self.system}] {self.message}"


class AdmiralScanner:
    """Cross-system scanner that finds problems before they find you."""

    def __init__(self):
        self.findings: List[Finding] = []

    def add(self, system: str, severity: str, category: str, message: str, file_path: str = "", fix_hint: str = ""):
        self.findings.append(Finding(system, severity, category, message, file_path, fix_hint))

    # ═══════════════════════════════════════════════════════════════════════════
    #  SEJRLISTE SYSTEM SCAN
    # ═══════════════════════════════════════════════════════════════════════════

    def scan_sejrliste(self):
        """Scan the Sejrliste system for issues."""
        print("\n━━━ SCANNING: SEJRLISTE SYSTEM ━━━")

        if not SEJRLISTE_PATH.exists():
            self.add("SEJRLISTE", "CRITICAL", "BROKEN_REF", "System path does not exist!", str(SEJRLISTE_PATH))
            return

        # 1. Check active victories for stale STATUS.yaml
        active_dir = SEJRLISTE_PATH / "10_ACTIVE"
        if active_dir.exists():
            for sejr_dir in sorted(active_dir.iterdir()):
                if not sejr_dir.is_dir() or sejr_dir.name.startswith('.'):
                    continue
                status_file = sejr_dir / "STATUS.yaml"
                if status_file.exists():
                    age = (NOW - datetime.fromtimestamp(status_file.stat().st_mtime)).days
                    if age > STALE_DAYS:
                        self.add("SEJRLISTE", "MEDIUM", "STALE",
                                 f"Active victory '{sejr_dir.name}' STATUS.yaml is {age} days old",
                                 str(status_file),
                                 "Consider updating or archiving this victory")
                else:
                    self.add("SEJRLISTE", "CRITICAL", "BROKEN_REF",
                             f"Active victory '{sejr_dir.name}' missing STATUS.yaml",
                             str(sejr_dir),
                             "Run: python3 scripts/auto_verify.py --all")

                # Check for missing SEJR_LISTE.md
                sejr_liste = sejr_dir / "SEJR_LISTE.md"
                if not sejr_liste.exists():
                    self.add("SEJRLISTE", "CRITICAL", "BROKEN_REF",
                             f"Active victory '{sejr_dir.name}' missing SEJR_LISTE.md",
                             str(sejr_dir))

        # 2. Check DK/EN file parity
        # web_app pair: should be same size (both simple Streamlit apps)
        # masterpiece pair: EN is PRIMARY (with INTRO integration), DK is simplified alternative
        parity_pairs = [
            ("web_app.py", "web_app_en.py", 50),        # strict parity — same features
        ]
        info_pairs = [
            ("masterpiece.py", "masterpiece_en.py"),     # EN is primary, DK is simplified
        ]
        for dk_file, en_file, threshold in parity_pairs:
            dk_path = SEJRLISTE_PATH / dk_file
            en_path = SEJRLISTE_PATH / en_file
            if dk_path.exists() and en_path.exists():
                dk_lines = len(dk_path.read_text(encoding="utf-8").splitlines())
                en_lines = len(en_path.read_text(encoding="utf-8").splitlines())
                diff = abs(dk_lines - en_lines)
                if diff > threshold:
                    self.add("SEJRLISTE", "MEDIUM", "PARITY",
                             f"{dk_file} ({dk_lines}L) vs {en_file} ({en_lines}L) — {diff} lines difference",
                             str(dk_path),
                             f"Sync features between DK and EN versions")
                else:
                    self.add("SEJRLISTE", "INFO", "PARITY",
                             f"{dk_file} ↔ {en_file} — OK ({diff}L diff)", str(dk_path))
        for dk_file, en_file in info_pairs:
            dk_path = SEJRLISTE_PATH / dk_file
            en_path = SEJRLISTE_PATH / en_file
            if dk_path.exists() and en_path.exists():
                dk_lines = len(dk_path.read_text(encoding="utf-8").splitlines())
                en_lines = len(en_path.read_text(encoding="utf-8").splitlines())
                self.add("SEJRLISTE", "INFO", "PARITY",
                         f"{dk_file} ({dk_lines}L) vs {en_file} ({en_lines}L) — EN is primary app with INTRO integration",
                         str(en_path))

        # 3. Check docs freshness
        docs_dir = SEJRLISTE_PATH / "docs"
        if docs_dir.exists():
            for doc in sorted(docs_dir.glob("*.md")):
                age = (NOW - datetime.fromtimestamp(doc.stat().st_mtime)).days
                if age > 14:
                    self.add("SEJRLISTE", "LOW", "STALE",
                             f"Doc '{doc.name}' is {age} days old",
                             str(doc),
                             "Review if content is still accurate")

        # 4. Check systemd service
        try:
            import subprocess
            result = subprocess.run(
                ["systemctl", "--user", "is-active", "sejrliste-web.service"],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip() == "active":
                self.add("SEJRLISTE", "INFO", "DRIFT", "Web service: ACTIVE")
            else:
                self.add("SEJRLISTE", "CRITICAL", "DRIFT",
                         f"Web service NOT active: {result.stdout.strip()}",
                         fix_hint="systemctl --user start sejrliste-web.service")
        except Exception as e:
            self.add("SEJRLISTE", "LOW", "DRIFT", f"Could not check service: {e}")

        # 5. Check cron jobs exist
        try:
            import subprocess
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
            cron_content = result.stdout
            expected_crons = ["auto_learn", "health_check"]
            for cron_name in expected_crons:
                if cron_name in cron_content:
                    self.add("SEJRLISTE", "INFO", "DRIFT", f"Cron '{cron_name}': PRESENT")
                else:
                    self.add("SEJRLISTE", "MEDIUM", "DRIFT",
                             f"Cron '{cron_name}' NOT found in crontab",
                             fix_hint=f"Add cron job for {cron_name}")
        except Exception as e:
            self.add("SEJRLISTE", "LOW", "DRIFT", f"Could not check cron: {e}")

        # 6. Git status check
        try:
            import subprocess
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=10,
                cwd=str(SEJRLISTE_PATH)
            )
            uncommitted = len([l for l in result.stdout.strip().splitlines() if l.strip()])
            if uncommitted > 0:
                self.add("SEJRLISTE", "LOW", "DRIFT",
                         f"{uncommitted} uncommitted changes in git",
                         fix_hint="Review and commit or discard changes")
            else:
                self.add("SEJRLISTE", "INFO", "DRIFT", "Git: clean working tree")
        except Exception as e:
            self.add("SEJRLISTE", "LOW", "DRIFT", f"Could not check git: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    #  INTRO SYSTEM SCAN
    # ═══════════════════════════════════════════════════════════════════════════

    def scan_intro(self):
        """Scan the INTRO/MASTER FOLDERS system for issues."""
        print("\n━━━ SCANNING: INTRO SYSTEM ━━━")

        if not INTRO_PATH.exists():
            self.add("INTRO", "CRITICAL", "BROKEN_REF", "INTRO path does not exist!", str(INTRO_PATH))
            return

        # 1. Check I-files staleness
        i_files = sorted(INTRO_PATH.glob("I[0-9]*.md"))
        for i_file in i_files:
            age = (NOW - datetime.fromtimestamp(i_file.stat().st_mtime)).days
            if age > 14:
                self.add("INTRO", "MEDIUM", "STALE",
                         f"I-file '{i_file.name}' is {age} days old",
                         str(i_file),
                         "Fact-check and update if needed")
            elif age > 7:
                self.add("INTRO", "LOW", "STALE",
                         f"I-file '{i_file.name}' is {age} days old",
                         str(i_file))

        # 2. Check STATUS PROJEKTS freshness
        status_dir = INTRO_PATH / "STATUS PROJEKTS"
        if status_dir.exists():
            # Find newest file in status dir (recursively)
            newest_age = 999
            newest_file = None
            for f in status_dir.rglob("*.md"):
                age = (NOW - datetime.fromtimestamp(f.stat().st_mtime)).days
                if age < newest_age:
                    newest_age = age
                    newest_file = f
            if newest_age > 7:
                self.add("INTRO", "CRITICAL", "STALE",
                         f"STATUS PROJEKTS newest file is {newest_age} days old ({newest_file.name if newest_file else 'none'})",
                         str(status_dir),
                         "Generate fresh system status")
        else:
            self.add("INTRO", "CRITICAL", "BROKEN_REF", "STATUS PROJEKTS directory missing!")

        # 3. Check empty directories
        for subdir in sorted(INTRO_PATH.iterdir()):
            if subdir.is_dir() and not subdir.name.startswith('.'):
                contents = list(subdir.iterdir())
                if len(contents) == 0:
                    self.add("INTRO", "MEDIUM", "DRIFT",
                             f"Empty directory: '{subdir.name}/'",
                             str(subdir),
                             "Add content or remove directory")

        # 4. Check for contradictory I-files (same port claimed BOTH active AND inactive)
        for i_file in i_files:
            try:
                content = i_file.read_text(encoding="utf-8")
                active_ports = set()
                inactive_ports = set()
                for line in content.splitlines():
                    port_match = re.search(r'(?:port|:)\s*(\d{4,5})', line, re.IGNORECASE)
                    if not port_match:
                        continue
                    port = port_match.group(1)
                    # Check inactive FIRST (IKKE/NOT + status keyword)
                    if re.search(r'(?:IKKE|NOT)\s+(?:AKTIV|aktive?|running|active|lytter)', line, re.IGNORECASE):
                        inactive_ports.add(port)
                    elif re.search(r'(?<![Ii]n)\b(?:AKTIV|UP|running|operational|listening)\b', line, re.IGNORECASE):
                        active_ports.add(port)
                # Only flag if the SAME port is claimed both active AND inactive
                contradicted = active_ports & inactive_ports
                if contradicted:
                    self.add("INTRO", "MEDIUM", "DRIFT",
                             f"'{i_file.name}' has contradictory status for port(s): {', '.join(sorted(contradicted))}",
                             str(i_file),
                             "Fact-check: same port claimed both active AND inactive")
            except Exception:
                pass

    # ═══════════════════════════════════════════════════════════════════════════
    #  ELLE SYSTEM SCAN
    # ═══════════════════════════════════════════════════════════════════════════

    def scan_elle(self):
        """Scan the ELLE agent system for issues."""
        print("\n━━━ SCANNING: ELLE SYSTEM ━━━")

        if not ELLE_PATH.exists():
            self.add("ELLE", "CRITICAL", "BROKEN_REF", "ELLE path does not exist!", str(ELLE_PATH))
            return

        # 1. Check master files freshness
        master_files = [
            "00_MASTER_INDEX.md",
            "00_MASTER_OVERSIGT.md",
            "CLAUDE.md",
        ]
        for mf in master_files:
            mf_path = ELLE_PATH / mf
            if mf_path.exists():
                age = (NOW - datetime.fromtimestamp(mf_path.stat().st_mtime)).days
                if age > 14:
                    self.add("ELLE", "CRITICAL" if age > 21 else "MEDIUM", "STALE",
                             f"'{mf}' is {age} days old",
                             str(mf_path),
                             "Update master documentation")
            else:
                self.add("ELLE", "MEDIUM", "BROKEN_REF", f"'{mf}' not found", str(ELLE_PATH))

        # 2. Check heartbeat AND update it (scanner is the heartbeat writer)
        heartbeat = ELLE_PATH / "ADMIRAL_HEARTBEAT.json"
        if heartbeat.exists():
            age = (NOW - datetime.fromtimestamp(heartbeat.stat().st_mtime)).days
            if age > 3:
                self.add("ELLE", "MEDIUM", "STALE",
                         f"Admiral heartbeat is {age} days old",
                         str(heartbeat),
                         "System may need reactivation")
        else:
            self.add("ELLE", "LOW", "BROKEN_REF", "No heartbeat file found")

        # Update heartbeat file to prove scanner is running
        try:
            import json as _json, time as _time
            docker_count = 0
            try:
                _out = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True, timeout=5)
                docker_count = len(_out.stdout.strip().split("\n")) if _out.stdout.strip() else 0
            except Exception:
                pass
            hb_data = {
                "timestamp": NOW.isoformat(),
                "status": "ALIVE",
                "message": "Admiral er IKKE luft - dette opdateres af admiral_scanner.py dagligt kl 07:50",
                "uptime_check": _time.time(),
                "docker_containers": docker_count,
                "sejrliste_health": "scanner_active",
                "systems_monitored": ["Sejrliste", "INTRO", "ELLE", "Context", "Infrastructure"],
                "scanner_version": "admiral_scanner.py v1.2 (with heartbeat write)",
                "last_scanner_run": NOW.strftime("%Y-%m-%d %H:%M"),
            }
            heartbeat.write_text(_json.dumps(hb_data, indent=4))
        except Exception:
            pass  # Don't fail scanner if heartbeat write fails

        # 3. Check for .md suffix directory naming conflicts
        for item in sorted(ELLE_PATH.iterdir()):
            if item.is_dir() and item.name.endswith('.md'):
                self.add("ELLE", "LOW", "DRIFT",
                         f"Directory with .md suffix: '{item.name}/' (confusing naming)",
                         str(item),
                         "Consider renaming to remove .md suffix")

        # 3b. Check crontab for stale ELLE paths
        # PERMANENT PREVENTION: Renamed dirs leave stale refs in crontab (2026-02-01)
        try:
            crontab = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
            if crontab.returncode == 0:
                for line in crontab.stdout.splitlines():
                    if line.strip().startswith('#') or not line.strip():
                        continue
                    # Check for .md suffix dirs in cron paths
                    for md_dir_match in re.finditer(r'ELLE\.md/(\w+)\.md/', line):
                        dirname = md_dir_match.group(1)
                        correct_dir = ELLE_PATH / dirname
                        stale_dir = ELLE_PATH / f"{dirname}.md"
                        if correct_dir.exists() and not stale_dir.exists():
                            self.add("ELLE", "MEDIUM", "STALE_PATH",
                                     f"Crontab references '{dirname}.md/' but dir was renamed to '{dirname}/'",
                                     line.strip()[:80],
                                     f"Fix crontab: replace {dirname}.md/ with {dirname}/")
        except Exception:
            pass

        # 4. Check organic teams activity
        organic_dir = ELLE_PATH / "ORGANIC_TEAMS"
        if organic_dir.exists():
            runtime_log = organic_dir / "runtime.log"
            if runtime_log.exists():
                age = (NOW - datetime.fromtimestamp(runtime_log.stat().st_mtime)).days
                if age > 7:
                    self.add("ELLE", "MEDIUM", "STALE",
                             f"Organic teams runtime.log is {age} days old",
                             str(runtime_log),
                             "Organic teams may need restarting")

        # 5. Check briefings
        briefings_dir = ELLE_PATH / "BRIEFINGS"
        if briefings_dir.exists():
            briefing_files = sorted(briefings_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
            if briefing_files:
                latest = briefing_files[0]
                age = (NOW - datetime.fromtimestamp(latest.stat().st_mtime)).days
                if age > 3:
                    self.add("ELLE", "MEDIUM", "STALE",
                             f"Latest briefing '{latest.name}' is {age} days old",
                             str(latest),
                             "Auto-briefing may have stopped")

        # 6. Disk usage warning
        try:
            import subprocess
            result = subprocess.run(
                ["du", "-sh", str(ELLE_PATH)],
                capture_output=True, text=True, timeout=30
            )
            size = result.stdout.split()[0] if result.stdout else "?"
            size_gb = float(size.replace('G', '')) if 'G' in size else 0
            if size_gb > 15:
                self.add("ELLE", "LOW", "OPPORTUNITY",
                         f"ELLE system is {size} — consider cleaning ML venvs",
                         str(ELLE_PATH),
                         "vllm-gateway-env (9.3GB) + mergekit_env (7.1GB) can be removed if unused")
            else:
                self.add("ELLE", "INFO", "DRIFT", f"ELLE disk usage: {size}")
        except Exception as e:
            self.add("ELLE", "LOW", "DRIFT", f"Could not check disk: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    #  CONTEXT SYSTEM SCAN (Kv1nt's memory)
    # ═══════════════════════════════════════════════════════════════════════════

    def scan_context(self):
        """Scan the context/memory system for issues."""
        print("\n━━━ SCANNING: CONTEXT SYSTEM ━━━")

        if not CONTEXT_PATH.exists():
            self.add("CONTEXT", "CRITICAL", "BROKEN_REF", "Context path does not exist!")
            return

        # 1. Check all core files exist
        required_files = [
            "identity.md", "preferences.md", "workflows.md", "relationships.md",
            "triggers.md", "projects.md", "rules.md", "session.md", "journal.md"
        ]
        for rf in required_files:
            rf_path = CONTEXT_PATH / rf
            if not rf_path.exists():
                self.add("CONTEXT", "CRITICAL", "BROKEN_REF", f"Missing core file: {rf}")
            else:
                # Check staleness
                age = (NOW - datetime.fromtimestamp(rf_path.stat().st_mtime)).days
                if rf in ["session.md", "projects.md"] and age > 7:
                    self.add("CONTEXT", "MEDIUM", "STALE",
                             f"'{rf}' is {age} days old",
                             str(rf_path),
                             "May need updating")

                # Check file size (too large = context window issues)
                size_kb = rf_path.stat().st_size / 1024
                if size_kb > 50:
                    self.add("CONTEXT", "LOW", "OPPORTUNITY",
                             f"'{rf}' is {size_kb:.0f}KB — consider archiving old content",
                             str(rf_path))

        # 2. Check journal for recent activity
        journal_path = CONTEXT_PATH / "journal.md"
        if journal_path.exists():
            content = journal_path.read_text(encoding="utf-8")
            dates = re.findall(r'### (\d{4}-\d{2}-\d{2})', content)
            if dates:
                latest = max(dates)
                latest_date = datetime.strptime(latest, "%Y-%m-%d")
                days_since = (NOW - latest_date).days
                if days_since > 3:
                    self.add("CONTEXT", "LOW", "STALE",
                             f"Last journal entry is {days_since} days old ({latest})",
                             str(journal_path))

    # ═══════════════════════════════════════════════════════════════════════════
    #  INFRASTRUCTURE SCAN (Docker, Tailscale, Disk, Services)
    # ═══════════════════════════════════════════════════════════════════════════

    def scan_infrastructure(self):
        """Scan the full ROG desktop infrastructure."""
        print("\n━━━ SCANNING: INFRASTRUCTURE ━━━")

        # 1. Docker containers
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                containers = [l.split('\t') for l in result.stdout.strip().splitlines() if l.strip()]
                healthy = [c for c in containers if "healthy" in (c[1] if len(c) > 1 else "")]
                unhealthy = [c for c in containers if "unhealthy" in (c[1] if len(c) > 1 else "")]
                total = len(containers)

                self.add("INFRA", "INFO", "DRIFT", f"Docker: {total} containers running, {len(healthy)} healthy")

                for c in unhealthy:
                    self.add("INFRA", "CRITICAL", "DRIFT",
                             f"Docker container UNHEALTHY: {c[0]}",
                             fix_hint=f"docker logs {c[0]}")

                # Check for expected containers
                expected = ["cc-cle", "cc-postgres", "cc-redis"]
                for exp in expected:
                    if not any(exp in c[0] for c in containers):
                        self.add("INFRA", "MEDIUM", "DRIFT",
                                 f"Expected container '{exp}' NOT running",
                                 fix_hint=f"Check docker-compose for {exp}")
            else:
                self.add("INFRA", "LOW", "DRIFT", "Docker not running or not accessible")
        except Exception as e:
            self.add("INFRA", "LOW", "DRIFT", f"Cannot check Docker: {e}")

        # 2. Tailscale mesh status
        try:
            result = subprocess.run(
                ["tailscale", "status", "--json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                ts_data = json.loads(result.stdout)
                peers = ts_data.get("Peer", {})
                self_online = ts_data.get("Self", {}).get("Online", False)

                if self_online:
                    self.add("INFRA", "INFO", "DRIFT", "Tailscale ROG: ONLINE")
                else:
                    self.add("INFRA", "CRITICAL", "DRIFT", "Tailscale ROG: OFFLINE!")

                for peer_id, peer in peers.items():
                    name = peer.get("HostName", "unknown")
                    online = peer.get("Online", False)
                    if not online:
                        last_seen = peer.get("LastSeen", "unknown")
                        self.add("INFRA", "LOW", "DRIFT",
                                 f"Tailscale peer '{name}': OFFLINE (last: {last_seen[:19] if len(last_seen) > 19 else last_seen})")
                    else:
                        self.add("INFRA", "INFO", "DRIFT", f"Tailscale peer '{name}': ONLINE")
        except Exception as e:
            self.add("INFRA", "LOW", "DRIFT", f"Cannot check Tailscale: {e}")

        # 3. Disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage("/home")
            pct = int(used / total * 100)
            free_gb = free / (1024**3)
            if pct > 90:
                self.add("INFRA", "CRITICAL", "DRIFT",
                         f"Disk {pct}% full — only {free_gb:.0f}GB free!",
                         fix_hint="Clean up large directories")
            elif pct > 80:
                self.add("INFRA", "MEDIUM", "DRIFT",
                         f"Disk {pct}% full — {free_gb:.0f}GB free",
                         fix_hint="Consider cleanup soon")
            else:
                self.add("INFRA", "INFO", "DRIFT", f"Disk: {pct}% used, {free_gb:.0f}GB free")
        except Exception as e:
            self.add("INFRA", "LOW", "DRIFT", f"Cannot check disk: {e}")

        # 4. Ollama AI
        try:
            import urllib.request
            resp = urllib.request.urlopen("http://localhost:11434/api/version", timeout=5)
            data = json.loads(resp.read())
            version = data.get("version", "?")
            self.add("INFRA", "INFO", "DRIFT", f"Ollama: v{version} RUNNING")
        except Exception:
            self.add("INFRA", "LOW", "DRIFT", "Ollama: NOT running")

        # 5. Large directory warnings
        large_dirs = {
            "/home/rasmus/Desktop/projekts/": 29,
            "/home/rasmus/Desktop/ELLE.md/": 19,
        }
        for dir_path, expected_gb in large_dirs.items():
            p = Path(dir_path)
            if p.exists():
                try:
                    result = subprocess.run(
                        ["du", "-s", str(p)],
                        capture_output=True, text=True, timeout=30
                    )
                    size_kb = int(result.stdout.split()[0])
                    size_gb = size_kb / (1024 * 1024)
                    if size_gb > expected_gb * 1.2:  # 20% growth alert
                        self.add("INFRA", "LOW", "OPPORTUNITY",
                                 f"'{p.name}/' grew to {size_gb:.1f}GB (was ~{expected_gb}GB)",
                                 str(p),
                                 "Check for unnecessary data growth")
                except Exception:
                    pass

    # ═══════════════════════════════════════════════════════════════════════════
    #  CROSS-SYSTEM ANALYSIS
    # ═══════════════════════════════════════════════════════════════════════════

    def scan_cross_system(self):
        """Find issues that span multiple systems."""
        print("\n━━━ SCANNING: CROSS-SYSTEM ━━━")

        # 1. Check if projects.md matches reality
        projects_path = CONTEXT_PATH / "projects.md"
        if projects_path.exists():
            content = projects_path.read_text(encoding="utf-8")

            # Check if current focus project path exists
            path_matches = re.findall(r'`(/home/rasmus/[^`]+)`', content)
            for pm in path_matches:
                if not Path(pm).exists():
                    self.add("CROSS", "MEDIUM", "BROKEN_REF",
                             f"projects.md references non-existent path: {pm}",
                             str(projects_path),
                             "Update path in projects.md")

        # 2. Pattern: recurring problems
        critical_count = len([f for f in self.findings if f.severity == "CRITICAL"])
        medium_count = len([f for f in self.findings if f.severity == "MEDIUM"])
        stale_count = len([f for f in self.findings if f.category == "STALE"])

        if stale_count > 5:
            self.add("CROSS", "MEDIUM", "OPPORTUNITY",
                     f"{stale_count} stale items across all systems — consider a maintenance day",
                     fix_hint="Dedicate a session to updating all stale files")

    # ═══════════════════════════════════════════════════════════════════════════
    #  GENERATE BRIEFING
    # ═══════════════════════════════════════════════════════════════════════════

    def generate_briefing(self) -> str:
        """Generate the morning briefing markdown."""
        critical = [f for f in self.findings if f.severity == "CRITICAL"]
        medium = [f for f in self.findings if f.severity == "MEDIUM"]
        low = [f for f in self.findings if f.severity == "LOW"]
        info = [f for f in self.findings if f.severity == "INFO"]

        # Calculate system scores
        def system_score(system: str) -> int:
            system_findings = [f for f in self.findings if f.system == system]
            if not system_findings:
                return 100  # No findings = no problems = perfect score
            crit = len([f for f in system_findings if f.severity == "CRITICAL"])
            med = len([f for f in system_findings if f.severity == "MEDIUM"])
            low_count = len([f for f in system_findings if f.severity == "LOW"])
            total = len(system_findings)
            penalty = crit * 15 + med * 5 + low_count * 1
            return max(0, 100 - penalty)

        sejr_score = system_score("SEJRLISTE")
        intro_score = system_score("INTRO")
        elle_score = system_score("ELLE")
        context_score = system_score("CONTEXT")

        lines = []
        lines.append(f"# ⚓ ADMIRAL MORNING BRIEFING — {NOW.strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        lines.append("> Auto-generated by admiral_scanner.py. Din daglige oversigt.")
        lines.append("")
        lines.append("## System Health")
        lines.append("")
        lines.append("| System | Score | Status |")
        lines.append("|--------|-------|--------|")

        infra_score = system_score("INFRA")

        for name, score in [("Sejrliste", sejr_score), ("INTRO", intro_score), ("ELLE", elle_score), ("Context", context_score), ("Infrastructure", infra_score)]:
            icon = "🟢" if score >= 90 else "🟡" if score >= 70 else "🔴"
            lines.append(f"| {name} | {score}% | {icon} |")

        lines.append("")

        if critical:
            lines.append(f"## 🔴 CRITICAL ({len(critical)})")
            lines.append("")
            for f in critical:
                lines.append(f"- **[{f.system}]** {f.message}")
                if f.fix_hint:
                    lines.append(f"  - Fix: {f.fix_hint}")
            lines.append("")

        if medium:
            lines.append(f"## 🟡 MEDIUM ({len(medium)})")
            lines.append("")
            for f in medium:
                lines.append(f"- **[{f.system}]** {f.message}")
                if f.fix_hint:
                    lines.append(f"  - Fix: {f.fix_hint}")
            lines.append("")

        if low:
            lines.append(f"## 🔵 LOW ({len(low)})")
            lines.append("")
            for f in low:
                lines.append(f"- [{f.system}] {f.message}")
            lines.append("")

        # Suggested priorities
        lines.append("## Foreslåede Prioriteter")
        lines.append("")
        if critical:
            lines.append(f"1. **FIX {len(critical)} CRITICAL issues** — disse blokerer systemintegriteten")
        if medium:
            lines.append(f"2. **Address {len(medium)} MEDIUM issues** — drift og stale filer")
        lines.append(f"3. **Total findings:** {len(critical)} critical, {len(medium)} medium, {len(low)} low, {len(info)} info")
        lines.append("")
        lines.append("---")
        lines.append(f"*Genereret: {NOW.strftime('%Y-%m-%d %H:%M:%S')} af admiral_scanner.py*")

        return "\n".join(lines)

    # ═══════════════════════════════════════════════════════════════════════════
    #  RUN ALL
    # ═══════════════════════════════════════════════════════════════════════════

    def run_all(self):
        """Run all scanners and generate output."""
        print("=" * 60)
        print("  ⚓ ADMIRAL SCANNER — Cross-System Discovery")
        print(f"  {NOW.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        self.scan_sejrliste()
        self.scan_intro()
        self.scan_elle()
        self.scan_context()
        self.scan_infrastructure()
        self.scan_cross_system()

        # Print summary
        critical = [f for f in self.findings if f.severity == "CRITICAL"]
        medium = [f for f in self.findings if f.severity == "MEDIUM"]
        low = [f for f in self.findings if f.severity == "LOW"]
        info = [f for f in self.findings if f.severity == "INFO"]

        print("\n" + "=" * 60)
        print(f"  RESULTAT: {len(critical)} CRITICAL | {len(medium)} MEDIUM | {len(low)} LOW | {len(info)} INFO")
        print("=" * 60)

        for f in critical:
            print(f"  🔴 [{f.system}] {f.message}")
        for f in medium:
            print(f"  🟡 [{f.system}] {f.message}")

        return len(critical), len(medium), len(low)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Admiral Scanner — Cross-System Discovery")
    parser.add_argument("--brief", action="store_true", help="Generate morning briefing file")
    parser.add_argument("--quiet", action="store_true", help="Only output if problems found")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    args = parser.parse_args()

    scanner = AdmiralScanner()
    crit, med, low = scanner.run_all()

    # Always generate briefing
    briefing = scanner.generate_briefing()

    if args.brief or True:  # Always write briefing
        BRIEFING_PATH.parent.mkdir(parents=True, exist_ok=True)
        BRIEFING_PATH.write_text(briefing, encoding="utf-8")
        print(f"\n  📋 Briefing saved: {BRIEFING_PATH}")

    # Log findings
    SCANNER_LOG.parent.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "timestamp": NOW.isoformat(),
        "critical": crit,
        "medium": med,
        "low": low,
        "total": len(scanner.findings),
        "findings": [f.to_dict() for f in scanner.findings],
    }
    with open(SCANNER_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    if args.json:
        print(json.dumps([f.to_dict() for f in scanner.findings], indent=2))

    # Exit code: 1 if critical, 0 otherwise
    sys.exit(1 if crit > 0 else 0)


if __name__ == "__main__":
    main()
