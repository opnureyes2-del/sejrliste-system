#!/usr/bin/env python3
"""
BUILD CLAUDE CONTEXT - Dynamisk CLAUDE.md generator
====================================================

Bygger en SPECIFIK CLAUDE.md baseret på:
1. Den faktiske opgave i SEJR_LISTE.md
2. Current state fra STATUS.yaml
3. Næste uafkrydsede checkbox
4. Faktiske scores og blockers

DETTE ER IKKE EN TEMPLATE - DET ER LEVENDE KONTEKST.
"""

import re
import json
from pathlib import Path
from datetime import datetime


def parse_yaml_simple(filepath: Path) -> dict:
    """Parse simple YAML."""
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
                    elif value == "null":
                        value = None
                    elif value.replace(".", "").replace("-", "").isdigit():
                        value = float(value) if "." in value else int(value)
                    result[key] = value
    except:
        pass
    return result


def extract_task_name(sejr_file: Path) -> str:
    """Extract the actual task name from SEJR_LISTE.md."""
    if not sejr_file.exists():
        return "Ukendt opgave"

    content = sejr_file.read_text(encoding="utf-8")

    # Find title line
    for line in content.split("\n"):
        if line.startswith("# SEJR:"):
            return line.replace("# SEJR:", "").strip()

    return sejr_file.parent.name


def extract_next_unchecked(sejr_file: Path) -> dict:
    """Find the SPECIFIC next unchecked checkbox with context."""
    if not sejr_file.exists():
        return {"task": "Åbn SEJR_LISTE.md", "section": "Unknown", "line": 0}

    content = sejr_file.read_text(encoding="utf-8")
    lines = content.split("\n")

    current_section = "Unknown"
    current_pass = "Unknown"

    for i, line in enumerate(lines, 1):
        # Track sections
        if line.startswith("# "):
            if "PASS 1" in line:
                current_pass = "Pass 1"
            elif "PASS 2" in line:
                current_pass = "Pass 2"
            elif "PASS 3" in line:
                current_pass = "Pass 3"

        if line.startswith("## "):
            current_section = line.replace("## ", "").strip()
        elif line.startswith("### "):
            current_section = line.replace("### ", "").strip()

        # Find unchecked checkbox
        if re.match(r'^- \[ \]', line.strip()):
            task = line.strip()[6:].strip()
            # Clean up task text
            task = re.sub(r'\s+', ' ', task)
            if len(task) > 100:
                task = task[:100] + "..."

            return {
                "task": task,
                "section": current_section,
                "pass": current_pass,
                "line": i
            }

    return {"task": "Alle checkboxes afkrydsede", "section": "Done", "line": 0}


def count_checkboxes_by_pass(sejr_file: Path) -> dict:
    """Count checkboxes for each pass."""
    if not sejr_file.exists():
        return {}

    content = sejr_file.read_text(encoding="utf-8")

    result = {
        "pass_1": {"done": 0, "total": 0},
        "pass_2": {"done": 0, "total": 0},
        "pass_3": {"done": 0, "total": 0},
    }

    current_pass = None

    for line in content.split("\n"):
        if "PASS 1" in line and line.startswith("#"):
            current_pass = "pass_1"
        elif "PASS 2" in line and line.startswith("#"):
            current_pass = "pass_2"
        elif "PASS 3" in line and line.startswith("#"):
            current_pass = "pass_3"
        elif "SEMANTISK KONKLUSION" in line:
            current_pass = None

        if current_pass:
            if re.match(r'^- \[[xX]\]', line.strip()):
                result[current_pass]["done"] += 1
                result[current_pass]["total"] += 1
            elif re.match(r'^- \[ \]', line.strip()):
                result[current_pass]["total"] += 1

    return result


def determine_current_pass(checkbox_counts: dict, status: dict) -> int:
    """Determine which pass we're actually on."""
    p1 = checkbox_counts.get("pass_1", {"done": 0, "total": 0})
    p2 = checkbox_counts.get("pass_2", {"done": 0, "total": 0})
    p3 = checkbox_counts.get("pass_3", {"done": 0, "total": 0})

    # If Pass 1 not complete
    if p1["total"] > 0 and p1["done"] < p1["total"]:
        return 1

    # If Pass 2 not complete
    if p2["total"] > 0 and p2["done"] < p2["total"]:
        return 2

    # If Pass 3 not complete
    if p3["total"] > 0 and p3["done"] < p3["total"]:
        return 3

    # All complete
    return 3


def build_specific_rules(task_name: str, next_task: dict) -> str:
    """Build rules SPECIFIC to this task."""
    rules = f"""
## 🎯 DIN SPECIFIKKE OPGAVE

**Opgave:** {task_name}

**Lige nu skal du:**
```
{next_task['task']}
```

**Sektion:** {next_task.get('section', 'Unknown')}
**Linje:** {next_task.get('line', 'Unknown')} i SEJR_LISTE.md

---

## ⛔ SPECIFIKT FOR DENNE OPGAVE

Du må IKKE:
- Arbejde på andre opgaver end "{task_name}"
- Skippe "{next_task['task']}"
- Starte nye features før denne checkbox er afkrydset
- Sige "det er færdigt" uden at afkrydse checkbox

Du SKAL:
- Fokusere KUN på: {next_task['task']}
- Afkrydse checkbox når færdig
- Gå til næste checkbox efter
"""
    return rules


def build_claude_md(sejr_path: Path) -> str:
    """Build a SPECIFIC, DYNAMIC CLAUDE.md."""
    sejr_file = sejr_path / "SEJR_LISTE.md"
    status_file = sejr_path / "STATUS.yaml"

    # Get actual data
    status = parse_yaml_simple(status_file)
    task_name = extract_task_name(sejr_file)
    next_task = extract_next_unchecked(sejr_file)
    checkbox_counts = count_checkboxes_by_pass(sejr_file)
    current_pass = determine_current_pass(checkbox_counts, status)

    # Calculate actual progress
    p1 = checkbox_counts.get("pass_1", {"done": 0, "total": 1})
    p2 = checkbox_counts.get("pass_2", {"done": 0, "total": 1})
    p3 = checkbox_counts.get("pass_3", {"done": 0, "total": 1})

    p1_pct = int(p1["done"] / p1["total"] * 100) if p1["total"] > 0 else 0
    p2_pct = int(p2["done"] / p2["total"] * 100) if p2["total"] > 0 else 0
    p3_pct = int(p3["done"] / p3["total"] * 100) if p3["total"] > 0 else 0

    # Determine blocker
    if current_pass == 1:
        blocker = f"Færdiggør Pass 1 ({p1['done']}/{p1['total']} done)"
    elif current_pass == 2:
        blocker = f"Færdiggør Pass 2 ({p2['done']}/{p2['total']} done)"
    else:
        blocker = f"Færdiggør Pass 3 ({p3['done']}/{p3['total']} done)"

    if status.get("can_archive"):
        blocker = "INTET - Klar til arkivering"

    # Build the SPECIFIC content
    content = f"""# 🔒 CLAUDE FOKUS LOCK

> **LÆS DETTE FØR DU GØR NOGET**

---

## ⚡ CURRENT STATE

| | |
|---|---|
| **Opgave** | {task_name} |
| **Pass** | {current_pass}/3 |
| **Blokeret af** | {blocker} |
| **Sidst opdateret** | {datetime.now().strftime("%Y-%m-%d %H:%M")} |

---

{build_specific_rules(task_name, next_task)}

---

## 📊 FAKTISK PROGRESS

### Pass 1: Planlægning
```
[{"█" * (p1_pct // 10)}{"░" * (10 - p1_pct // 10)}] {p1_pct}% ({p1['done']}/{p1['total']})
```

### Pass 2: Eksekvering
```
[{"█" * (p2_pct // 10)}{"░" * (10 - p2_pct // 10)}] {p2_pct}% ({p2['done']}/{p2['total']})
```

### Pass 3: 7-DNA Review
```
[{"█" * (p3_pct // 10)}{"░" * (10 - p3_pct // 10)}] {p3_pct}% ({p3['done']}/{p3['total']})
```

### Scores
| Pass | Score | Krav |
|------|-------|------|
| Pass 1 | {status.get('pass_1_score', 0)}/10 | Baseline |
| Pass 2 | {status.get('pass_2_score', 0)}/10 | > Pass 1 |
| Pass 3 | {status.get('pass_3_score', 0)}/10 | > Pass 2 |
| **Total** | **{status.get('total_score', 0)}/30** | **≥ 24** |

---

## 🚨 ANTI-DUM CHECKPOINT

Før du gør NOGET, bekræft:

- [ ] Jeg arbejder på: **{task_name}**
- [ ] Min næste handling er: **{next_task['task'][:50]}...**
- [ ] Jeg er på Pass: **{current_pass}**
- [ ] Jeg vil afkrydse checkbox når færdig: **JA**

**Hvis du ikke kan bekræfte alle 4 → STOP og genlæs denne fil**

---

## 📁 FILER DU SKAL BRUGE

| Fil | Hvad | Handling |
|-----|------|----------|
| `SEJR_LISTE.md` | Alle opgaver | Afkryds her |
| `CLAUDE.md` | Denne fil | Genlæs ved tvivl |
| `STATUS.yaml` | Auto-status | Rør ikke |
| `AUTO_LOG.jsonl` | Auto-log | Rør ikke |

---

## ⛔ FORBUDT

1. ❌ Arbejde på andet end "{task_name}"
2. ❌ Skippe til næste pass før current er 100%
3. ❌ Glemme at afkrydse checkboxes
4. ❌ "Forbedre" ting uden for scope
5. ❌ Sige "færdig" uden bevis

---

## ✅ NÅR DU HAR GJORT CURRENT TASK

1. Afkryds `- [ ]` til `- [x]` i SEJR_LISTE.md linje {next_task.get('line', '?')}
2. Kør: `python scripts/build_claude_context.py --sejr "{sejr_path.name}"`
3. Læs opdateret CLAUDE.md
4. Fortsæt til næste checkbox

---

## 🎖️ ADMIRAL KOMMANDO

> Du er her for at færdiggøre **{task_name}**.
> Din næste handling er **{next_task['task'][:40]}...**.
> Intet andet. Fokusér. Eksekver. Bevis.

---

**Auto-genereret:** {datetime.now().isoformat()}
**Baseret på:** Faktisk state fra SEJR_LISTE.md og STATUS.yaml
"""
    return content


def update_sejr(sejr_path: Path):
    """Update CLAUDE.md for a specific sejr."""
    claude_content = build_claude_md(sejr_path)
    claude_file = sejr_path / "CLAUDE.md"
    claude_file.write_text(claude_content, encoding="utf-8")

    print(f"✅ CLAUDE.md opdateret: {claude_file}")

    # Also print current state
    status = parse_yaml_simple(sejr_path / "STATUS.yaml")
    next_task = extract_next_unchecked(sejr_path / "SEJR_LISTE.md")

    print(f"\n{'─' * 50}")
    print(f"🔒 FOKUS LOCK AKTIVERET")
    print(f"{'─' * 50}")
    print(f"   Opgave: {extract_task_name(sejr_path / 'SEJR_LISTE.md')}")
    print(f"   Pass: {status.get('current_pass', 1)}/3")
    print(f"   Næste: {next_task['task'][:50]}...")
    print(f"   Score: {status.get('total_score', 0)}/30")
    print(f"{'─' * 50}\n")


def update_all(system_path: Path):
    """Update all active sejr."""
    active_dir = system_path / "10_ACTIVE"

    if not active_dir.exists():
        print("❌ Ingen 10_ACTIVE mappe")
        return

    sejr_folders = [f for f in active_dir.iterdir() if f.is_dir()]

    if not sejr_folders:
        print("ℹ️  Ingen aktive sejr")
        return

    for sejr_path in sejr_folders:
        update_sejr(sejr_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Build SPECIFIC CLAUDE.md based on actual task state"
    )
    parser.add_argument("--sejr", help="Specific sejr folder name")
    parser.add_argument("--all", action="store_true", help="Update all active")
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent

    if args.all:
        update_all(system_path)
    elif args.sejr:
        sejr_path = system_path / "10_ACTIVE" / args.sejr
        if sejr_path.exists():
            update_sejr(sejr_path)
        else:
            print(f"❌ Ikke fundet: {sejr_path}")
    else:
        update_all(system_path)
