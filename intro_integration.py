#!/usr/bin/env python3
"""
INTRO FOLDER SYSTEM - DATA MODEL AND INTEGRATION LAYER

This module provides the data model and scanning functions for integrating
the MASTER FOLDERS (INTRO) system into the Victory List GTK4 application.

It reads the real filesystem at /home/rasmus/Desktop/MASTER FOLDERS(INTRO)/
and provides structured Python dataclasses for all INTRO content:
  - I1-I12 System Intelligence files
  - B1-B10 Terminal Commands
  - C1-C10 Environment Configuration
  - D1-D10 Architecture Documentation
  - E1-E4 Templates (structure only, no agent content)
  - F1-F10 Old Projects
  - G0-G4 Laptop Catalog
  - H1-H3 Fleet Collaboration

FASE 0: Data Model for Sejrliste INTRO Integration
Author: Kv1nt (Claude Opus 4.5) for Rasmus
Date: 2026-01-30
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

INTRO_PATH: Path = Path("/home/rasmus/Desktop/MASTER FOLDERS(INTRO)")
"""Absolute path to the MASTER FOLDERS (INTRO) root directory."""

# Category definitions: (letter, display_name, subfolder_or_root, description, file_prefix_pattern)
# Files live either in root or in a named subfolder.
CATEGORY_DEFINITIONS: list[tuple[str, str, Optional[str], str, str]] = [
    (
        "I",
        "System Intelligence",
        None,  # root level
        "Core system intelligence files I1-I12: vision, orders, briefings, alerts, environments, bug fixes, central control, bridges, ecosystem, compliance, and victory tracking.",
        r"^I\d+_",
    ),
    (
        "B",
        "Terminal Commands",
        "PROJEKTS TERMINALS",
        "Terminal command references B1-B10: Cirkelline, Cosmic, CKC Gateway, Kommandor, Docker, Database, Monitoring, Backup, Deployment, and Troubleshooting.",
        r"^B\d+_",
    ),
    (
        "C",
        "Environment Configuration",
        "PROJEKTS LOKAL ENV",
        "Local environment configurations C1-C10: platform environments, Redis, RabbitMQ, Docker, PostgreSQL, AWS/LocalStack, and Monitoring.",
        r"^C\d+_",
    ),
    (
        "D",
        "Architecture Documentation",
        "PROJEKTS ARKITEKTUR(TEMPLATES)",
        "Architecture documentation D1-D10: system overview, platform architectures, integration, database schemas, API patterns, security, and deployment.",
        r"^D\d+_",
    ),
    (
        "E",
        "Agent Templates",
        "PROJEKTS ARKITEKTUR(TEMPLATES)",
        "Agent template documentation E1-E4: ELLE agents, Admiral dashboard agents, Kommandor producers, and universal agent patterns. NOTE: Structure only, agent content is out of scope.",
        r"^E\d+_",
    ),
    (
        "F",
        "Old Projects",
        "OLD PROJEKTS ORIGINAL",
        "Historical project references F1-F10: original project baselines and integration summaries.",
        r"^F\d+_",
    ),
    (
        "G",
        "Laptop Catalog",
        "LAPTOP KATALOG",
        "Complete laptop catalogs G0-G4: system index, ELLE.md catalog, projects catalog, fleet guide, and new projects.",
        r"^G\d+_",
    ),
    (
        "H",
        "Fleet Collaboration",
        "ADMIRAL FLEET COLLABORATION",
        "Admiral fleet collaboration H1-H3: multi-admiral workflow, systems guide, and victory status.",
        r"^H\d+_",
    ),
]

# I-file specific metadata: number -> (short_title, description)
I_FILE_TITLES: dict[int, tuple[str, str]] = {
    1:  ("Admiral+ Vision", "Overarching vision and 5 victories for force multiplication"),
    2:  ("Obligatory Orders", "13 mandatory orders for system compliance"),
    3:  ("Hybridernes Sandhed", "Hybrid system truth -- all working status"),
    4:  ("Morning Briefing", "Automated daily briefing system"),
    5:  ("Realtime Alerts", "Real-time monitoring and alert system"),
    6:  ("Localhost Environments", "Complete localhost setup documentation"),
    7:  ("Bug Fixes", "Bug fix patterns and tracking system"),
    8:  ("Admiral Central", "Central control hub -- the brain of the ecosystem"),
    9:  ("Ultimate Localhost Bridge", "Integration bridge for localhost services"),
    10: ("Organisk Okosystem", "Organic ecosystem documentation"),
    11: ("Naughty or Not List", "Compliance tracking and prevention log"),
    12: ("Sejr Liste System", "Victory tracking template system"),
}


# ---------------------------------------------------------------------------
# DATACLASSES
# ---------------------------------------------------------------------------

@dataclass
class IntroFile:
    """Represents a single file within the INTRO folder system.

    Attributes:
        name: Filename (e.g. "I1_ADMIRAL_PLUS_VISION.md")
        path: Absolute path to the file
        category: Category letter (I, B, C, D, E, F, G, H) or empty for misc
        size: File size in bytes
        lines: Number of lines in the file
        last_modified: Last modification timestamp as ISO string
        status: Parsed status from file header ("ACTIVE", "COMPLETE", "UNKNOWN", etc.)
    """
    name: str
    path: Path
    category: str
    size: int
    lines: int
    last_modified: str
    status: str = "UNKNOWN"

    @property
    def size_human(self) -> str:
        """Return human-readable file size."""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        else:
            return f"{self.size / (1024 * 1024):.1f} MB"

    @property
    def category_number(self) -> Optional[int]:
        """Extract the numeric part from the filename (e.g. I7 -> 7, B10 -> 10)."""
        match = re.match(r"^[A-Z](\d+)", self.name)
        if match:
            return int(match.group(1))
        return None


@dataclass
class IntroCategory:
    """Represents a category of files within the INTRO folder system.

    Attributes:
        letter: Category letter (I, B, C, D, E, F, G, H)
        name: Human-readable category name
        files: List of IntroFile instances in this category
        description: Description of what this category contains
    """
    letter: str
    name: str
    files: list[IntroFile] = field(default_factory=list)
    description: str = ""

    @property
    def file_count(self) -> int:
        """Number of files in this category."""
        return len(self.files)

    @property
    def total_size(self) -> int:
        """Total size of all files in bytes."""
        return sum(f.size for f in self.files)

    @property
    def total_lines(self) -> int:
        """Total line count across all files."""
        return sum(f.lines for f in self.files)

    @property
    def latest_modified(self) -> str:
        """ISO timestamp of the most recently modified file, or empty string."""
        if not self.files:
            return ""
        return max(f.last_modified for f in self.files)


@dataclass
class NavigationEntry:
    """A single document entry parsed from NAVIGATION_INDEX.md.

    Attributes:
        filename: The document filename
        lines: Number of lines reported in the index
        location: Relative path within INTRO folder
        main_topic: The main topic/title of the document
        sections: List of section headings found in the document
        category_code: The category code from the index (e.g. "00", "B1", "I1")
        archived: Whether the document is marked as archived
    """
    filename: str
    lines: int
    location: str
    main_topic: str
    sections: list[str] = field(default_factory=list)
    category_code: str = ""
    archived: bool = False


@dataclass
class HealthCheckResult:
    """Result of a single health check.

    Attributes:
        check_name: Name of the check performed
        passed: Whether the check passed
        message: Human-readable result message
        details: Optional additional details (e.g. list of issues)
    """
    check_name: str
    passed: bool
    message: str
    details: list[str] = field(default_factory=list)


@dataclass
class IntroHealthReport:
    """Aggregated health report for the INTRO folder system.

    Attributes:
        timestamp: When the report was generated
        checks: List of individual check results
        overall_score: Percentage of checks that passed (0.0 - 100.0)
        errors: Count of failed checks
        warnings: Count of warnings
    """
    timestamp: str
    checks: list[HealthCheckResult] = field(default_factory=list)
    overall_score: float = 0.0
    errors: int = 0
    warnings: int = 0

    def compute_score(self) -> None:
        """Recompute overall_score from individual check results."""
        if not self.checks:
            self.overall_score = 0.0
            return
        passed = sum(1 for c in self.checks if c.passed)
        self.overall_score = (passed / len(self.checks)) * 100.0
        self.errors = sum(1 for c in self.checks if not c.passed)


# ---------------------------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------------------------

def _count_lines(filepath: Path) -> int:
    """Count the number of lines in a text file, returning 0 on failure."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh)
    except (OSError, UnicodeDecodeError):
        return 0


def _read_first_lines(filepath: Path, n: int = 15) -> list[str]:
    """Read the first N lines of a file for header parsing."""
    lines: list[str] = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh):
                if i >= n:
                    break
                lines.append(line.rstrip("\n"))
    except (OSError, UnicodeDecodeError):
        pass
    return lines


def _parse_file_status(filepath: Path) -> str:
    """Parse the status from a markdown file header.

    Looks for patterns like:
        **Status:** AKTIV
        **Status:** COMPLETE
        **Status:** FAERDIG (100%)
    within the first 15 lines.
    """
    header_lines = _read_first_lines(filepath, 15)
    for line in header_lines:
        status_match = re.search(
            r"\*\*Status[:\*]*\*?\*?\s*[:]*\s*(.+)",
            line,
            re.IGNORECASE,
        )
        if status_match:
            raw = status_match.group(1).strip()
            # Normalize common statuses
            upper = raw.upper()
            if "FAERDIG" in upper or "FAERDIG" in upper or "COMPLETE" in upper or "100%" in upper:
                return "COMPLETE"
            elif "AKTIV" in upper or "ACTIVE" in upper:
                return "ACTIVE"
            elif "IN PROGRESS" in upper or "PROGRESS" in upper:
                return "IN_PROGRESS"
            elif "ARKIV" in upper or "ARCHIVED" in upper:
                return "ARCHIVED"
            elif "SEPARAT" in upper:
                return "SEPARATE_SYSTEM"
            elif "STABIL" in upper or "STABLE" in upper:
                return "STABLE"
            elif "VERIFICERET" in upper or "VERIFIED" in upper:
                return "VERIFIED"
            elif "OPERATIONAL" in upper:
                return "OPERATIONAL"
            elif "ETABLERET" in upper or "ESTABLISHED" in upper:
                return "ESTABLISHED"
            elif "ALLE" in upper and "VIRKER" in upper:
                return "ALL_WORKING"
            else:
                return raw[:40]  # Return first 40 chars of unrecognized status
    return "UNKNOWN"


def _file_modified_iso(filepath: Path) -> str:
    """Return the last-modified timestamp as an ISO 8601 string."""
    try:
        mtime = filepath.stat().st_mtime
        return datetime.fromtimestamp(mtime).isoformat(timespec="seconds")
    except OSError:
        return ""


def _scan_file(filepath: Path, category: str) -> IntroFile:
    """Build an IntroFile from a real file on disk."""
    stat = filepath.stat()
    return IntroFile(
        name=filepath.name,
        path=filepath.resolve(),
        category=category,
        size=stat.st_size,
        lines=_count_lines(filepath),
        last_modified=_file_modified_iso(filepath),
        status=_parse_file_status(filepath),
    )


def _natural_sort_key(intro_file: IntroFile) -> tuple[str, int]:
    """Sort key that orders files by category letter then by numeric suffix."""
    num = intro_file.category_number
    return (intro_file.category, num if num is not None else 9999)


# ---------------------------------------------------------------------------
# PUBLIC API: SCANNING FUNCTIONS
# ---------------------------------------------------------------------------

def get_intro_structure() -> Dict[str, Any]:
    """Scan the INTRO folder structure and return a comprehensive dict.

    Returns a dict with keys:
        "root": Path -- the INTRO root path
        "exists": bool -- whether the root exists
        "categories": dict mapping category letter to IntroCategory
        "root_files": list of IntroFile for files not belonging to any category
        "subdirectories": list of subdir names
        "total_files": int
        "total_size": int (bytes)
        "total_lines": int
        "scan_time": str (ISO timestamp of scan)
    """
    result: Dict[str, Any] = {
        "root": INTRO_PATH,
        "exists": INTRO_PATH.is_dir(),
        "categories": {},
        "root_files": [],
        "subdirectories": [],
        "total_files": 0,
        "total_size": 0,
        "total_lines": 0,
        "scan_time": datetime.now().isoformat(timespec="seconds"),
    }

    if not INTRO_PATH.is_dir():
        return result

    # Collect all subdirectory names
    try:
        result["subdirectories"] = sorted(
            entry.name
            for entry in INTRO_PATH.iterdir()
            if entry.is_dir() and not entry.name.startswith(".")
        )
    except OSError:
        pass

    # Build categories
    categories = get_intro_categories()
    cat_dict: Dict[str, IntroCategory] = {}
    for cat in categories:
        cat_dict[cat.letter] = cat

    result["categories"] = cat_dict

    # Identify root-level files that do not belong to any category
    categorized_names: set[str] = set()
    for cat in categories:
        for f in cat.files:
            categorized_names.add(f.name)

    try:
        for entry in sorted(INTRO_PATH.iterdir()):
            if entry.is_file() and entry.name not in categorized_names:
                ifile = _scan_file(entry, "")
                result["root_files"].append(ifile)
    except OSError:
        pass

    # Aggregate totals
    all_files: list[IntroFile] = list(result["root_files"])
    for cat in categories:
        all_files.extend(cat.files)

    result["total_files"] = len(all_files)
    result["total_size"] = sum(f.size for f in all_files)
    result["total_lines"] = sum(f.lines for f in all_files)

    return result


def get_intro_i_files() -> list[IntroFile]:
    """Return the I1-I12 System Intelligence files with title, size, date, and status.

    Each returned IntroFile has its category set to "I".
    Files are sorted by their numeric index (I1, I2, ... I12).

    Returns:
        Sorted list of IntroFile instances for all I-files found on disk.
    """
    if not INTRO_PATH.is_dir():
        return []

    i_files: list[IntroFile] = []
    pattern = re.compile(r"^I(\d+)_.*\.md$")

    try:
        for entry in INTRO_PATH.iterdir():
            if entry.is_file() and pattern.match(entry.name):
                ifile = _scan_file(entry, "I")
                i_files.append(ifile)
    except OSError:
        return []

    i_files.sort(key=_natural_sort_key)
    return i_files


def get_intro_categories() -> list[IntroCategory]:
    """Return all INTRO file categories (B, C, D, E, F, G, H) plus I-files.

    Each IntroCategory contains a list of its IntroFile members, scanned
    from the real filesystem.

    Returns:
        List of IntroCategory instances, one per category letter.
    """
    if not INTRO_PATH.is_dir():
        return []

    categories: list[IntroCategory] = []

    for letter, display_name, subfolder, description, prefix_re in CATEGORY_DEFINITIONS:
        # Determine the directory to scan
        if subfolder is not None:
            scan_dir = INTRO_PATH / subfolder
        else:
            scan_dir = INTRO_PATH

        cat = IntroCategory(
            letter=letter,
            name=display_name,
            description=description,
        )

        if not scan_dir.is_dir():
            categories.append(cat)
            continue

        file_pattern = re.compile(prefix_re)
        try:
            for entry in sorted(scan_dir.iterdir()):
                if entry.is_file() and file_pattern.match(entry.name):
                    ifile = _scan_file(entry, letter)
                    cat.files.append(ifile)
        except OSError:
            pass

        # Sort files naturally
        cat.files.sort(key=_natural_sort_key)
        categories.append(cat)

    return categories


def get_intro_health() -> IntroHealthReport:
    """Run verification checks on the INTRO folder system and return a health report.

    Checks performed:
        1. INTRO root directory exists
        2. All I-files I1-I12 are present
        3. All category subdirectories exist
        4. B-files B1-B10 are present
        5. C-files C1-C10 are present
        6. D-files D1-D10 are present
        7. NAVIGATION_INDEX.md exists and is non-empty
        8. FOLDER_STRUCTURE_AND_RULES.md exists
        9. verify_master_folders.py exists
        10. Git repository status (clean or dirty)

    Returns:
        IntroHealthReport with all check results and computed score.
    """
    report = IntroHealthReport(
        timestamp=datetime.now().isoformat(timespec="seconds"),
    )

    # Check 1: Root directory exists
    root_exists = INTRO_PATH.is_dir()
    report.checks.append(HealthCheckResult(
        check_name="Root directory exists",
        passed=root_exists,
        message="INTRO root found" if root_exists else f"INTRO root NOT found at {INTRO_PATH}",
    ))

    if not root_exists:
        report.compute_score()
        return report

    # Check 2: I-files I1 through I12
    missing_i: list[str] = []
    for i in range(1, 13):
        pattern = f"I{i}_"
        found = any(
            f.name.startswith(pattern)
            for f in INTRO_PATH.iterdir()
            if f.is_file()
        )
        if not found:
            missing_i.append(f"I{i}")

    report.checks.append(HealthCheckResult(
        check_name="I-files I1-I12 present",
        passed=len(missing_i) == 0,
        message=f"All I-files present" if not missing_i else f"Missing: {', '.join(missing_i)}",
        details=missing_i,
    ))

    # Check 3: Category subdirectories exist
    expected_dirs = [
        "PROJEKTS TERMINALS",
        "PROJEKTS LOKAL ENV",
        "PROJEKTS ARKITEKTUR(TEMPLATES)",
        "OLD PROJEKTS ORIGINAL",
        "LAPTOP KATALOG",
        "ADMIRAL FLEET COLLABORATION",
        "BOGF\u00d8RINGSMAPPE (MED INDHOLDSFORTEGNELSERNE)",
    ]
    missing_dirs: list[str] = []
    for dirname in expected_dirs:
        dirpath = INTRO_PATH / dirname
        if not dirpath.is_dir():
            # Try with special characters (Danish letters)
            alt = INTRO_PATH / dirname.replace("O", "O")
            if not alt.is_dir():
                missing_dirs.append(dirname)

    # Also check with actual encoding
    actual_dirs = {d.name for d in INTRO_PATH.iterdir() if d.is_dir()}
    checked_dirs_found: list[str] = []
    checked_dirs_missing: list[str] = []
    for dirname in expected_dirs:
        # Fuzzy match: check if any actual dir starts with the same prefix
        found = dirname in actual_dirs
        if not found:
            # Try partial match for encoding issues
            prefix = dirname.split("(")[0].split(" ")[0]
            found = any(prefix in d for d in actual_dirs)
        if found:
            checked_dirs_found.append(dirname)
        else:
            checked_dirs_missing.append(dirname)

    report.checks.append(HealthCheckResult(
        check_name="Category subdirectories present",
        passed=len(checked_dirs_missing) == 0,
        message=(
            f"All {len(expected_dirs)} subdirectories found"
            if not checked_dirs_missing
            else f"Missing: {', '.join(checked_dirs_missing)}"
        ),
        details=checked_dirs_missing,
    ))

    # Check 4: B-files B1-B10
    b_dir = INTRO_PATH / "PROJEKTS TERMINALS"
    missing_b: list[str] = []
    if b_dir.is_dir():
        for i in range(1, 11):
            pattern = f"B{i}_"
            found = any(f.name.startswith(pattern) for f in b_dir.iterdir() if f.is_file())
            if not found:
                missing_b.append(f"B{i}")
    else:
        missing_b = [f"B{i}" for i in range(1, 11)]

    report.checks.append(HealthCheckResult(
        check_name="B-files B1-B10 present",
        passed=len(missing_b) == 0,
        message="All B-files present" if not missing_b else f"Missing: {', '.join(missing_b)}",
        details=missing_b,
    ))

    # Check 5: C-files C1-C10
    c_dir = INTRO_PATH / "PROJEKTS LOKAL ENV"
    missing_c: list[str] = []
    if c_dir.is_dir():
        for i in range(1, 11):
            pattern = f"C{i}_"
            found = any(f.name.startswith(pattern) for f in c_dir.iterdir() if f.is_file())
            if not found:
                missing_c.append(f"C{i}")
    else:
        missing_c = [f"C{i}" for i in range(1, 11)]

    report.checks.append(HealthCheckResult(
        check_name="C-files C1-C10 present",
        passed=len(missing_c) == 0,
        message="All C-files present" if not missing_c else f"Missing: {', '.join(missing_c)}",
        details=missing_c,
    ))

    # Check 6: D-files D1-D10
    d_dir = INTRO_PATH / "PROJEKTS ARKITEKTUR(TEMPLATES)"
    missing_d: list[str] = []
    if d_dir.is_dir():
        for i in range(1, 11):
            pattern = f"D{i}_"
            found = any(f.name.startswith(pattern) for f in d_dir.iterdir() if f.is_file())
            if not found:
                missing_d.append(f"D{i}")
    else:
        missing_d = [f"D{i}" for i in range(1, 11)]

    report.checks.append(HealthCheckResult(
        check_name="D-files D1-D10 present",
        passed=len(missing_d) == 0,
        message="All D-files present" if not missing_d else f"Missing: {', '.join(missing_d)}",
        details=missing_d,
    ))

    # Check 7: NAVIGATION_INDEX.md exists and is non-empty
    nav_index = INTRO_PATH / "NAVIGATION_INDEX.md"
    nav_exists = nav_index.is_file()
    nav_size = nav_index.stat().st_size if nav_exists else 0
    report.checks.append(HealthCheckResult(
        check_name="NAVIGATION_INDEX.md present",
        passed=nav_exists and nav_size > 100,
        message=(
            f"NAVIGATION_INDEX.md found ({nav_size} bytes)"
            if nav_exists
            else "NAVIGATION_INDEX.md NOT found"
        ),
    ))

    # Check 8: FOLDER_STRUCTURE_AND_RULES.md exists
    rules_file = INTRO_PATH / "FOLDER_STRUCTURE_AND_RULES.md"
    report.checks.append(HealthCheckResult(
        check_name="FOLDER_STRUCTURE_AND_RULES.md present",
        passed=rules_file.is_file(),
        message=(
            "FOLDER_STRUCTURE_AND_RULES.md found"
            if rules_file.is_file()
            else "FOLDER_STRUCTURE_AND_RULES.md NOT found"
        ),
    ))

    # Check 9: verify_master_folders.py exists
    verify_script = INTRO_PATH / "verify_master_folders.py"
    report.checks.append(HealthCheckResult(
        check_name="verify_master_folders.py present",
        passed=verify_script.is_file(),
        message=(
            "Verification script found"
            if verify_script.is_file()
            else "Verification script NOT found"
        ),
    ))

    # Check 10: Git status
    git_clean = False
    git_message = "Git check not performed"
    try:
        git_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(INTRO_PATH),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if git_result.returncode == 0:
            dirty_lines = [
                line for line in git_result.stdout.strip().splitlines() if line.strip()
            ]
            if not dirty_lines:
                git_clean = True
                git_message = "Git working tree is clean"
            else:
                git_message = f"Git has {len(dirty_lines)} uncommitted change(s)"
        else:
            git_message = "Not a git repository or git error"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        git_message = "Could not run git command"

    report.checks.append(HealthCheckResult(
        check_name="Git status clean",
        passed=git_clean,
        message=git_message,
    ))

    report.compute_score()
    return report


def parse_intro_navigation_index() -> Dict[str, Any]:
    """Read and parse NAVIGATION_INDEX.md, returning structured data.

    Returns a dict with keys:
        "exists": bool
        "total_documents": int
        "total_lines": int
        "unique_keywords": int
        "entries_by_category": dict mapping category code to list of NavigationEntry
        "all_entries": list of all NavigationEntry instances
        "parse_errors": list of error messages encountered during parsing
    """
    nav_path = INTRO_PATH / "NAVIGATION_INDEX.md"

    result: Dict[str, Any] = {
        "exists": nav_path.is_file(),
        "total_documents": 0,
        "total_lines": 0,
        "unique_keywords": 0,
        "entries_by_category": {},
        "all_entries": [],
        "parse_errors": [],
    }

    if not nav_path.is_file():
        return result

    try:
        content = nav_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        result["parse_errors"].append(f"Could not read file: {exc}")
        return result

    lines = content.splitlines()

    # Parse summary statistics from the header
    for line in lines[:30]:
        doc_match = re.search(r"\*\*Total Documents:\*\*\s*(\d+)", line)
        if doc_match:
            result["total_documents"] = int(doc_match.group(1))

        lines_match = re.search(r"\*\*Total Lines:\*\*\s*([\d,]+)", line)
        if lines_match:
            result["total_lines"] = int(lines_match.group(1).replace(",", ""))

        kw_match = re.search(r"\*\*Unique Keywords:\*\*\s*([\d,]+)", line)
        if kw_match:
            result["unique_keywords"] = int(kw_match.group(1).replace(",", "").replace("+", ""))

    # Parse document entries
    # Format per entry:
    #   ### CATEGORY (N files)
    #   - **FILENAME.md** (NNN lines) [optional: (arkiveret)]
    #     - Location: `path`
    #     - Main topic: TOPIC
    #     - Sections: SEC1, SEC2, ...

    current_category = ""
    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect category header: ### CODE (N files)
        cat_match = re.match(r"^###\s+(\S+)\s+\((\d+)\s+files?\)", line)
        if cat_match:
            current_category = cat_match.group(1)
            if current_category not in result["entries_by_category"]:
                result["entries_by_category"][current_category] = []
            i += 1
            continue

        # Detect file entry: - **FILENAME** (NNN lines) [optional: (arkiveret)]
        entry_match = re.match(
            r"^-\s+\*\*(.+?)\*\*\s+\((\d[\d,]*)\s+lines?\s*(?:est\.)?\)",
            line,
        )
        if entry_match:
            filename = entry_match.group(1)
            line_count_str = entry_match.group(2).replace(",", "")
            line_count = int(line_count_str) if line_count_str.isdigit() else 0
            archived = "(arkiveret)" in line.lower()

            entry = NavigationEntry(
                filename=filename,
                lines=line_count,
                location="",
                main_topic="",
                sections=[],
                category_code=current_category,
                archived=archived,
            )

            # Parse sub-fields on following lines
            j = i + 1
            while j < len(lines) and lines[j].startswith("  "):
                subline = lines[j].strip()

                loc_match = re.match(r"^-\s+Location:\s+`?(.+?)`?\s*$", subline)
                if loc_match:
                    entry.location = loc_match.group(1)
                    j += 1
                    continue

                topic_match = re.match(r"^-\s+Main topic:\s+(.+)$", subline)
                if topic_match:
                    entry.main_topic = topic_match.group(1).strip()
                    j += 1
                    continue

                sec_match = re.match(r"^-\s+Sections:\s+(.+)$", subline)
                if sec_match:
                    raw_sections = sec_match.group(1)
                    entry.sections = [s.strip() for s in raw_sections.split(",")]
                    j += 1
                    continue

                j += 1

            result["all_entries"].append(entry)
            if current_category not in result["entries_by_category"]:
                result["entries_by_category"][current_category] = []
            result["entries_by_category"][current_category].append(entry)

            i = j
            continue

        i += 1

    return result


# ---------------------------------------------------------------------------
# CONVENIENCE / SUMMARY FUNCTIONS
# ---------------------------------------------------------------------------

def get_intro_summary() -> Dict[str, Any]:
    """Return a quick summary of the INTRO system for sidebar display.

    Returns a dict with:
        "available": bool
        "i_file_count": int
        "category_count": int
        "total_files": int
        "total_size_human": str
        "health_score": float
        "latest_change": str
    """
    if not INTRO_PATH.is_dir():
        return {
            "available": False,
            "i_file_count": 0,
            "category_count": 0,
            "total_files": 0,
            "total_size_human": "0 B",
            "health_score": 0.0,
            "latest_change": "",
        }

    i_files = get_intro_i_files()
    categories = get_intro_categories()
    total_files = sum(cat.file_count for cat in categories)
    total_size = sum(cat.total_size for cat in categories)

    # Human-readable size
    if total_size < 1024:
        size_human = f"{total_size} B"
    elif total_size < 1024 * 1024:
        size_human = f"{total_size / 1024:.1f} KB"
    else:
        size_human = f"{total_size / (1024 * 1024):.1f} MB"

    # Find latest modification across all categories
    all_timestamps = [cat.latest_modified for cat in categories if cat.latest_modified]
    latest = max(all_timestamps) if all_timestamps else ""

    return {
        "available": True,
        "i_file_count": len(i_files),
        "category_count": len(categories),
        "total_files": total_files,
        "total_size_human": size_human,
        "health_score": 0.0,  # Computed lazily to avoid slowdown
        "latest_change": latest,
    }


def get_i_file_title(number: int) -> str:
    """Return the short title for an I-file by its number (1-12)."""
    entry = I_FILE_TITLES.get(number)
    return entry[0] if entry else f"I{number}"


def get_i_file_description(number: int) -> str:
    """Return the description for an I-file by its number (1-12)."""
    entry = I_FILE_TITLES.get(number)
    return entry[1] if entry else ""


# ---------------------------------------------------------------------------
# MAIN (for standalone testing)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("  INTRO FOLDER SYSTEM -- DATA MODEL VERIFICATION")
    print("=" * 70)
    print()

    # Test 1: Check INTRO path
    print(f"INTRO_PATH: {INTRO_PATH}")
    print(f"  Exists: {INTRO_PATH.is_dir()}")
    print()

    # Test 2: I-files
    print("--- I-FILES (System Intelligence) ---")
    i_files = get_intro_i_files()
    for f in i_files:
        title = get_i_file_title(f.category_number or 0)
        print(f"  {f.name:<50s}  {f.size_human:>10s}  {f.lines:>5d} lines  [{f.status}]  {title}")
    print(f"  Total: {len(i_files)} I-files")
    print()

    # Test 3: Categories
    print("--- CATEGORIES ---")
    categories = get_intro_categories()
    for cat in categories:
        print(f"  [{cat.letter}] {cat.name:<30s}  {cat.file_count:>3d} files  {cat.total_lines:>6d} lines  Last: {cat.latest_modified}")
    print()

    # Test 4: Navigation Index
    print("--- NAVIGATION INDEX ---")
    nav = parse_intro_navigation_index()
    print(f"  Exists: {nav['exists']}")
    print(f"  Total documents: {nav['total_documents']}")
    print(f"  Total lines:     {nav['total_lines']}")
    print(f"  Unique keywords: {nav['unique_keywords']}")
    print(f"  Categories parsed: {len(nav['entries_by_category'])}")
    print(f"  Entries parsed:    {len(nav['all_entries'])}")
    if nav["parse_errors"]:
        for err in nav["parse_errors"]:
            print(f"  ERROR: {err}")
    print()

    # Test 5: Health
    print("--- HEALTH CHECK ---")
    health = get_intro_health()
    for check in health.checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"  [{status}] {check.check_name}: {check.message}")
        for detail in check.details:
            print(f"         - {detail}")
    print(f"  Overall Score: {health.overall_score:.1f}%")
    print(f"  Errors: {health.errors}  Warnings: {health.warnings}")
    print()

    # Test 6: Full structure
    print("--- FULL STRUCTURE ---")
    structure = get_intro_structure()
    print(f"  Root: {structure['root']}")
    print(f"  Exists: {structure['exists']}")
    print(f"  Total files: {structure['total_files']}")
    print(f"  Total size: {structure['total_size']} bytes")
    print(f"  Total lines: {structure['total_lines']}")
    print(f"  Subdirectories: {len(structure['subdirectories'])}")
    for d in structure["subdirectories"]:
        print(f"    - {d}")
    print(f"  Root files (uncategorized): {len(structure['root_files'])}")
    for f in structure["root_files"]:
        print(f"    - {f.name} ({f.size_human})")
    print()

    # Test 7: Summary
    print("--- QUICK SUMMARY ---")
    summary = get_intro_summary()
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print()

    print("=" * 70)
    print("  DATA MODEL VERIFICATION COMPLETE")
    print("=" * 70)
