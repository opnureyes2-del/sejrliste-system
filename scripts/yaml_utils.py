#!/usr/bin/env python3
"""
Shared YAML utilities for all Sejrliste scripts.

REPLACES: parse_yaml_simple/write_yaml_simple (buggy flat parser)
USES: PyYAML (properly installed in venv)

This module provides safe, correct YAML handling that preserves
nested structures, lists, and all YAML features.

Part of SEJR LISTE SYSTEM — DNA Layer 4 (SELF-IMPROVING)
"""

import yaml
from pathlib import Path
from datetime import datetime, timezone


def parse_yaml(filepath: Path) -> dict:
    """Parse YAML file using PyYAML (handles nested structures correctly).

    Args:
        filepath: Path to the YAML file

    Returns:
        dict: Parsed YAML content, or empty dict if file doesn't exist or is invalid
    """
    if not filepath.exists():
        return {}

    try:
        content = filepath.read_text(encoding="utf-8")
        result = yaml.safe_load(content)
        return result if isinstance(result, dict) else {}
    except (yaml.YAMLError, UnicodeDecodeError):
        return {}


def write_yaml(filepath: Path, data: dict, header: str = None):
    """Write YAML file using PyYAML (preserves nested structures).

    Args:
        filepath: Path to write to
        data: Dictionary to serialize
        header: Optional comment header (without # prefix)
    """
    lines = []
    if header:
        lines.append(f"# {header}")
    lines.append(f"# Last updated: {datetime.now(timezone.utc).astimezone().isoformat()}")
    lines.append("")

    yaml_content = yaml.dump(
        data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=120
    )

    filepath.write_text(
        "\n".join(lines) + yaml_content,
        encoding="utf-8"
    )


# Backwards-compatible aliases
parse_yaml_simple = parse_yaml
write_yaml_simple = write_yaml
