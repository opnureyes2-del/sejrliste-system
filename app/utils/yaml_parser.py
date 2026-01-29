#!/usr/bin/env python3
"""
Unified YAML Parser for Sejrliste System
=========================================

INGEN EXTERNAL DEPENDENCIES - Kun Python standard library.

This module provides simple YAML parsing without PyYAML dependency.
Used across all scripts for consistent YAML handling.

Usage:
    from app.utils import parse_yaml_simple, write_yaml_simple

    # Read
    data = parse_yaml_simple(Path("config.yaml"))

    # Write
    write_yaml_simple(Path("output.yaml"), {"key": "value"})
"""

from pathlib import Path
from typing import Any, Dict, Union


def parse_yaml_simple(filepath: Path) -> Dict[str, Any]:
    """
    Parse simple YAML file without PyYAML dependency.

    Supports:
    - String values (with or without quotes)
    - Boolean values (true/false)
    - Integer and float values
    - Comments (lines starting with #)

    Does NOT support:
    - Nested structures (only top-level keys)
    - Lists
    - Multi-line strings

    Args:
        filepath: Path to YAML file

    Returns:
        Dictionary of parsed key-value pairs

    Example:
        >>> data = parse_yaml_simple(Path("config.yaml"))
        >>> print(data.get("name", "unknown"))
    """
    if not filepath.exists():
        return {}

    result = {}
    try:
        content = filepath.read_text(encoding="utf-8")
        for line in content.split("\n"):
            # Skip empty lines and comments
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()

                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]

                    # Convert types
                    result[key] = _convert_value(value)
    except Exception:
        pass  # Return empty dict on any error

    return result


def _convert_value(value: str) -> Union[str, int, float, bool, None]:
    """Convert string value to appropriate Python type."""
    # Handle empty values
    if not value or value.lower() in ('null', 'none', '~'):
        return None

    # Handle booleans
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    # Handle numbers
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    return value


def write_yaml_simple(filepath: Path, data: Dict[str, Any], indent: int = 0) -> None:
    """
    Write simple YAML file without PyYAML dependency.

    Supports:
    - Nested dictionaries
    - Lists of primitives or dicts
    - All primitive types (str, int, float, bool, None)

    Args:
        filepath: Path to write YAML file
        data: Dictionary to write
        indent: Base indentation level (internal use)

    Example:
        >>> write_yaml_simple(Path("output.yaml"), {"name": "test", "active": True})
    """
    def _to_yaml_lines(obj: Any, level: int = 0) -> list:
        lines = []
        prefix = "  " * level

        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, dict):
                    lines.append(f"{prefix}{key}:")
                    lines.extend(_to_yaml_lines(value, level + 1))
                elif isinstance(value, list):
                    lines.append(f"{prefix}{key}:")
                    for item in value:
                        if isinstance(item, dict):
                            lines.append(f"{prefix}  -")
                            for k, v in item.items():
                                v_str = _value_to_yaml(v)
                                lines.append(f"{prefix}    {k}: {v_str}")
                        else:
                            lines.append(f"{prefix}  - {_value_to_yaml(item)}")
                else:
                    lines.append(f"{prefix}{key}: {_value_to_yaml(value)}")
        return lines

    yaml_lines = _to_yaml_lines(data, indent)
    filepath.write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")


def _value_to_yaml(value: Any) -> str:
    """Convert Python value to YAML string representation."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        # Quote strings that might be confused with other types
        if value.lower() in ('true', 'false', 'null', 'none', '~'):
            return f'"{value}"'
        # Quote strings with special characters
        if ':' in value or '#' in value or '\n' in value:
            return f'"{value}"'
        return value
    return str(value)


# ============================================================================
# TEST (when run directly)
# ============================================================================

if __name__ == "__main__":
    import tempfile

    print("Testing yaml_parser.py...")

    # Test write and read
    test_data = {
        "name": "Test Project",
        "version": 1,
        "active": True,
        "score": 27.5,
        "status": None,
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

    print("\n[OK] All tests passed!")

    # Cleanup
    test_path.unlink()
