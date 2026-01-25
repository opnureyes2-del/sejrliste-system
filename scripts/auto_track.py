#!/usr/bin/env python3
"""
Auto-track state and update _CURRENT/
Part of SEJR LISTE SYSTEM - DNA Layer 2 (SELF-DOCUMENTING)

INGEN EXTERNAL DEPENDENCIES - Kun Python standard library
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ============================================================================
# SIMPLE YAML PARSING (No PyYAML dependency)
# ============================================================================

def parse_yaml_simple(filepath: Path) -> dict:
    """Parse simple YAML without PyYAML."""
    if not filepath.exists():
        return {}

    result = {}
    try:
        content = filepath.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if ":" in line and not line.strip().startswith("#"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().strip('"').strip("'")
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    elif value.replace(".", "").isdigit():
                        value = float(value) if "." in value else int(value)
                    result[key] = value
    except:
        pass
    return result

def scan_active_sejr(system_path: Path):
    """Scan all active sejr lister and collect current state"""
    active_dir = system_path / "10_ACTIVE"

    if not active_dir.exists():
        return []

    sejr_data = []
    for sejr_folder in active_dir.iterdir():
        if not sejr_folder.is_dir():
            continue

        # Read STATUS.yaml
        status_file = sejr_folder / "STATUS.yaml"
        if status_file.exists():
            status = parse_yaml_simple(status_file)
        else:
            status = {'status': 'unknown'}

        # Read AUTO_LOG.jsonl to get latest actions
        log_file = sejr_folder / "AUTO_LOG.jsonl"
        latest_action = None
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    latest_action = json.loads(lines[-1])

        sejr_data.append({
            'name': sejr_folder.name,
            'path': sejr_folder,
            'status': status.get('status', 'unknown'),
            'completion': status.get('completion_percentage', 0),
            'latest_action': latest_action
        })

    return sejr_data

def update_state_md(system_path: Path, sejr_data: list):
    """Update _CURRENT/STATE.md with current state"""
    state_file = system_path / "_CURRENT" / "STATE.md"

    # Determine what we're working on
    in_progress = [s for s in sejr_data if s['status'] == 'in_progress']
    nearly_complete = [s for s in sejr_data if s['status'] == 'nearly_complete']

    if in_progress:
        current_work = in_progress[0]['name']
        next_step = "Continue with current sejr"
    elif nearly_complete:
        current_work = nearly_complete[0]['name']
        next_step = "Complete final verifications"
    elif sejr_data:
        current_work = sejr_data[0]['name']
        next_step = "Start or continue sejr"
    else:
        current_work = "No active sejr"
        next_step = "Generate new sejr liste"

    # Generate STATE.md content
    content = f"""# CURRENT STATE - Hvor Er Vi NU?

**Opdateret:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## LIGE NU (Dette Øjeblik)

**Arbejder på:** {current_work}
**Næste skridt:** {next_step}
**Blokkeret af:** INTET - Check verify status for details

---

## ACTIVE SEJR LISTER ({len(sejr_data)})

"""

    for sejr in sejr_data:
        status_emoji = {
            'completed': '✅',
            'nearly_complete': '⚡',
            'in_progress': '🔵',
            'early_stage': '🟡',
            'unknown': '❓'
        }.get(sejr['status'], '❓')

        content += f"""### {status_emoji} {sejr['name']}
**Status:** {sejr['status']}
**Progress:** {sejr['completion']:.0f}%
**Path:** `{sejr['path']}`

"""

    if not sejr_data:
        content += """*Ingen aktive sejr lister*

**Start ny sejr:**
```bash
python scripts/generate_sejr.py --name "Your Project Name"
```

"""

    content += """---

## QUICK RESUME (3 Linjer)

"""

    if sejr_data:
        total_completion = sum(s['completion'] for s in sejr_data) / len(sejr_data)
        content += f"""{len(sejr_data)} aktive sejr liste(r) med gennemsnitlig {total_completion:.0f}% completion.
Kan fortsætte ved at: Åbn SEJR_LISTE.md i aktivt sejr → Udfyld phases →
Run auto_verify.py → Archive når 100% complete.
"""
    else:
        content += """Sejr Liste System operationelt og klar til brug.
Start med: python scripts/generate_sejr.py --name "Project Name"
Derefter: Arbejd gennem SEJR_LISTE.md phases → Verify → Archive.
"""

    content += """
---

**Auto-opdateret af:** scripts/auto_track.py
**Frekvens:** On-demand or via cron
**Formål:** DNA Layer 2 (SELF-DOCUMENTING)
"""

    with open(state_file, 'w') as f:
        f.write(content)

    print(f"✅ Updated: {state_file}")

def update_delta_md(system_path: Path):
    """Append changes to _CURRENT/DELTA.md"""
    delta_file = system_path / "_CURRENT" / "DELTA.md"

    # Read existing deltas
    if delta_file.exists():
        with open(delta_file, 'r') as f:
            existing = f.read()
    else:
        existing = "# DELTA - Hvad Er NYT?\n\n"

    # Check if we need to add a delta (only if there are recent changes)
    # For now, just confirm the file exists
    if not delta_file.exists():
        with open(delta_file, 'w') as f:
            f.write(existing)
        print(f"✅ Created: {delta_file}")

def rebuild_state(system_path: Path):
    """Rebuild STATE.md from scratch by scanning all sejr"""
    print("🔄 Rebuilding STATE.md from active sejr lister...\n")

    sejr_data = scan_active_sejr(system_path)
    update_state_md(system_path, sejr_data)
    update_delta_md(system_path)

    print(f"\n✅ State rebuilt - found {len(sejr_data)} active sejr")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto-track sejr liste state")
    parser.add_argument("--rebuild-state", action="store_true",
                       help="Rebuild STATE.md from scratch")
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent

    if args.rebuild_state:
        rebuild_state(system_path)
    else:
        # Default: update state
        sejr_data = scan_active_sejr(system_path)
        update_state_md(system_path, sejr_data)
        print("✅ State tracking updated")
