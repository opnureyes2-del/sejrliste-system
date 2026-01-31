#!/usr/bin/env python3
"""
Unified YAML Parser for Sejrliste System
=========================================

Uses PyYAML for safe, correct YAML handling.
Handles nested structures, lists, and all YAML features.

Usage:
    from app.utils import parse_yaml_simple, write_yaml_simple

    # Read
    data = parse_yaml_simple(Path("config.yaml"))

    # Write
    write_yaml_simple(Path("output.yaml"), {"key": "value"})

Migrated 2026-01-31: Flat line parser replaced with PyYAML.
"""

import yaml
from pathlib import Path
from typing import Any, Dict


def parse_yaml_simple(filepath: Path) -> Dict[str, Any]:
    """
    Parse YAML file using PyYAML (handles nested structures correctly).

    Args:
        filepath: Path to YAML file

    Returns:
        Dictionary of parsed content, or empty dict if file missing/invalid
    """
    if not filepath.exists():
        return {}

    try:
        content = filepath.read_text(encoding="utf-8")
        result = yaml.safe_load(content)
        return result if isinstance(result, dict) else {}
    except (yaml.YAMLError, UnicodeDecodeError):
        return {}


def write_yaml_simple(filepath: Path, data: Dict[str, Any], indent: int = 0) -> None:
    """
    Write YAML file using PyYAML (preserves nested structures).

    Args:
        filepath: Path to write YAML file
        data: Dictionary to write
        indent: Unused (kept for backward compatibility)
    """
    yaml_content = yaml.dump(
        data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=120
    )
    filepath.write_text(yaml_content, encoding="utf-8")


# ============================================================================
# TEST (when run directly)
# ============================================================================

if __name__ == "__main__":
    import tempfile

    print("Testing yaml_parser.py (PyYAML backend)...")

    # Test write and read
    test_data = {
        "name": "Test Project",
        "version": 1,
        "active": True,
        "score": 27.5,
        "status": None,
        "nested": {
            "key1": "value1",
            "key2": [1, 2, 3],
        },
    }

    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        test_path = Path(f.name)

    write_yaml_simple(test_path, test_data)
    print(f"Wrote: {test_path}")
    print(f"Content:\n{test_path.read_text()}")

    read_data = parse_yaml_simple(test_path)
    print(f"\nRead back: {read_data}")

    # Verify
    assert read_data["name"] == "Test Project", "name mismatch"
    assert read_data["version"] == 1, "version mismatch"
    assert read_data["active"] is True, "active mismatch"
    assert read_data["score"] == 27.5, "score mismatch"
    assert read_data["nested"]["key1"] == "value1", "nested mismatch"
    assert read_data["nested"]["key2"] == [1, 2, 3], "list mismatch"

    print("\n[OK] All tests passed!")

    # Cleanup
    test_path.unlink()
