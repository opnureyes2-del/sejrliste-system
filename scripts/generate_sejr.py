#!/usr/bin/env python3
"""
Generate new SEJR liste - STRØMLINET VERSION
Part of SEJR LISTE SYSTEM - DNA Layer 7 (SELF-OPTIMIZING)

SINGLE SOURCE OF TRUTH - Opretter KUN 4 filer:
- SEJR_LISTE.md (hovedopgave)
- CLAUDE.md (fokus lock - genereret)
- STATUS.yaml (UNIFIED: pass + score + model tracking)
- AUTO_LOG.jsonl (MASTER: alt logging)

INGEN REDUNDANS - Alt data eksisterer kun ét sted.
"""

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


def get_timestamp():
    """Get ISO 8601 timestamp with timezone."""
    return datetime.now(timezone.utc).astimezone().isoformat()


def generate_session_id():
    """Generate unique session ID."""
    return f"sess_{uuid.uuid4().hex[:12]}"


def generate_claude_md(sejr_path: Path, name: str):
    """Generate CLAUDE.md focus lock file."""
    template_path = sejr_path.parent.parent / "00_TEMPLATES" / "CLAUDE.md"

    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
    else:
        content = """# CLAUDE FOKUS LOCK

**Sejr:** {SEJR_NAVN}
**Current Pass:** 1/3
**Status:** Pass 1 - Planlægning

## DIN OPGAVE
Læs SEJR_LISTE.md og start med PHASE 0: Research
"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    replacements = {
        "{SEJR_NAVN}": name,
        "{CURRENT_PASS}": "1",
        "{STATUS}": "Pass 1 - Planlægning",
        "{BLOCKER}": "Færdiggør Pass 1",
        "{NEXT_ACTION}": "Læs SEJR_LISTE.md og afkryds første checkbox",
        "{PASS_1_STATUS}": "🔵 In Progress",
        "{PASS_1_SCORE}": "0",
        "{PASS_2_STATUS}": "⏳ Pending",
        "{PASS_2_SCORE}": "0",
        "{PASS_3_STATUS}": "⏳ Pending",
        "{PASS_3_SCORE}": "0",
        "{TOTAL_SCORE}": "0",
        "{TIMESTAMP}": timestamp,
    }

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    claude_file = sejr_path / "CLAUDE.md"
    claude_file.write_text(content, encoding="utf-8")
    return claude_file


def generate_sejr(name: str, system_path: Path):
    """Generate new sejr with ONLY 4 files (Single Source of Truth)."""

    # Create folder
    date = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{name.replace(' ', '_').upper()}_{date}"
    sejr_path = system_path / "10_ACTIVE" / folder_name
    sejr_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {sejr_path}")

    # Generate IDs
    session_id = generate_session_id()
    timestamp = get_timestamp()

    # ═══════════════════════════════════════════════════════════
    # FILE 1: SEJR_LISTE.md (hovedopgave)
    # ═══════════════════════════════════════════════════════════

    template_path = system_path / "00_TEMPLATES" / "SEJR_TEMPLATE.md"
    sejr_file = sejr_path / "SEJR_LISTE.md"

    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
        content = content.replace("{OPGAVE_NAVN}", name)
        content = content.replace("{DATO}", datetime.now().strftime("%Y-%m-%d %H:%M"))
        content = content.replace("{OWNER}", "Kv1nt + Rasmus")
        sejr_file.write_text(content, encoding="utf-8")
        print(f"✅ File 1/4: {sejr_file.name}")
    else:
        print(f"❌ Template not found: {template_path}")
        return False

    # ═══════════════════════════════════════════════════════════
    # FILE 2: CLAUDE.md (fokus lock - genereret)
    # ═══════════════════════════════════════════════════════════

    claude_file = generate_claude_md(sejr_path, name)
    print(f"✅ File 2/4: {claude_file.name}")

    # ═══════════════════════════════════════════════════════════
    # FILE 3: STATUS.yaml (UNIFIED - erstatter 3 filer)
    # ═══════════════════════════════════════════════════════════

    status_file = sejr_path / "STATUS.yaml"
    status_content = f"""# STATUS.yaml - UNIFIED STATUS (Single Source of Truth)
# Alt status data i ÉN fil - ingen redundans
# Sejr: {name}

# ═══════════════════════════════════════════════════════════
# META
# ═══════════════════════════════════════════════════════════

meta:
  sejr_name: "{name}"
  folder: "{folder_name}"
  created: "{timestamp}"
  created_by: "generate_sejr.py"
  session_id: "{session_id}"
  last_updated: "{timestamp}"

# ═══════════════════════════════════════════════════════════
# 3-PASS TRACKING
# ═══════════════════════════════════════════════════════════

pass_tracking:
  current_pass: 1
  can_archive: false
  archive_blocker: "Pass 1 ikke færdig"

  pass_1:
    name: "Planlægning"
    status: "in_progress"
    complete: false
    score: 0
    checkboxes_done: 0
    checkboxes_total: 0
    percentage: 0
    review_done: false

  pass_2:
    name: "Eksekvering"
    status: "pending"
    complete: false
    score: 0
    checkboxes_done: 0
    checkboxes_total: 0
    percentage: 0
    review_done: false

  pass_3:
    name: "7-DNA Review"
    status: "pending"
    complete: false
    score: 0
    checkboxes_done: 0
    checkboxes_total: 0
    percentage: 0
    final_verification: false

  totals:
    score: 0
    required_score: 24
    tests_passed: 0
    tests_required: 5

# ═══════════════════════════════════════════════════════════
# SCORE TRACKING
# ═══════════════════════════════════════════════════════════

score_tracking:
  positive:
    checkbox_done: 0
    pass_complete: 0
    verified_working: 0
    test_passed: 0
    admiral_moment: 0
    sejr_archived: 0

  negative:
    token_waste: 0
    memory_loss: 0
    lie_detected: 0
    rule_break: 0
    focus_lost: 0

  totals:
    positive_points: 0
    negative_points: 0
    total_score: 0
    rank: "KADET"

# ═══════════════════════════════════════════════════════════
# MODEL TRACKING
# ═══════════════════════════════════════════════════════════

model_tracking:
  current_model: null
  models_used: []
  human_activity:
    sessions: 0
    approvals: 0
    corrections: 0
  sessions:
    - id: "{session_id}"
      started: "{timestamp}"
      actor: "generate_sejr.py"
      action: "SEJR_CREATED"

# ═══════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════

statistics:
  total_sessions: 1
  total_actions: 1
  total_time_minutes: 0
  unique_models: 0
"""
    status_file.write_text(status_content, encoding="utf-8")
    print(f"✅ File 3/4: {status_file.name}")

    # ═══════════════════════════════════════════════════════════
    # FILE 4: AUTO_LOG.jsonl (MASTER - alt logging)
    # ═══════════════════════════════════════════════════════════

    log_file = sejr_path / "AUTO_LOG.jsonl"
    log_entry = {
        "timestamp": timestamp,
        "session_id": session_id,
        "actor": {
            "type": "script",
            "name": "generate_sejr.py",
            "model_id": None
        },
        "action": "SEJR_CREATED",
        "target": {
            "file": "SEJR_LISTE.md",
            "section": "Init"
        },
        "details": {
            "sejr_name": name,
            "folder": folder_name,
            "files_created": ["SEJR_LISTE.md", "CLAUDE.md", "STATUS.yaml", "AUTO_LOG.jsonl"]
        },
        "pass": 1
    }
    log_file.write_text(json.dumps(log_entry) + "\n", encoding="utf-8")
    print(f"✅ File 4/4: {log_file.name}")

    # ═══════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════

    print(f"\n{'═' * 60}")
    print(f"🎯 SEJR OPRETTET: {name}")
    print(f"{'═' * 60}")
    print(f"\n📁 Mappe: {sejr_path}")
    print(f"\n📋 STRØMLINET - Kun 4 filer (Single Source of Truth):")
    print(f"   1. SEJR_LISTE.md  → Opgaver og checkboxes")
    print(f"   2. CLAUDE.md      → Fokus lock (genereret)")
    print(f"   3. STATUS.yaml    → ALT status (unified)")
    print(f"   4. AUTO_LOG.jsonl → ALT logging (master)")
    print(f"\n📊 Session ID: {session_id}")
    print(f"\n🚀 START:")
    print(f"   1. Åbn SEJR_LISTE.md")
    print(f"   2. Start med PHASE 0")
    print(f"   3. Afkryds checkboxes")
    print(f"\n✅ INGEN REDUNDANS - Alt data kun ét sted!")
    print(f"{'═' * 60}\n")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate new SEJR (Streamlined - 4 files only)"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Name of the sejr"
    )
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent
    generate_sejr(args.name, system_path)
