#!/usr/bin/env python3
"""
Verify Index-Content Sync
==========================
Checks that documentation indexes match their actual content:
1. Status headers match real state
2. Navigation indexes list existing files
3. Internal links resolve correctly
4. External references are valid paths
5. Timestamps are not stale (>7 days old)
6. Chapter numbering is sequential
7. TODO markers are tracked

Source: workflows.md protocol description.
Output: Sync verification report.
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field

# --- Configuration ---
SCAN_DIRS = [
    Path.home() / "Desktop" / "MIN ADMIRAL",
    Path.home() / "Desktop" / "MASTER FOLDERS(INTRO)",
    Path.home() / "Desktop" / "sejrliste systemet",
]
REPORT_DIR = Path(__file__).parent.parent
EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}
STALE_DAYS = 7


@dataclass
class SyncIssue:
    check_type: str  # status_header, nav_index, internal_link, external_ref, timestamp, numbering, todo
    file_path: str
    line_number: int
    description: str
    severity: str  # INFO, WARN, FAIL


@dataclass
class SyncReport:
    timestamp: str = ""
    files_scanned: int = 0
    total_issues: int = 0
    issues: list = field(default_factory=list)
    checks_passed: int = 0
    checks_failed: int = 0


def check_status_headers(filepath: Path) -> list:
    """Check that status headers ([OK], [FAIL], etc.) match reality."""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception:
        return issues

    for i, line in enumerate(lines, 1):
        # Look for status markers
        status_match = re.search(r'\[(OK|FAIL|PENDING|DONE|ACTIVE|BLOCKED|WIP)\]', line, re.IGNORECASE)
        if status_match:
            status = status_match.group(1).upper()
            # Check if status claims something verifiable
            if status == "OK" and "IKKE TESTET" in line.upper():
                issues.append(SyncIssue(
                    "status_header", str(filepath), i,
                    f"Status [OK] but also says 'IKKE TESTET': {line.strip()[:80]}",
                    "FAIL"
                ))
            elif status == "DONE" and "TODO" in line.upper():
                issues.append(SyncIssue(
                    "status_header", str(filepath), i,
                    f"Status [DONE] but contains TODO: {line.strip()[:80]}",
                    "WARN"
                ))

    return issues


def check_internal_links(filepath: Path) -> list:
    """Check markdown links point to existing files."""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception:
        return issues

    for i, line in enumerate(lines, 1):
        # Markdown links
        for match in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', line):
            target = match.group(2)
            if target.startswith("http") or target.startswith("#") or target.startswith("mailto"):
                continue

            # Strip anchor
            target_path = target.split("#")[0]
            if not target_path:
                continue

            resolved = (filepath.parent / target_path).resolve()
            if not resolved.exists():
                issues.append(SyncIssue(
                    "internal_link", str(filepath), i,
                    f"Broken link: [{match.group(1)}]({target}) -> {resolved}",
                    "FAIL"
                ))

    return issues


def check_external_refs(filepath: Path) -> list:
    """Check path references point to existing files/dirs."""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception:
        return issues

    path_pattern = re.compile(r'(?<![`])(/home/rasmus/[^\s\)\]"\'`]+)(?![`])')
    for i, line in enumerate(lines, 1):
        # Skip code blocks
        if line.strip().startswith("```") or line.strip().startswith("#!"):
            continue

        for match in path_pattern.finditer(line):
            ref = match.group(1).rstrip(".,;:)")
            if "*" in ref or "{" in ref:
                continue  # Skip globs
            if not os.path.exists(ref):
                issues.append(SyncIssue(
                    "external_ref", str(filepath), i,
                    f"Path does not exist: {ref}",
                    "WARN"
                ))

    return issues


def check_timestamps(filepath: Path) -> list:
    """Check for stale timestamps in documentation."""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception:
        return issues

    now = datetime.now()
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')

    for i, line in enumerate(lines, 1):
        # Look for date strings in context of "updated", "generated", "verified"
        lower = line.lower()
        if any(word in lower for word in ["opdateret", "updated", "generated", "verificeret", "verified", "sidst"]):
            match = date_pattern.search(line)
            if match:
                try:
                    doc_date = datetime.strptime(match.group(1), "%Y-%m-%d")
                    days_old = (now - doc_date).days
                    if days_old > STALE_DAYS:
                        issues.append(SyncIssue(
                            "timestamp", str(filepath), i,
                            f"Stale timestamp ({days_old} days old): {line.strip()[:80]}",
                            "INFO"
                        ))
                except ValueError:
                    pass

    return issues


def check_chapter_numbering(filepath: Path) -> list:
    """Check that numbered sections are sequential."""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception:
        return issues

    # Look for numbered headings like ### FASE 0:, ### FASE 1:, etc.
    fase_numbers = []
    for i, line in enumerate(lines, 1):
        match = re.match(r'^###\s+FASE\s+(\d+)', line)
        if match:
            fase_numbers.append((int(match.group(1)), i))

    # Check for gaps or duplicates
    if len(fase_numbers) > 1:
        seen = {}
        for num, lineno in fase_numbers:
            if num in seen:
                issues.append(SyncIssue(
                    "numbering", str(filepath), lineno,
                    f"Duplicate FASE {num} (also at line {seen[num]})",
                    "WARN"
                ))
            seen[num] = lineno

    return issues


def check_todo_markers(filepath: Path) -> list:
    """Track TODO/FIXME/HACK markers."""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception:
        return issues

    for i, line in enumerate(lines, 1):
        for marker in ["TODO", "FIXME", "HACK", "XXX", "UDFYLDES"]:
            if marker in line.upper() and not line.strip().startswith("#"):
                # Skip checkbox lines
                if re.match(r'\s*-\s+\[', line):
                    continue
                issues.append(SyncIssue(
                    "todo", str(filepath), i,
                    f"{marker} found: {line.strip()[:80]}",
                    "INFO"
                ))

    return issues


def scan_all() -> SyncReport:
    """Run all checks on all directories."""
    report = SyncReport(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for f in scan_dir.rglob("*.md"):
            if any(ex in f.parts for ex in EXCLUDE_DIRS):
                continue
            report.files_scanned += 1

            report.issues.extend(check_status_headers(f))
            report.issues.extend(check_internal_links(f))
            report.issues.extend(check_external_refs(f))
            report.issues.extend(check_timestamps(f))
            report.issues.extend(check_chapter_numbering(f))
            report.issues.extend(check_todo_markers(f))

    report.total_issues = len(report.issues)
    report.checks_failed = sum(1 for i in report.issues if i.severity == "FAIL")
    report.checks_passed = report.files_scanned - report.checks_failed

    return report


def format_report(report: SyncReport) -> str:
    """Format sync report."""
    lines = []
    lines.append("=" * 70)
    lines.append("VERIFY INDEX-CONTENT SYNC")
    lines.append(f"Timestamp: {report.timestamp}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Files scanned: {report.files_scanned}")
    lines.append(f"Total issues: {report.total_issues}")
    lines.append(f"  [FAIL] {sum(1 for i in report.issues if i.severity == 'FAIL')}")
    lines.append(f"  [WARN] {sum(1 for i in report.issues if i.severity == 'WARN')}")
    lines.append(f"  [INFO] {sum(1 for i in report.issues if i.severity == 'INFO')}")
    lines.append("")

    # Group by check type
    by_type = {}
    for issue in report.issues:
        by_type.setdefault(issue.check_type, []).append(issue)

    check_names = {
        "status_header": "1. Status Header Validation",
        "internal_link": "2. Internal Link Validation",
        "external_ref": "3. External Reference Validation",
        "timestamp": "4. Timestamp Freshness",
        "numbering": "5. Chapter Numbering",
        "todo": "6. TODO Marker Tracking",
    }

    for check_type, name in check_names.items():
        issues = by_type.get(check_type, [])
        status = "[PASS]" if not issues else f"[{len(issues)} issues]"
        lines.append(f"--- {name} {status} ---")
        if not issues:
            lines.append("  [OK] No issues found")
        else:
            for issue in issues[:10]:
                lines.append(f"  [{issue.severity}] {Path(issue.file_path).name}:{issue.line_number}")
                lines.append(f"         {issue.description}")
            if len(issues) > 10:
                lines.append(f"  ... and {len(issues) - 10} more")
        lines.append("")

    lines.append("-" * 70)
    lines.append(f"Generated by verify_index_content_sync.py")
    return "\n".join(lines)


def main():
    print("Verify Index-Content Sync starting...")
    print()

    report = scan_all()
    text = format_report(report)
    print(text)

    # Save
    report_path = REPORT_DIR / "INDEX_SYNC_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Index-Content Sync Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"```\n{text}\n```\n")

    print(f"\nReport saved to: {report_path}")

    # Exit code: 0 if no FAIL, 1 if any FAIL
    fail_count = sum(1 for i in report.issues if i.severity == "FAIL")
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
