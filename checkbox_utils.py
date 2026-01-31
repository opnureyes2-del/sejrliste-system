#!/usr/bin/env python3
"""
CHECKBOX UTILITIES — Delt modul for checkbox-tælling
=====================================================

WHAT: Centraliseret count_checkboxes() funktion
WHY:  Var duplikeret i 6 filer — ét sted = ingen drift, ingen fejl
WHO:  Importeret af web_app, masterpiece, auto_verify, pages/
HOW:  from checkbox_utils import count_checkboxes

Version: 3.0.0
"""
import re


def count_checkboxes(content: str) -> tuple:
    """Count checked and total checkboxes in markdown content.

    Args:
        content: Markdown text containing checkboxes like - [x] and - [ ]

    Returns:
        Tuple of (checked_count, total_count)
    """
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked
