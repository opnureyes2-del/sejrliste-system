#!/usr/bin/env python3
"""
Shared timestamp utility for SEJR LISTE SYSTEM.
ALL scripts MUST use these functions for timestamps.

REGEL: datetime.now().isoformat() er FORBUDT.
BRUG: get_timestamp() eller get_date() i stedet.

PERMANENT FIX: 2026-01-29 — Alle timestamps inkluderer timezone (+01:00).
"""

from datetime import datetime, timezone


def get_timestamp() -> str:
    """Get ISO 8601 timestamp WITH timezone.

    Returns: "2026-01-29T23:29:24.133919+01:00"

    ALDRIG brug datetime.now().isoformat() direkte!
    """
    return datetime.now(timezone.utc).astimezone().isoformat()


def get_date() -> str:
    """Get date string YYYY-MM-DD.

    Returns: "2026-01-29"
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_datetime_display() -> str:
    """Get human-readable datetime for display.

    Returns: "2026-01-29 23:29"
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_time_display() -> str:
    """Get time-only string for display.

    Returns: "23:29:24"
    """
    return datetime.now().strftime("%H:%M:%S")
