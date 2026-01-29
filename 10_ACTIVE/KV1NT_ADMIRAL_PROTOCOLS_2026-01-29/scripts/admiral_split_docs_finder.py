#!/usr/bin/env python3
"""
Admiral Split Docs Finder
==========================
Finds fragmented documentation across the system.
Detects:
- Same topic documented in multiple places
- Broken cross-references between docs
- Orphan documentation (no links to/from)
- Duplicate content across files

Output: Reunification plan mapping fragments to canonical locations.
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict

# --- Configuration ---
SCAN_DIRS = [
    Path.home() / "Desktop" / "MIN ADMIRAL",
    Path.home() / ".claude" / ".context" / "core",
    Path.home() / "Desktop" / "sejrliste systemet",
    Path.home() / "Desktop" / "MASTER FOLDERS(INTRO)",
]
REPORT_DIR = Path(__file__).parent.parent
EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "archives", "90_ARCHIVE"}


@dataclass
class DocFragment:
    file_path: str
    topic: str
    heading: str
    line_number: int
    content_hash: str  # Simple hash for duplicate detection
    word_count: int


@dataclass
class BrokenRef:
    source_file: str
    source_line: int
    target: str
    ref_type: str  # file_link, path_reference, section_link


@dataclass
class DuplicateTopic:
    topic: str
    locations: list  # List of (file_path, heading, line_number)
    recommendation: str


def extract_headings(filepath: Path) -> list:
    """Extract all markdown headings from a file."""
    headings = []
    try:
        lines = filepath.read_text(encoding="utf-8", errors="replace").split("\n")
    except Exception:
        return headings

    for i, line in enumerate(lines, 1):
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            # Simple content hash: next 5 non-empty lines
            content_lines = []
            for j in range(i, min(i + 6, len(lines))):
                if lines[j - 1].strip():
                    content_lines.append(lines[j - 1].strip().lower())
            content_hash = hash(tuple(content_lines))

            word_count = 0
            for j in range(i, len(lines)):
                next_line = lines[j - 1] if j > 0 else ""
                if j > i and re.match(r'^#{1,6}\s+', next_line):
                    break
                word_count += len(next_line.split())

            headings.append(DocFragment(
                file_path=str(filepath),
                topic=title.lower().strip("*_#"),
                heading=title,
                line_number=i,
                content_hash=str(content_hash),
                word_count=word_count,
            ))

    return headings


def find_broken_references(filepath: Path, all_files: set) -> list:
    """Find broken file references in a markdown file."""
    broken = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception:
        return broken

    all_filenames = {f.name for f in all_files}

    for i, line in enumerate(lines, 1):
        # Markdown links: [text](path)
        for match in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', line):
            target = match.group(2)
            if target.startswith("http") or target.startswith("#"):
                continue
            # Check if file exists
            target_path = (filepath.parent / target).resolve()
            if not target_path.exists():
                # Also check if just filename exists somewhere
                target_name = Path(target).name
                if target_name not in all_filenames:
                    broken.append(BrokenRef(
                        source_file=str(filepath),
                        source_line=i,
                        target=target,
                        ref_type="file_link"
                    ))

        # Path references: /home/rasmus/...
        for match in re.finditer(r'(/home/rasmus/[^\s\)\]"\'`]+)', line):
            ref_path = match.group(1).rstrip(".,;:")
            if not os.path.exists(ref_path) and not ref_path.endswith("*"):
                broken.append(BrokenRef(
                    source_file=str(filepath),
                    source_line=i,
                    target=ref_path,
                    ref_type="path_reference"
                ))

    return broken


def find_duplicate_topics(all_headings: list) -> list:
    """Find topics documented in multiple places."""
    topic_map = defaultdict(list)
    duplicates = []

    # Normalize topics
    for h in all_headings:
        # Clean topic for comparison
        clean = re.sub(r'[^a-z0-9\s]', '', h.topic)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if len(clean) > 5:  # Skip very short headings
            topic_map[clean].append(h)

    for topic, fragments in topic_map.items():
        if len(fragments) > 1:
            # Check if they're actually duplicates (similar content)
            unique_hashes = set(f.content_hash for f in fragments)
            if len(unique_hashes) < len(fragments):
                # Some have same content — real duplicates
                locations = [(f.file_path, f.heading, f.line_number) for f in fragments]
                # Find the largest version
                largest = max(fragments, key=lambda f: f.word_count)
                duplicates.append(DuplicateTopic(
                    topic=topic,
                    locations=locations,
                    recommendation=f"Canonical: {Path(largest.file_path).name}:{largest.line_number} ({largest.word_count} words)"
                ))

    return duplicates


def find_orphan_docs(all_files: set, all_references: set) -> list:
    """Find documentation files never referenced by other docs."""
    orphans = []
    for f in all_files:
        if f.suffix != ".md":
            continue
        if f not in all_references:
            # Check if it's a root/index file (those are OK to be unreferenced)
            if f.name.lower() in ("readme.md", "index.md", "claude.md", "status.yaml"):
                continue
            orphans.append(str(f))
    return orphans


def scan_all() -> dict:
    """Scan all directories and collect results."""
    all_files = set()
    all_headings = []
    all_broken_refs = []
    all_referenced_files = set()

    # Collect all files
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for f in scan_dir.rglob("*"):
            if f.is_file() and not any(ex in f.parts for ex in EXCLUDE_DIRS):
                all_files.add(f)

    # Extract headings and find broken references
    md_files = [f for f in all_files if f.suffix == ".md"]
    for f in md_files:
        all_headings.extend(extract_headings(f))
        all_broken_refs.extend(find_broken_references(f, all_files))

        # Track which files are referenced
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            for other in all_files:
                if other != f and other.name in content:
                    all_referenced_files.add(other)
        except Exception:
            pass

    # Find duplicates and orphans
    duplicates = find_duplicate_topics(all_headings)
    orphans = find_orphan_docs(all_files, all_referenced_files)

    return {
        "total_files": len(all_files),
        "total_md": len(md_files),
        "total_headings": len(all_headings),
        "broken_refs": all_broken_refs,
        "duplicates": duplicates,
        "orphans": orphans,
    }


def format_report(data: dict) -> str:
    """Format scan results as report."""
    lines = []
    lines.append("=" * 70)
    lines.append("ADMIRAL SPLIT DOCS FINDER")
    lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Files scanned: {data['total_files']}")
    lines.append(f"Markdown files: {data['total_md']}")
    lines.append(f"Headings found: {data['total_headings']}")
    lines.append("")

    # Broken references
    lines.append(f"--- BROKEN REFERENCES ({len(data['broken_refs'])}) ---")
    if not data["broken_refs"]:
        lines.append("  [OK] No broken references found")
    else:
        for ref in data["broken_refs"][:20]:
            lines.append(f"  [BROKEN] {Path(ref.source_file).name}:{ref.source_line}")
            lines.append(f"           -> {ref.target} ({ref.ref_type})")
        if len(data["broken_refs"]) > 20:
            lines.append(f"  ... and {len(data['broken_refs']) - 20} more")
    lines.append("")

    # Duplicate topics
    lines.append(f"--- DUPLICATE TOPICS ({len(data['duplicates'])}) ---")
    if not data["duplicates"]:
        lines.append("  [OK] No duplicate topics found")
    else:
        for dup in data["duplicates"][:10]:
            lines.append(f"  [DUP] \"{dup.topic}\" found in {len(dup.locations)} places:")
            for path, heading, lineno in dup.locations:
                lines.append(f"         - {Path(path).name}:{lineno} \"{heading}\"")
            lines.append(f"         Recommendation: {dup.recommendation}")
        if len(data["duplicates"]) > 10:
            lines.append(f"  ... and {len(data['duplicates']) - 10} more")
    lines.append("")

    # Orphan docs
    lines.append(f"--- ORPHAN DOCUMENTATION ({len(data['orphans'])}) ---")
    if not data["orphans"]:
        lines.append("  [OK] No orphan documentation found")
    else:
        for orphan in data["orphans"][:15]:
            lines.append(f"  [ORPHAN] {Path(orphan).name}")
            lines.append(f"           {orphan}")
        if len(data["orphans"]) > 15:
            lines.append(f"  ... and {len(data['orphans']) - 15} more")
    lines.append("")

    # Reunification plan
    lines.append("--- REUNIFICATION PLAN ---")
    lines.append("  1. Fix broken references (update paths or remove dead links)")
    lines.append("  2. Merge duplicate topics (keep canonical, redirect others)")
    lines.append("  3. Connect orphan docs (add to index or archive)")
    lines.append("")
    lines.append("-" * 70)
    lines.append(f"Generated by admiral_split_docs_finder.py")
    return "\n".join(lines)


def main():
    print("Admiral Split Docs Finder starting...")
    print(f"Scanning {len(SCAN_DIRS)} directories...")
    print()

    data = scan_all()
    text = format_report(data)
    print(text)

    # Save
    report_path = REPORT_DIR / "SPLIT_DOCS_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Split Documentation Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"```\n{text}\n```\n")

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
