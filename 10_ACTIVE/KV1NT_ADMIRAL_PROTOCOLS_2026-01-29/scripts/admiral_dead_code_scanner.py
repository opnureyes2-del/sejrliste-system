#!/usr/bin/env python3
"""
Admiral Dead Code Scanner
=========================
Scans project directories for dead code:
- Unused imports in Python files
- Functions/classes never called
- Files never imported/referenced
- Stale data (old configs, orphan scripts)

Asks the 4 obligatory questions (Rule -39):
1. What was the vision?
2. What worked?
3. What went wrong?
4. How do we do it right?

Output: Classified report with categories.
"""

import os
import sys
import ast
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict

# --- Configuration ---
SCAN_DIRS = [
    Path.home() / "Desktop" / "sejrliste systemet",
    Path.home() / "Desktop" / "MIN ADMIRAL",
]
REPORT_DIR = Path(__file__).parent.parent
EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".mypy_cache"}
EXCLUDE_FILES = {"__init__.py"}


@dataclass
class DeadCodeItem:
    category: str       # unused_import, unused_function, orphan_file, stale_data
    file_path: str
    name: str
    line_number: int = 0
    details: str = ""
    severity: str = "LOW"  # LOW, MEDIUM, HIGH


@dataclass
class ScanResult:
    timestamp: str = ""
    total_files_scanned: int = 0
    total_python_files: int = 0
    total_md_files: int = 0
    total_sh_files: int = 0
    items: list = field(default_factory=list)
    categories: dict = field(default_factory=lambda: defaultdict(list))


def find_unused_imports(filepath: Path) -> list:
    """Find imports that are never used in the file."""
    items = []
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(filepath))
    except (SyntaxError, ValueError):
        return items

    # Collect all imports
    imports = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                imports[name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                name = alias.asname or alias.name
                imports[name] = node.lineno

    # Check which imports are used
    # Simple approach: check if the name appears in the source text
    # outside of import statements
    import_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_lines.add(node.lineno)

    lines = source.split("\n")
    for name, lineno in imports.items():
        # Check if name appears anywhere else in the file
        used = False
        for i, line in enumerate(lines, 1):
            if i == lineno:
                continue  # Skip the import line itself
            if i in import_lines:
                continue  # Skip other import lines
            if re.search(r'\b' + re.escape(name) + r'\b', line):
                used = True
                break

        if not used:
            items.append(DeadCodeItem(
                category="unused_import",
                file_path=str(filepath),
                name=name,
                line_number=lineno,
                details=f"Import '{name}' appears to be unused",
                severity="LOW"
            ))

    return items


def find_unused_functions(filepath: Path) -> list:
    """Find functions defined but never called in the same file."""
    items = []
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(filepath))
    except (SyntaxError, ValueError):
        return items

    # Collect all function definitions (excluding __dunder__ methods)
    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            if name.startswith("__") and name.endswith("__"):
                continue  # Skip dunder methods
            if name.startswith("_"):
                continue  # Skip private methods (convention)
            functions[name] = node.lineno

    # Check if functions are called anywhere in the source
    for name, lineno in functions.items():
        # Look for function calls: name(
        call_pattern = re.compile(r'\b' + re.escape(name) + r'\s*\(')
        lines = source.split("\n")
        called = False
        for i, line in enumerate(lines, 1):
            if i == lineno:
                continue  # Skip definition line
            if call_pattern.search(line):
                called = True
                break

        # Also check if it's used as a callback: name without ()
        if not called:
            ref_pattern = re.compile(r'\b' + re.escape(name) + r'\b')
            for i, line in enumerate(lines, 1):
                if i == lineno:
                    continue
                if "def " + name in line:
                    continue
                if ref_pattern.search(line):
                    called = True
                    break

        if not called:
            items.append(DeadCodeItem(
                category="unused_function",
                file_path=str(filepath),
                name=name,
                line_number=lineno,
                details=f"Function '{name}' defined but never called in this file",
                severity="MEDIUM"
            ))

    return items


def find_orphan_files(scan_dir: Path) -> list:
    """Find files that are never referenced by other files."""
    items = []
    all_files = set()
    all_references = set()

    # Collect all files
    for f in scan_dir.rglob("*"):
        if f.is_file() and not any(ex in f.parts for ex in EXCLUDE_DIRS):
            all_files.add(f)

    # Collect all references (imports, includes, links)
    for f in all_files:
        if f.suffix not in (".py", ".md", ".sh", ".yaml", ".yml", ".json"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        # Look for file references
        for other in all_files:
            if other == f:
                continue
            # Check if filename or relative path is mentioned
            if other.name in content:
                all_references.add(other)
            # Check for path references
            try:
                rel = other.relative_to(scan_dir)
                if str(rel) in content:
                    all_references.add(other)
            except ValueError:
                pass

    # Files never referenced (only .py and .sh — .md is documentation)
    for f in all_files:
        if f.suffix in (".py", ".sh") and f not in all_references:
            if f.name in EXCLUDE_FILES:
                continue
            items.append(DeadCodeItem(
                category="orphan_file",
                file_path=str(f),
                name=f.name,
                details=f"File '{f.name}' is never referenced by other files in {scan_dir.name}",
                severity="MEDIUM"
            ))

    return items


def find_stale_configs(scan_dir: Path) -> list:
    """Find config files that reference non-existent paths or services."""
    items = []
    service_patterns = [
        r"systemctl\s+\w+\s+([\w\-]+\.service)",
        r"ExecStart\s*=\s*(.+)",
        r"Restart\s*=\s*(.+)",
    ]

    for f in scan_dir.rglob("*.md"):
        if any(ex in f.parts for ex in EXCLUDE_DIRS):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        # Check for references to paths that don't exist
        path_pattern = re.compile(r'(/home/rasmus/[^\s\)\]"\'`]+)')
        for match in path_pattern.finditer(content):
            ref_path = match.group(1).rstrip(".,;:")
            if not os.path.exists(ref_path) and not ref_path.endswith("*"):
                items.append(DeadCodeItem(
                    category="stale_reference",
                    file_path=str(f),
                    name=ref_path,
                    line_number=content[:match.start()].count("\n") + 1,
                    details=f"References non-existent path: {ref_path}",
                    severity="LOW"
                ))

    return items


def scan_directory(scan_dir: Path) -> ScanResult:
    """Scan a directory for dead code."""
    result = ScanResult(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if not scan_dir.exists():
        return result

    # Count files
    for f in scan_dir.rglob("*"):
        if f.is_file() and not any(ex in f.parts for ex in EXCLUDE_DIRS):
            result.total_files_scanned += 1
            if f.suffix == ".py":
                result.total_python_files += 1
            elif f.suffix == ".md":
                result.total_md_files += 1
            elif f.suffix == ".sh":
                result.total_sh_files += 1

    # Scan Python files for unused imports and functions
    for f in scan_dir.rglob("*.py"):
        if any(ex in f.parts for ex in EXCLUDE_DIRS):
            continue
        result.items.extend(find_unused_imports(f))
        result.items.extend(find_unused_functions(f))

    # Scan for orphan files
    result.items.extend(find_orphan_files(scan_dir))

    # Scan for stale references
    result.items.extend(find_stale_configs(scan_dir))

    # Categorize
    for item in result.items:
        result.categories[item.category].append(item)

    return result


def format_report(results: dict) -> str:
    """Format scan results as readable report."""
    lines = []
    lines.append("=" * 70)
    lines.append("ADMIRAL DEAD CODE SCANNER")
    lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")

    total_items = 0
    for dir_name, result in results.items():
        lines.append(f"--- {dir_name} ---")
        lines.append(f"  Files scanned: {result.total_files_scanned}")
        lines.append(f"  Python: {result.total_python_files} | Markdown: {result.total_md_files} | Shell: {result.total_sh_files}")
        lines.append(f"  Issues found: {len(result.items)}")
        lines.append("")

        if not result.items:
            lines.append("  [OK] No dead code detected")
            lines.append("")
            continue

        for category, items in sorted(result.categories.items()):
            lines.append(f"  [{category.upper()}] ({len(items)} items)")
            for item in items[:10]:  # Limit to 10 per category
                loc = f":{item.line_number}" if item.line_number else ""
                sev = f"[{item.severity}]"
                lines.append(f"    {sev} {item.name}")
                lines.append(f"         File: {item.file_path}{loc}")
                lines.append(f"         {item.details}")
            if len(items) > 10:
                lines.append(f"    ... and {len(items) - 10} more")
            lines.append("")
            total_items += len(items)

    lines.append("-" * 70)
    lines.append(f"TOTAL ISSUES: {total_items}")
    lines.append("")
    lines.append("OBLIGATORY QUESTIONS (Rule -39):")
    lines.append("  1. What was the vision for each dead item?")
    lines.append("  2. What worked before it became dead?")
    lines.append("  3. What went wrong (why abandoned)?")
    lines.append("  4. How do we do it right (revive or archive)?")
    lines.append("")
    lines.append("ACTION: Review each item. Revive or archive. Never delete blindly.")
    lines.append("-" * 70)
    lines.append(f"Generated by admiral_dead_code_scanner.py")
    return "\n".join(lines)


def main():
    print("Admiral Dead Code Scanner starting...")
    print(f"Scanning {len(SCAN_DIRS)} directories...")
    print()

    results = {}
    for scan_dir in SCAN_DIRS:
        if scan_dir.exists():
            print(f"  Scanning: {scan_dir.name}...")
            results[scan_dir.name] = scan_directory(scan_dir)

    text = format_report(results)
    print(text)

    # Save report
    report_path = REPORT_DIR / "DEAD_CODE_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Dead Code Scanner Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"```\n{text}\n```\n")

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
