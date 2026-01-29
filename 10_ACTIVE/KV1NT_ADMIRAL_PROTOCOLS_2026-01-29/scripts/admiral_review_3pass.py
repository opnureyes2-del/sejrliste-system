#!/usr/bin/env python3
"""
Admiral 3-Pass Review System
=============================
Guides through the 3-pass review process for any sejrliste.
Reads SEJR_LISTE.md, calculates real progress, and verifies completion.

Pass 1: PLANNING (identify and document)
Pass 2: EXECUTION (build and implement)
Pass 3: VERIFICATION (300% FAERDIGT)

Output: Verified status + score per pass.
"""

import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field

# --- Configuration ---
SEJRLISTE_DIR = Path.home() / "Desktop" / "sejrliste systemet"
ACTIVE_DIR = SEJRLISTE_DIR / "10_ACTIVE"
ARCHIVE_DIR = SEJRLISTE_DIR / "20_ARCHIVED"
REPORT_DIR = Path(__file__).parent.parent


@dataclass
class CheckboxItem:
    text: str
    checked: bool
    line_number: int
    pass_number: int = 0
    section: str = ""


@dataclass
class PassReview:
    pass_number: int
    total: int = 0
    checked: int = 0
    unchecked: int = 0
    pct: float = 0.0
    score: int = 0
    items: list = field(default_factory=list)


@dataclass
class SejrReview:
    name: str
    path: str
    passes: list = field(default_factory=list)
    total_checkboxes: int = 0
    total_checked: int = 0
    overall_pct: float = 0.0
    total_score: int = 0


def parse_sejr_liste(filepath: Path) -> SejrReview:
    """Parse a SEJR_LISTE.md file and extract checkbox status per pass."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception as e:
        return SejrReview(name="ERROR", path=str(filepath))

    review = SejrReview(
        name=filepath.parent.name,
        path=str(filepath)
    )

    current_pass = 0
    current_section = ""
    pass_data = {1: PassReview(1), 2: PassReview(2), 3: PassReview(3)}

    for i, line in enumerate(lines, 1):
        # Detect pass sections
        if re.match(r'^##\s+PASS\s+1[:\s]', line, re.IGNORECASE):
            current_pass = 1
        elif re.match(r'^##\s+PASS\s+2[:\s]', line, re.IGNORECASE):
            current_pass = 2
        elif re.match(r'^##\s+PASS\s+3[:\s]', line, re.IGNORECASE):
            current_pass = 3
        elif re.match(r'^##\s+PASS\s+\d\s+REVIEW', line, re.IGNORECASE):
            # Pass review sections belong to current pass
            pass

        # Detect section headers
        section_match = re.match(r'^###\s+(.+)', line)
        if section_match:
            current_section = section_match.group(1).strip()

        # Detect checkboxes
        checkbox_match = re.match(r'^(\s*)-\s+\[([ xX])\]\s+(.+)', line)
        if checkbox_match and current_pass > 0:
            checked = checkbox_match.group(2).lower() == "x"
            text = checkbox_match.group(3).strip()

            item = CheckboxItem(
                text=text,
                checked=checked,
                line_number=i,
                pass_number=current_pass,
                section=current_section
            )

            if current_pass in pass_data:
                pass_data[current_pass].items.append(item)
                pass_data[current_pass].total += 1
                if checked:
                    pass_data[current_pass].checked += 1
                else:
                    pass_data[current_pass].unchecked += 1

    # Calculate percentages and scores
    for p in [1, 2, 3]:
        pd = pass_data[p]
        pd.pct = (pd.checked / pd.total * 100) if pd.total > 0 else 0

        # Extract score from REVIEW section if present
        score_pattern = re.compile(r'Score:\s*\*?\*?(\d+)/10', re.IGNORECASE)
        for item in pd.items:
            match = score_pattern.search(item.text)
            if match:
                pd.score = int(match.group(1))

        review.passes.append(pd)
        review.total_checkboxes += pd.total
        review.total_checked += pd.checked
        review.total_score += pd.score

    review.overall_pct = (review.total_checked / review.total_checkboxes * 100) if review.total_checkboxes > 0 else 0

    return review


def format_progress_bar(pct: float, width: int = 20) -> str:
    """Create text progress bar."""
    filled = int(width * pct / 100)
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {pct:.0f}%"


def format_review(review: SejrReview) -> str:
    """Format a single sejrliste review."""
    lines = []
    lines.append(f"  {review.name}")
    lines.append(f"  Path: {review.path}")
    lines.append(f"  Overall: {format_progress_bar(review.overall_pct)} ({review.total_checked}/{review.total_checkboxes})")
    lines.append(f"  Total Score: {review.total_score}/30 (minimum 24 for archive)")
    lines.append("")

    for pd in review.passes:
        status = "COMPLETE" if pd.pct == 100 else "IN PROGRESS" if pd.checked > 0 else "NOT STARTED"
        lines.append(f"    Pass {pd.pass_number}: {format_progress_bar(pd.pct)} ({pd.checked}/{pd.total}) [{status}]")
        if pd.score > 0:
            lines.append(f"             Score: {pd.score}/10")

        # Show unchecked items
        unchecked = [item for item in pd.items if not item.checked]
        if unchecked:
            lines.append(f"             Remaining ({len(unchecked)}):")
            for item in unchecked[:5]:
                text = item.text[:60] + "..." if len(item.text) > 60 else item.text
                lines.append(f"               - Line {item.line_number}: {text}")
            if len(unchecked) > 5:
                lines.append(f"               ... and {len(unchecked) - 5} more")
        lines.append("")

    return "\n".join(lines)


def scan_all_sejrlister() -> list:
    """Scan all active sejrlister."""
    reviews = []

    if not ACTIVE_DIR.exists():
        print(f"[FAIL] Active directory not found: {ACTIVE_DIR}")
        return reviews

    for d in sorted(ACTIVE_DIR.iterdir()):
        if not d.is_dir():
            continue
        sejr_file = d / "SEJR_LISTE.md"
        if sejr_file.exists():
            review = parse_sejr_liste(sejr_file)
            reviews.append(review)

    return reviews


def format_full_report(reviews: list) -> str:
    """Format complete 3-pass review report."""
    lines = []
    lines.append("=" * 70)
    lines.append("ADMIRAL 3-PASS REVIEW SYSTEM")
    lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Active Sejrlister: {len(reviews)}")
    lines.append("")

    # Summary table
    lines.append("-" * 70)
    lines.append(f"{'Sejrliste':<45} {'Progress':<12} {'Score':<10}")
    lines.append("-" * 70)
    for r in reviews:
        name = r.name[:44]
        pct = f"{r.overall_pct:.0f}%"
        score = f"{r.total_score}/30"
        archivable = " [READY]" if r.total_score >= 24 else ""
        lines.append(f"  {name:<43} {pct:<12} {score}{archivable}")
    lines.append("-" * 70)
    lines.append("")

    # Detailed per sejrliste
    for r in reviews:
        lines.append("=" * 50)
        lines.append(format_review(r))

    # Archive readiness
    ready = [r for r in reviews if r.total_score >= 24]
    not_ready = [r for r in reviews if r.total_score < 24]

    lines.append("=" * 70)
    lines.append("ARCHIVE READINESS")
    lines.append(f"  Ready (>= 24/30): {len(ready)}")
    for r in ready:
        lines.append(f"    [READY] {r.name} — {r.total_score}/30")
    lines.append(f"  Not ready (< 24/30): {len(not_ready)}")
    for r in not_ready:
        lines.append(f"    [PENDING] {r.name} — {r.total_score}/30")
    lines.append("")

    lines.append("-" * 70)
    lines.append(f"Generated by admiral_review_3pass.py")
    return "\n".join(lines)


def main():
    print("Admiral 3-Pass Review System starting...")
    print()

    reviews = scan_all_sejrlister()

    if not reviews:
        print("[FAIL] No sejrlister found in 10_ACTIVE/")
        sys.exit(1)

    text = format_full_report(reviews)
    print(text)

    # Save
    report_path = REPORT_DIR / "REVIEW_3PASS_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 3-Pass Review Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"```\n{text}\n```\n")

    # Also save JSON
    json_path = REPORT_DIR / "review_3pass.json"
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sejrlister": [
            {
                "name": r.name,
                "overall_pct": r.overall_pct,
                "total_score": r.total_score,
                "passes": [
                    {
                        "pass": p.pass_number,
                        "checked": p.checked,
                        "total": p.total,
                        "pct": p.pct,
                        "score": p.score,
                    }
                    for p in r.passes
                ]
            }
            for r in reviews
        ]
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nReport saved to: {report_path}")
    print(f"JSON saved to:   {json_path}")


if __name__ == "__main__":
    main()
