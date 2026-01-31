#!/usr/bin/env python3
"""
AUTO HEALTH CHECK — Permanent System Integrity Guard
=====================================================

Kører automatisk og finder + reparerer problemer LØBENDE.
Deler ALDRIG YAML, ALDRIG lader korrupte filer overleve.

DNA Layer 3 (SELF-VERIFYING) + DNA Layer 7 (SELF-OPTIMIZING)

BRUG:
    python3 scripts/auto_health_check.py          # Full check
    python3 scripts/auto_health_check.py --repair  # Check + auto-repair
    python3 scripts/auto_health_check.py --quiet   # Kun fejl vises

EXIT CODES:
    0 = All OK
    1 = Issues found (use --repair to fix)
    2 = Critical failure
"""

import argparse
import yaml
import json
import py_compile
import subprocess
import sys
from pathlib import Path
from datetime import datetime


# ════════════════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════════════════

SYSTEM_PATH = Path(__file__).parent.parent
SCRIPTS_DIR = SYSTEM_PATH / "scripts"
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
CURRENT_DIR = SYSTEM_PATH / "_CURRENT"
TEMPLATES_DIR = SYSTEM_PATH / "00_TEMPLATES"


class HealthCheck:
    def __init__(self, quiet=False, repair=False):
        self.quiet = quiet
        self.repair = repair
        self.passed = 0
        self.failed = 0
        self.repaired = 0
        self.warnings = 0

    def ok(self, msg, detail=""):
        self.passed += 1
        if not self.quiet:
            d = f" — {detail}" if detail else ""
            print(f"  [OK]   {msg}{d}")

    def fail(self, msg, detail=""):
        self.failed += 1
        d = f" — {detail}" if detail else ""
        print(f"  [FAIL] {msg}{d}")

    def fixed(self, msg, detail=""):
        self.repaired += 1
        d = f" — {detail}" if detail else ""
        print(f"  [FIXED] {msg}{d}")

    def warn(self, msg, detail=""):
        self.warnings += 1
        if not self.quiet:
            d = f" — {detail}" if detail else ""
            print(f"  [WARN] {msg}{d}")

    # ══════════════════════════════════════════════════════════════════════
    # CHECK 1: STATUS.yaml integrity
    # ══════════════════════════════════════════════════════════════════════

    def check_status_yaml(self):
        """Verify all STATUS.yaml files are valid YAML with correct structure."""
        print("\n── STATUS.yaml INTEGRITY ──")

        for status_file in sorted(SYSTEM_PATH.rglob("STATUS.yaml")):
            if any(x in str(status_file) for x in ["_unused", ".venv", "venv", "00_TEMPLATES"]):
                continue

            try:
                content = status_file.read_text(encoding="utf-8")
                data = yaml.safe_load(content)

                if not isinstance(data, dict):
                    if self.repair:
                        self._repair_status_yaml(status_file)
                    else:
                        self.fail(f"{status_file.parent.name}/STATUS.yaml", "Not a dict")
                    continue

                if len(data) == 0:
                    self.warn(f"{status_file.parent.name}/STATUS.yaml", "Empty file")
                    continue

                # Check for flat structure (sign of old buggy parser)
                if "meta" in data and isinstance(data["meta"], str):
                    if self.repair:
                        self._repair_status_yaml(status_file)
                    else:
                        self.fail(f"{status_file.parent.name}/STATUS.yaml", "Flat structure detected (meta is string)")
                    continue

                self.ok(f"{status_file.parent.name}/STATUS.yaml")

            except yaml.YAMLError as e:
                if self.repair:
                    self._repair_status_yaml(status_file)
                else:
                    self.fail(f"{status_file.parent.name}/STATUS.yaml", f"Invalid YAML: {str(e)[:50]}")

    def _repair_status_yaml(self, filepath: Path):
        """Repair a corrupted STATUS.yaml by restructuring flat data."""
        content = filepath.read_text(encoding="utf-8")

        flat = {}
        session_lines = []
        in_session = False

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- id:"):
                in_session = True
                session_lines.append(line)
                continue
            if in_session and ":" not in line:
                in_session = False
            if in_session:
                session_lines.append(line)
                continue
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().strip('"').strip("'")
                    if value == "":
                        value = None
                    elif value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    elif value == "null":
                        value = None
                    elif value == "[]":
                        value = []
                    else:
                        try:
                            value = float(value) if "." in value else int(value)
                        except (ValueError, TypeError):
                            pass
                    flat[key] = value

        sessions = []
        if session_lines:
            current = {}
            for line in session_lines:
                line = line.strip()
                if line.startswith("- id:"):
                    if current:
                        sessions.append(current)
                    current = {"id": line.split(":", 1)[1].strip().strip('"')}
                elif ":" in line:
                    parts = line.split(":", 1)
                    current[parts[0].strip()] = parts[1].strip().strip('"').strip("'")
            if current:
                sessions.append(current)

        reconstructed = {
            "meta": {
                "sejr_name": flat.get("sejr_name", "unknown"),
                "folder": flat.get("folder", "unknown"),
                "created": flat.get("created", ""),
                "created_by": flat.get("created_by", "generate_sejr.py"),
                "session_id": flat.get("session_id", ""),
                "last_updated": datetime.now().isoformat(),
            },
            "pass_tracking": {
                "current_pass": flat.get("current_pass", 1),
                "can_archive": flat.get("can_archive", False),
                "archive_blocker": flat.get("archive_blocker", ""),
                "pass_1": {
                    "name": "Planlægning",
                    "status": flat.get("status", "pending"),
                    "complete": flat.get("pass_1_complete", False),
                    "score": flat.get("pass_1_score", flat.get("score", 0)),
                    "percentage": flat.get("pass_1_pct", flat.get("percentage", 0)),
                },
                "pass_2": {
                    "name": "Eksekvering",
                    "complete": flat.get("pass_2_complete", False),
                    "score": flat.get("pass_2_score", 0),
                    "percentage": flat.get("pass_2_pct", 0),
                },
                "pass_3": {
                    "name": "7-DNA Review",
                    "complete": flat.get("pass_3_complete", False),
                    "score": flat.get("pass_3_score", 0),
                    "percentage": flat.get("pass_3_pct", 0),
                },
            },
            "score_tracking": {
                "positive": {k: flat.get(k, 0) for k in ["checkbox_done", "pass_complete", "verified_working", "admiral_moment", "sejr_archived"]},
                "negative": {k: flat.get(k, 0) for k in ["token_waste", "memory_loss", "lie_detected", "rule_break", "focus_lost"]},
                "totals": {
                    "total_score": flat.get("total_score", 0),
                    "rank": flat.get("rank", "KADET"),
                },
            },
            "model_tracking": {
                "sessions": sessions if sessions else [],
            },
            "statistics": {
                "total_sessions": flat.get("total_sessions", 1),
                "total_actions": flat.get("total_actions", 1),
                "completion_percentage": flat.get("completion_percentage", 0),
            },
        }

        header = f"# STATUS.yaml - REPAIRED by auto_health_check.py\n# Repaired: {datetime.now().isoformat()}\n\n"
        yaml_content = yaml.dump(reconstructed, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
        filepath.write_text(header + yaml_content, encoding="utf-8")
        self.fixed(f"{filepath.parent.name}/STATUS.yaml")

    def _reconstruct_sejr_liste(self, archive_dir: Path):
        """Reconstruct a missing SEJR_LISTE.md from archive metadata."""
        status_file = archive_dir / "STATUS.yaml"
        sejr_name = archive_dir.name.split("_2026")[0].replace("_", " ")
        created = ""
        total_score = 0
        rank = "KADET"

        if status_file.exists():
            try:
                data = yaml.safe_load(status_file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    meta = data.get("meta", {})
                    sejr_name = meta.get("sejr_name", sejr_name)
                    created = meta.get("created", "")
                    scoring = data.get("score_tracking", {}).get("totals", {})
                    total_score = scoring.get("total_score", 0)
                    rank = scoring.get("rank", "KADET")
            except (yaml.YAMLError, UnicodeDecodeError):
                pass

        content = f"""# SEJR LISTE: {sejr_name}

> **REKONSTRUERET** af auto_health_check.py ({datetime.now().strftime('%Y-%m-%d')})
> Original gik tabt under arkivering (pre-fix).

---

## STATUS: ARKIVERET

- **Navn:** {sejr_name}
- **Oprettet:** {created}
- **Score:** {total_score}/30
- **Rang:** {rank}
"""
        sejr_liste = archive_dir / "SEJR_LISTE.md"
        sejr_liste.write_text(content, encoding="utf-8")
        self.fixed(f"Archive: {archive_dir.name}/SEJR_LISTE.md", "Reconstructed")

    # ══════════════════════════════════════════════════════════════════════
    # CHECK 2: Script syntax
    # ══════════════════════════════════════════════════════════════════════

    def check_scripts_compile(self):
        """Verify all Python scripts compile without syntax errors."""
        print("\n── SCRIPT SYNTAX ──")
        all_ok = True
        for script in sorted(SCRIPTS_DIR.glob("*.py")):
            try:
                py_compile.compile(str(script), doraise=True)
            except py_compile.PyCompileError as e:
                self.fail(f"{script.name}", str(e)[:60])
                all_ok = False
        if all_ok:
            count = len(list(SCRIPTS_DIR.glob("*.py")))
            self.ok(f"All scripts compile", f"{count} scripts")

    # ══════════════════════════════════════════════════════════════════════
    # CHECK 3: Web app
    # ══════════════════════════════════════════════════════════════════════

    def check_web_app(self):
        """Verify Streamlit web app is running and has responsive CSS."""
        print("\n── WEB APP ──")
        try:
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:8501"],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip() == "200":
                self.ok("Streamlit running", "HTTP 200")
            else:
                self.fail("Streamlit running", f"HTTP {result.stdout.strip()}")
        except Exception:
            self.fail("Streamlit running", "Connection failed")

        for name, path in [("Dansk", "web_app.py"), ("English", "web_app_en.py")]:
            f = SYSTEM_PATH / path
            if f.exists():
                content = f.read_text()
                media = content.count("@media")
                if media >= 5:
                    self.ok(f"{name} responsive CSS", f"{media} @media queries")
                else:
                    self.fail(f"{name} responsive CSS", f"Only {media} @media queries")

    # ══════════════════════════════════════════════════════════════════════
    # CHECK 4: Data integrity
    # ══════════════════════════════════════════════════════════════════════

    def check_data_integrity(self):
        """Verify patterns, archives, and system files."""
        print("\n── DATA INTEGRITY ──")

        # PATTERNS.json
        pf = CURRENT_DIR / "PATTERNS.json"
        if pf.exists():
            try:
                data = json.loads(pf.read_text())
                # PATTERNS.json is a dict with "learned_patterns" list inside
                if isinstance(data, dict) and "learned_patterns" in data:
                    patterns = data["learned_patterns"]
                    self.ok("PATTERNS.json", f"{len(patterns)} patterns")
                elif isinstance(data, list):
                    self.ok("PATTERNS.json", f"{len(data)} patterns (legacy format)")
                else:
                    self.warn("PATTERNS.json", "Unexpected structure")
            except json.JSONDecodeError:
                self.fail("PATTERNS.json", "Invalid JSON")
        else:
            self.warn("PATTERNS.json", "File missing")

        # Archives — check completeness (every archive should have SEJR_LISTE.md + STATUS.yaml)
        if ARCHIVE_DIR.exists():
            archive_dirs = [d for d in ARCHIVE_DIR.iterdir() if d.is_dir()]
            complete = 0
            for adir in sorted(archive_dirs):
                required_archive = ["STATUS.yaml", "SEJR_LISTE.md", "CONCLUSION.md"]
                missing_archive = [f for f in required_archive if not (adir / f).exists()]
                if missing_archive:
                    if self.repair:
                        # Reconstruct missing SEJR_LISTE.md from metadata
                        if "SEJR_LISTE.md" in missing_archive:
                            self._reconstruct_sejr_liste(adir)
                            missing_archive.remove("SEJR_LISTE.md")
                    if missing_archive:
                        self.fail(f"Archive: {adir.name}", f"Missing: {', '.join(missing_archive)}")
                    else:
                        complete += 1
                else:
                    complete += 1
            self.ok("Archive completeness", f"{complete}/{len(archive_dirs)} complete")

        # Clean up crashed atomic creations (temp dirs left behind)
        if ACTIVE_DIR.exists():
            import shutil as _shutil
            for item in sorted(ACTIVE_DIR.iterdir()):
                if item.is_dir() and item.name.startswith(".tmp_"):
                    if self.repair:
                        _shutil.rmtree(item)
                        self.fixed(f"Temp dir removed: {item.name}", "Crashed atomic creation")
                    else:
                        self.fail(f"Temp dir in ACTIVE: {item.name}", "Crashed atomic creation — use --repair")

        # Active sejre have required files — detect + remove orphans
        if ACTIVE_DIR.exists():
            for sejr_dir in sorted(ACTIVE_DIR.iterdir()):
                if not sejr_dir.is_dir() or sejr_dir.name.startswith("."):
                    continue
                required = ["SEJR_LISTE.md", "CLAUDE.md", "STATUS.yaml"]
                missing = [f for f in required if not (sejr_dir / f).exists()]
                if missing:
                    # Check if this is an orphan (already archived)
                    archived_match = any(
                        sejr_dir.name.split("_2026")[0] in a.name
                        for a in ARCHIVE_DIR.iterdir() if a.is_dir()
                    ) if ARCHIVE_DIR.exists() else False

                    if self.repair and archived_match and len(missing) >= 2:
                        import shutil
                        shutil.rmtree(sejr_dir)
                        self.fixed(f"Orphan removed: {sejr_dir.name}", "Already archived")
                    elif archived_match:
                        self.fail(f"Orphan: {sejr_dir.name}", f"Already archived, missing: {', '.join(missing)}")
                    else:
                        self.fail(f"Active: {sejr_dir.name}", f"Missing: {', '.join(missing)}")
                else:
                    self.ok(f"Active: {sejr_dir.name}", "All required files present")

        # Check for duplicate sejre (in both active AND archive)
        if ACTIVE_DIR.exists() and ARCHIVE_DIR.exists():
            active_names = {d.name.split("_2026")[0] for d in ACTIVE_DIR.iterdir() if d.is_dir()}
            archive_names = {d.name.split("_2026")[0] for d in ARCHIVE_DIR.iterdir() if d.is_dir()}
            duplicates = active_names & archive_names
            if duplicates:
                for dup in duplicates:
                    self.warn(f"Duplicate sejr in active+archive: {dup}")

    # ══════════════════════════════════════════════════════════════════════
    # CHECK 5: Prevention — no buggy YAML parsers can return
    # ══════════════════════════════════════════════════════════════════════

    def check_prevention(self):
        """Ensure the buggy flat YAML parser never returns to any script."""
        print("\n── PREVENTION ──")

        buggy_scripts = []
        for script in sorted(SCRIPTS_DIR.glob("*.py")):
            content = script.read_text(encoding="utf-8")
            # The buggy parser had this exact pattern: line-by-line parsing + "parse_yaml" function
            if "def parse_yaml_simple" in content:
                # Check if it's the PyYAML version or the buggy version
                if "yaml.safe_load" not in content:
                    buggy_scripts.append(script.name)

        if buggy_scripts:
            for s in buggy_scripts:
                self.fail(f"Buggy YAML parser in {s}", "Missing yaml.safe_load — must use PyYAML")
        else:
            self.ok("No buggy YAML parsers", "All scripts use PyYAML")

        # Check for orphan .venv (deleted 2026-01-31, cairosvg moved to venv/)
        dotenv = SYSTEM_PATH / ".venv"
        if dotenv.exists():
            self.warn("Orphan .venv/ found", "Should not exist — cairosvg is in venv/")

    # ══════════════════════════════════════════════════════════════════════
    # CHECK 6: systemd + services
    # ══════════════════════════════════════════════════════════════════════

    def check_services(self):
        """Verify system services are running."""
        print("\n── SERVICES ──")
        try:
            result = subprocess.run(
                ["systemctl", "--user", "is-active", "sejrliste-web.service"],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip() == "active":
                self.ok("sejrliste-web.service", "active")
            else:
                self.fail("sejrliste-web.service", result.stdout.strip())
        except Exception:
            self.warn("sejrliste-web.service", "Cannot check")

    # ══════════════════════════════════════════════════════════════════════
    # RUN ALL
    # ══════════════════════════════════════════════════════════════════════

    def run_all(self):
        """Run complete health check."""
        print("=" * 60)
        print("  SEJRLISTE SYSTEM — HEALTH CHECK")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        self.check_status_yaml()
        self.check_scripts_compile()
        self.check_web_app()
        self.check_data_integrity()
        self.check_prevention()
        self.check_services()

        total = self.passed + self.failed
        pct = (self.passed / total * 100) if total > 0 else 0

        print()
        print("=" * 60)
        print(f"  RESULTAT: {self.passed}/{total} PASSED ({pct:.0f}%)")
        if self.repaired:
            print(f"  Auto-repaired: {self.repaired}")
        if self.warnings:
            print(f"  Warnings: {self.warnings}")
        if self.failed == 0:
            print("  STATUS: ADMIRAL STANDARD")
        else:
            print(f"  STATUS: {self.failed} ISSUES")
        print("=" * 60)

        return 0 if self.failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Sejrliste System Health Check")
    parser.add_argument("--repair", action="store_true", help="Auto-repair corrupted files")
    parser.add_argument("--quiet", action="store_true", help="Only show failures")
    args = parser.parse_args()

    hc = HealthCheck(quiet=args.quiet, repair=args.repair)
    exit_code = hc.run_all()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
