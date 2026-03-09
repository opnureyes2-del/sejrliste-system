#!/usr/bin/env python3
"""Migrate old flat STATUS.yaml → new unified nested format.

Reads existing flat keys (pass_1_complete, pass_1_score, etc.)
and adds the new nested structure (pass_tracking, score_tracking, model_tracking).
Preserves ALL existing data — backwards compatible flat keys remain.
"""

import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone

SYSTEM_ROOT = Path(__file__).parent.parent
ARCHIVE = SYSTEM_ROOT / "90_ARCHIVE"
ACTIVE = SYSTEM_ROOT / "10_ACTIVE"


def migrate_status(status_path: Path) -> bool:
    """Migrate a single STATUS.yaml to unified format. Returns True if changed."""
    if not status_path.exists():
        return False

    data = yaml.safe_load(status_path.read_text()) or {}

    # Already migrated?
    if 'pass_tracking' in data and isinstance(data['pass_tracking'], dict):
        return False

    now_iso = datetime.now(timezone.utc).astimezone().isoformat()

    # Build nested structure from flat keys
    data['meta'] = {
        'sejr_name': data.get('sejr_name', status_path.parent.name),
        'folder': status_path.parent.name,
        'last_updated': data.get('last_verification', now_iso),
        'created': data.get('last_verification', now_iso),
    }

    data['pass_tracking'] = {
        'current_pass': data.get('current_pass', 1),
        'can_archive': data.get('can_archive', False),
        'status': data.get('status', 'unknown'),
        'completion_percentage': data.get('completion_percentage', 0),
        'final_verification_complete': data.get('final_verification_complete', False),
        'total_score': data.get('total_score', 0),
        'pass_1': {
            'complete': data.get('pass_1_complete', False),
            'score': data.get('pass_1_score', 0),
            'max_score': 10,
            'percentage': data.get('pass_1_pct', 0),
        },
        'pass_2': {
            'complete': data.get('pass_2_complete', False),
            'score': data.get('pass_2_score', 0),
            'max_score': 10,
            'percentage': data.get('pass_2_pct', 0),
        },
        'pass_3': {
            'complete': data.get('pass_3_complete', False),
            'score': data.get('pass_3_score', 0),
            'max_score': 10,
            'percentage': data.get('pass_3_pct', 0),
        },
    }

    data['score_tracking'] = {'totals': {'total_score': data.get('total_score', 0)}}
    data['model_tracking'] = {'models_used': [], 'sessions': []}

    # Write back
    header = f"# STATUS.yaml - Unified format (migrated {now_iso})\n\n"
    yaml_content = yaml.dump(data, default_flow_style=False, allow_unicode=True,
                             sort_keys=False, width=120)
    status_path.write_text(header + yaml_content, encoding="utf-8")
    return True


def main():
    migrated = 0
    skipped = 0
    errors = 0

    for folder in [ARCHIVE, ACTIVE]:
        if not folder.exists():
            continue
        for project_dir in sorted(folder.iterdir()):
            if not project_dir.is_dir() or project_dir.name.startswith('.'):
                continue
            status_path = project_dir / "STATUS.yaml"
            try:
                if migrate_status(status_path):
                    print(f"  [MIGRATED] {project_dir.name}")
                    migrated += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"  [ERROR] {project_dir.name}: {e}")
                errors += 1

    print(f"\nDone: {migrated} migrated, {skipped} skipped (already done), {errors} errors")


if __name__ == "__main__":
    main()
