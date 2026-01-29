#!/usr/bin/env python3
"""
Admiral Compliance Check — Rule Compliance Scanner
===================================================
Scans context system, documentation, and scripts for rule compliance.
Runs automatically at session start.

Output: Compliance report with rule status per category.

Rules source: ~/.claude/.context/core/rules.md
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field

# --- Configuration ---
CONTEXT_DIR = Path.home() / ".claude" / ".context"
CORE_DIR = CONTEXT_DIR / "core"
MIN_ADMIRAL_DIR = Path.home() / "Desktop" / "MIN ADMIRAL"
SEJRLISTE_DIR = Path.home() / "Desktop" / "sejrliste systemet"
MASTER_FOLDERS = Path.home() / "Desktop" / "MASTER FOLDERS(INTRO)"
REPORT_DIR = Path(__file__).parent.parent

# --- Data Classes ---
@dataclass
class RuleCheck:
    rule_id: str
    name: str
    status: str  # PASS, FAIL, WARN, SKIP
    details: str
    evidence: str = ""

@dataclass
class ComplianceReport:
    timestamp: str = ""
    total_rules: int = 0
    passing: int = 0
    failing: int = 0
    warnings: int = 0
    skipped: int = 0
    checks: list = field(default_factory=list)
    score_pct: float = 0.0


def check_context_files_exist() -> RuleCheck:
    """Rule -9: Context system must exist and be loadable."""
    required = [
        "rules.md", "identity.md", "preferences.md",
        "workflows.md", "relationships.md", "triggers.md",
        "projects.md", "session.md", "journal.md"
    ]
    missing = []
    for f in required:
        path = CORE_DIR / f
        if not path.exists():
            missing.append(f)
        elif path.stat().st_size == 0:
            missing.append(f"{f} (EMPTY)")

    if not missing:
        return RuleCheck(
            "-9", "Context files exist",
            "PASS", f"All {len(required)} core files present and non-empty",
            f"Files checked: {', '.join(required)}"
        )
    return RuleCheck(
        "-9", "Context files exist",
        "FAIL", f"Missing/empty: {', '.join(missing)}",
        f"Expected in {CORE_DIR}"
    )


def check_context_file_sizes() -> RuleCheck:
    """Rule 29: Context files under 25K tokens (~100KB)."""
    oversized = []
    max_bytes = 100_000  # ~25K tokens
    for f in CORE_DIR.iterdir():
        if f.suffix == ".md" and not f.name.startswith("journal_archive"):
            size = f.stat().st_size
            if size > max_bytes:
                oversized.append(f"{f.name} ({size:,} bytes)")

    if not oversized:
        return RuleCheck(
            "29", "Context file sizes within limits",
            "PASS", "All core .md files under 100KB",
            f"Directory: {CORE_DIR}"
        )
    return RuleCheck(
        "29", "Context file sizes within limits",
        "WARN", f"Oversized: {', '.join(oversized)}",
        "Risk: auto-load failure"
    )


def check_no_emoji_in_docs() -> RuleCheck:
    """Rule -44: No emoji in documentation."""
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F9FF"
        "\U00002702-\U000027B0"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002600-\U000026FF"
        "]+", flags=re.UNICODE
    )
    violations = []
    search_dirs = [MIN_ADMIRAL_DIR, CORE_DIR]
    for d in search_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*.md"):
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                matches = emoji_pattern.findall(content)
                if matches:
                    violations.append(f"{f.name}: {len(matches)} emoji found")
            except Exception:
                pass

    if not violations:
        return RuleCheck(
            "-44", "No emoji in documentation",
            "PASS", "Zero emoji found in MIN ADMIRAL + context",
            f"Scanned: {', '.join(str(d) for d in search_dirs)}"
        )
    return RuleCheck(
        "-44", "No emoji in documentation",
        "FAIL", f"{len(violations)} files with emoji: {'; '.join(violations[:5])}",
        "Rule: Professional enterprise level"
    )


def check_sejrliste_active() -> RuleCheck:
    """Rule 3: One thing at a time — active sejrlister should exist."""
    active_dir = SEJRLISTE_DIR / "10_ACTIVE"
    if not active_dir.exists():
        return RuleCheck(
            "3", "Active sejrlister exist",
            "FAIL", "10_ACTIVE directory not found",
            f"Expected: {active_dir}"
        )
    sejrlister = [d for d in active_dir.iterdir() if d.is_dir()]
    with_claude = [d.name for d in sejrlister if (d / "CLAUDE.md").exists()]
    without_claude = [d.name for d in sejrlister if not (d / "CLAUDE.md").exists()]

    if without_claude:
        return RuleCheck(
            "3", "Active sejrlister have CLAUDE.md",
            "WARN",
            f"{len(with_claude)} have CLAUDE.md, {len(without_claude)} missing: {', '.join(without_claude[:3])}",
            f"Active: {active_dir}"
        )
    return RuleCheck(
        "3", "Active sejrlister have CLAUDE.md",
        "PASS", f"{len(with_claude)} active sejrlister, all with CLAUDE.md",
        f"Active: {active_dir}"
    )


def check_min_admiral_exists() -> RuleCheck:
    """Rule -5: Permanent documentation must be indexed and findable."""
    if not MIN_ADMIRAL_DIR.exists():
        return RuleCheck(
            "-5", "MIN ADMIRAL directory exists",
            "FAIL", "MIN ADMIRAL directory not found",
            f"Expected: {MIN_ADMIRAL_DIR}"
        )
    files = list(MIN_ADMIRAL_DIR.rglob("*.md"))
    return RuleCheck(
        "-5", "MIN ADMIRAL directory exists",
        "PASS", f"{len(files)} .md files in MIN ADMIRAL",
        f"Path: {MIN_ADMIRAL_DIR}"
    )


def check_git_status() -> RuleCheck:
    """Rule -28a: Work complete = git complete."""
    results = []
    repos = []

    # Check known repos
    for repo_path in [SEJRLISTE_DIR, MIN_ADMIRAL_DIR, MASTER_FOLDERS]:
        if not repo_path.exists():
            continue
        git_dir = repo_path / ".git"
        if not git_dir.exists():
            continue
        repos.append(repo_path)
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path), "status", "--porcelain"],
                capture_output=True, text=True, timeout=10
            )
            dirty_count = len([l for l in result.stdout.strip().split("\n") if l.strip()])
            if dirty_count > 0:
                results.append(f"{repo_path.name}: {dirty_count} uncommitted")
            else:
                results.append(f"{repo_path.name}: clean")
        except Exception as e:
            results.append(f"{repo_path.name}: error ({e})")

    if not repos:
        return RuleCheck("-28a", "Git repos clean", "SKIP", "No git repos found", "")

    dirty = [r for r in results if "uncommitted" in r]
    if dirty:
        return RuleCheck(
            "-28a", "Git repos clean",
            "WARN", f"{len(dirty)} dirty repos: {'; '.join(dirty)}",
            f"Repos checked: {', '.join(r.name for r in repos)}"
        )
    return RuleCheck(
        "-28a", "Git repos clean",
        "PASS", "All repos clean",
        f"Repos: {', '.join(r.name for r in repos)}"
    )


def check_documentation_accuracy() -> RuleCheck:
    """Rule -42: No lies in documentation — check for unverified claims."""
    suspect_patterns = [
        (r"\b100%\s+success", "unverified 100% claims"),
        (r"\b2\.1M\s+files", "organic production claims (Rule -19)"),
        (r"\b24/7\b.*running", "24/7 running claims"),
        (r"\bALWAYS\s+available", "always available claims"),
    ]
    violations = []
    if MIN_ADMIRAL_DIR.exists():
        for f in MIN_ADMIRAL_DIR.rglob("*.md"):
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                for pattern, desc in suspect_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        violations.append(f"{f.name}: {desc}")
            except Exception:
                pass

    if not violations:
        return RuleCheck(
            "-42", "Documentation accuracy",
            "PASS", "No suspect unverified claims found",
            f"Scanned MIN ADMIRAL .md files"
        )
    return RuleCheck(
        "-42", "Documentation accuracy",
        "WARN", f"{len(violations)} potential issues: {'; '.join(violations[:5])}",
        "Review manually for accuracy"
    )


def check_master_folders_exist() -> RuleCheck:
    """Rule -14: MASTER FOLDERS documentation must exist and be accurate."""
    if not MASTER_FOLDERS.exists():
        return RuleCheck(
            "-14", "MASTER FOLDERS exists",
            "FAIL", "MASTER FOLDERS(INTRO) not found",
            f"Expected: {MASTER_FOLDERS}"
        )
    files = list(MASTER_FOLDERS.rglob("*.md"))
    folders = [d for d in MASTER_FOLDERS.iterdir() if d.is_dir()]
    return RuleCheck(
        "-14", "MASTER FOLDERS exists",
        "PASS", f"{len(files)} .md files in {len(folders)} folders",
        f"Path: {MASTER_FOLDERS}"
    )


def check_archives_outside_core() -> RuleCheck:
    """Rule 29: Archive files must be stored OUTSIDE core/ directory."""
    archive_in_core = []
    for f in CORE_DIR.iterdir():
        if "archive" in f.name.lower() and f.suffix == ".md":
            size = f.stat().st_size
            if size > 50_000:  # Only flag large ones
                archive_in_core.append(f"{f.name} ({size:,} bytes)")

    if not archive_in_core:
        return RuleCheck(
            "29b", "Archives outside core/",
            "PASS", "No large archive files in core/",
            f"Dir: {CORE_DIR}"
        )
    return RuleCheck(
        "29b", "Archives outside core/",
        "WARN", f"Large archives in core/: {', '.join(archive_in_core)}",
        "Should be in archives/ directory"
    )


def run_all_checks() -> ComplianceReport:
    """Run all compliance checks and build report."""
    report = ComplianceReport(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    checks = [
        check_context_files_exist,
        check_context_file_sizes,
        check_no_emoji_in_docs,
        check_sejrliste_active,
        check_min_admiral_exists,
        check_git_status,
        check_documentation_accuracy,
        check_master_folders_exist,
        check_archives_outside_core,
    ]

    for check_fn in checks:
        try:
            result = check_fn()
        except Exception as e:
            result = RuleCheck("?", check_fn.__name__, "FAIL", f"Error: {e}")
        report.checks.append(result)

    report.total_rules = len(report.checks)
    report.passing = sum(1 for c in report.checks if c.status == "PASS")
    report.failing = sum(1 for c in report.checks if c.status == "FAIL")
    report.warnings = sum(1 for c in report.checks if c.status == "WARN")
    report.skipped = sum(1 for c in report.checks if c.status == "SKIP")
    applicable = report.total_rules - report.skipped
    report.score_pct = (report.passing / applicable * 100) if applicable > 0 else 0

    return report


def format_report(report: ComplianceReport) -> str:
    """Format compliance report as readable text."""
    lines = []
    lines.append("=" * 70)
    lines.append("ADMIRAL COMPLIANCE CHECK")
    lines.append(f"Timestamp: {report.timestamp}")
    lines.append("=" * 70)
    lines.append("")

    # Summary
    lines.append(f"Score: {report.score_pct:.0f}% ({report.passing}/{report.total_rules - report.skipped} rules compliant)")
    lines.append(f"  [PASS] {report.passing}  [FAIL] {report.failing}  [WARN] {report.warnings}  [SKIP] {report.skipped}")
    lines.append("")

    # Details
    lines.append("-" * 70)
    for check in report.checks:
        status_label = {
            "PASS": "[PASS]",
            "FAIL": "[FAIL]",
            "WARN": "[WARN]",
            "SKIP": "[SKIP]"
        }.get(check.status, "[????]")

        lines.append(f"  {status_label} Rule {check.rule_id}: {check.name}")
        lines.append(f"         {check.details}")
        if check.evidence:
            lines.append(f"         Evidence: {check.evidence}")
        lines.append("")

    lines.append("-" * 70)
    lines.append(f"Generated by admiral_compliance_check.py")
    lines.append(f"Source: {__file__}")
    return "\n".join(lines)


def save_report(report: ComplianceReport, text: str):
    """Save report as JSON and text."""
    report_path = REPORT_DIR / "COMPLIANCE_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Admiral Compliance Report\n\n")
        f.write(f"**Generated:** {report.timestamp}\n\n")
        f.write(f"```\n{text}\n```\n")

    json_path = REPORT_DIR / "compliance_report.json"
    data = {
        "timestamp": report.timestamp,
        "score_pct": report.score_pct,
        "total": report.total_rules,
        "passing": report.passing,
        "failing": report.failing,
        "warnings": report.warnings,
        "checks": [
            {
                "rule_id": c.rule_id,
                "name": c.name,
                "status": c.status,
                "details": c.details,
                "evidence": c.evidence,
            }
            for c in report.checks
        ]
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    print("Admiral Compliance Check starting...")
    print(f"Scanning: context, MIN ADMIRAL, sejrlister, MASTER FOLDERS")
    print()

    report = run_all_checks()
    text = format_report(report)
    print(text)

    save_report(report, text)
    print(f"\nReport saved to: {REPORT_DIR / 'COMPLIANCE_REPORT.md'}")
    print(f"JSON saved to:   {REPORT_DIR / 'compliance_report.json'}")

    # Exit code: 0 if no FAIL, 1 if any FAIL
    sys.exit(0 if report.failing == 0 else 1)


if __name__ == "__main__":
    main()
