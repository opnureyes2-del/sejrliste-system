#!/usr/bin/env python3
"""
Auto-archive completed sejr lister with 3-PASS ENFORCEMENT
Part of SEJR LISTE SYSTEM - DNA Layer 5 (SELF-ARCHIVING)

INGEN EXTERNAL DEPENDENCIES - Kun Python standard library

3-PASS REGEL:
Kan KUN arkivere når:
- Pass 1 complete
- Pass 2 complete (score > Pass 1)
- Pass 3 complete (score > Pass 2)
- Final verification complete (5+ tests)
- Total score >= 24/30
"""

import argparse
import shutil
import re
from pathlib import Path
from datetime import datetime


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
                    elif value == "null":
                        value = None
                    elif value.replace(".", "").replace("-", "").isdigit():
                        value = float(value) if "." in value else int(value)
                    result[key] = value
    except:
        pass
    return result


def write_yaml_simple(filepath: Path, data: dict):
    """Write simple YAML without PyYAML."""
    lines = [f"# Archive metadata - {datetime.now().isoformat()}"]
    for key, value in data.items():
        if isinstance(value, bool):
            value_str = "true" if value else "false"
        elif isinstance(value, (int, float)):
            value_str = str(value)
        elif value is None:
            value_str = "null"
        else:
            value_str = f'"{value}"'
        lines.append(f"{key}: {value_str}")

    filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ============================================================================
# 3-PASS ARCHIVE ENFORCEMENT
# ============================================================================

def check_3pass_complete(sejr_path: Path) -> dict:
    """Check if all 3 passes are complete and scores improve."""
    status_file = sejr_path / "STATUS.yaml"

    if not status_file.exists():
        return {
            "can_archive": False,
            "reason": "STATUS.yaml ikke fundet - kør auto_verify.py først"
        }

    status = parse_yaml_simple(status_file)

    # Check can_archive flag
    if status.get("can_archive", False):
        return {
            "can_archive": True,
            "total_score": status.get("total_score", 0),
            "current_pass": status.get("current_pass", 0),
        }

    # Build detailed reason
    reasons = []

    if not status.get("pass_1_complete", False):
        reasons.append("Pass 1 ikke færdig")

    if not status.get("pass_2_complete", False):
        reasons.append("Pass 2 ikke færdig")
    elif status.get("pass_2_score", 0) <= status.get("pass_1_score", 0):
        reasons.append(f"Pass 2 score ({status.get('pass_2_score', 0)}) skal være højere end Pass 1 ({status.get('pass_1_score', 0)})")

    if not status.get("pass_3_complete", False):
        reasons.append("Pass 3 ikke færdig")
    elif status.get("pass_3_score", 0) <= status.get("pass_2_score", 0):
        reasons.append(f"Pass 3 score ({status.get('pass_3_score', 0)}) skal være højere end Pass 2 ({status.get('pass_2_score', 0)})")

    if not status.get("final_verification_complete", False):
        reasons.append("Final verification ikke færdig (minimum 5 tests)")

    total_score = status.get("total_score", 0)
    if total_score < 24:
        reasons.append(f"Total score for lav ({total_score}/30, minimum 24)")

    return {
        "can_archive": False,
        "reason": "\n   • ".join([""] + reasons) if reasons else "Ukendt",
        "current_pass": status.get("current_pass", 1),
        "total_score": total_score,
        "pass_1_score": status.get("pass_1_score", 0),
        "pass_2_score": status.get("pass_2_score", 0),
        "pass_3_score": status.get("pass_3_score", 0),
    }


def extract_semantic_conclusion(sejr_path: Path) -> str:
    """Extract semantic conclusion and 3-pass results from SEJR_LISTE.md"""
    sejr_file = sejr_path / "SEJR_LISTE.md"

    if not sejr_file.exists():
        return None

    content = sejr_file.read_text(encoding="utf-8")

    # Extract 3-PASS KONKURRENCE RESULTAT
    result_start = content.find("# 📊 3-PASS KONKURRENCE RESULTAT")
    if result_start == -1:
        result_start = content.find("3-PASS KONKURRENCE RESULTAT")

    # Extract SEMANTISK KONKLUSION
    conclusion_start = content.find("# 🏆 SEMANTISK KONKLUSION")
    if conclusion_start == -1:
        conclusion_start = content.find("SEMANTISK KONKLUSION")

    # Get both sections
    sections = []

    if result_start != -1:
        result_end = content.find("\n# ", result_start + 1)
        if result_end == -1:
            result_end = len(content)
        sections.append(content[result_start:result_end].strip())

    if conclusion_start != -1:
        conclusion_end = content.find("\n## 🔒 ARCHIVE LOCK", conclusion_start)
        if conclusion_end == -1:
            conclusion_end = len(content)
        sections.append(content[conclusion_start:conclusion_end].strip())

    if sections:
        return "\n\n---\n\n".join(sections)

    # Fallback: create minimal conclusion
    return None


def get_rank_from_score(total_score: int) -> tuple[str, str]:
    """Get rank name and emoji based on total score."""
    if total_score >= 27:
        return "GRAND ADMIRAL", "🏅"
    elif total_score >= 24:
        return "ADMIRAL", "🎖️"
    elif total_score >= 21:
        return "KAPTAJN", "⭐"
    elif total_score >= 18:
        return "LØJTNANT", "📊"
    else:
        return "KADET", "🔰"


def extract_learnings_and_patterns(sejr_path: Path) -> dict:
    """Extract learnings, patterns, and tips from SEJR_LISTE.md"""
    sejr_file = sejr_path / "SEJR_LISTE.md"
    result = {
        'learnings': '_Ikke dokumenteret_',
        'patterns': '_Ikke dokumenteret_',
        'reusable': '_Ikke dokumenteret_',
        'tips': '_Ikke dokumenteret_',
        'p1_approach': '_Ikke dokumenteret_',
        'p2_approach': '_Ikke dokumenteret_',
        'p3_approach': '_Ikke dokumenteret_',
        'achievement_summary': '_Ikke dokumenteret_',
    }

    if not sejr_file.exists():
        return result

    content = sejr_file.read_text(encoding="utf-8")

    # Extract from SEMANTISK KONKLUSION section
    # Look for "SEMANTISK KONKLUSION" with or without emoji
    conclusion_start = content.find("SEMANTISK KONKLUSION")
    if conclusion_start == -1:
        conclusion_start = content.find("🏆 SEMANTISK")

    if conclusion_start != -1:
        conclusion_section = content[conclusion_start:]

        # Extract learnings - match both ## and ### headers
        learn_match = re.search(r'##+ Hvad Lærte Vi[^\n]*\n(.*?)(?=##|\n---|\Z)', conclusion_section, re.DOTALL)
        if learn_match:
            learnings = learn_match.group(1).strip()
            # Clean up placeholder text
            if learnings and not learnings.startswith('_'):
                result['learnings'] = learnings

        # Extract reusable - match both ## and ### headers
        reusable_match = re.search(r'##+ Hvad Kan Genbruges[^\n]*\n(.*?)(?=##|\n---|\Z)', conclusion_section, re.DOTALL)
        if reusable_match:
            reusable = reusable_match.group(1).strip()
            if reusable and not reusable.startswith('_'):
                result['reusable'] = reusable

    # Extract improvement descriptions as approach summaries
    p1_match = re.search(r'Pass 1[^:]*→[^:]*Forbedring\s*\n(.*?)(?=###|Pass \d|\n---|\Z)', content, re.DOTALL)
    if p1_match:
        approach = p1_match.group(1).strip()
        if approach and len(approach) > 10:
            result['p1_approach'] = approach[:200]

    p2_match = re.search(r'Pass 2[^:]*→[^:]*Forbedring\s*\n(.*?)(?=###|Pass \d|\n---|\Z)', content, re.DOTALL)
    if p2_match:
        approach = p2_match.group(1).strip()
        if approach and len(approach) > 10:
            result['p2_approach'] = approach[:200]

    # Try to extract achievement from project brief
    brief_file = sejr_path / "PROJECT_BRIEF.md"
    if brief_file.exists():
        try:
            brief = brief_file.read_text(encoding="utf-8")
            goal_match = re.search(r'\*\*MÅL:\*\*\s*(.*?)(?=\n\*\*|\n---|\n\n|\Z)', brief, re.DOTALL)
            if goal_match:
                result['achievement_summary'] = goal_match.group(1).strip()
        except:
            pass

    return result


def generate_sejr_diplom(sejr_path: Path, archive_path: Path, status: dict) -> Path:
    """Generate SEJR_DIPLOM.md from template with all data filled in."""
    template_path = sejr_path.parent.parent / "00_TEMPLATES" / "SEJR_DIPLOM.md"

    # Get scores
    p1_score = status.get('pass_1_score', 0)
    p2_score = status.get('pass_2_score', 0)
    p3_score = status.get('pass_3_score', 0)
    total_score = status.get('total_score', 0)

    # Get rank
    rank_name, rank_emoji = get_rank_from_score(total_score)

    # Calculate improvements
    p2_improvement = f"+{p2_score - p1_score}" if p2_score > p1_score else "0"
    p3_improvement = f"+{p3_score - p2_score}" if p3_score > p2_score else "0"
    total_improvement = f"+{(p2_score - p1_score) + (p3_score - p2_score)}"

    # Get checkbox counts from STATUS.yaml
    p1_checkboxes = status.get('pass_1_checkboxes', 'N/A')
    p2_checkboxes = status.get('pass_2_checkboxes', 'N/A')
    p3_checkboxes = status.get('pass_3_checkboxes', 'N/A')
    total_checkboxes = f"{p1_checkboxes}+{p2_checkboxes}+{p3_checkboxes}"

    # Get learnings and patterns
    learnings = extract_learnings_and_patterns(sejr_path)

    # Build diplom content
    sejr_name = sejr_path.name
    archive_date = datetime.now().strftime('%Y-%m-%d %H:%M')

    diplom_content = f"""# 🏆 SEJR DIPLOM

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    {rank_emoji}  SEJR DIPLOM  {rank_emoji}                           ║
║                                                                  ║
║  ┌────────────────────────────────────────────────────────────┐  ║
║  │                                                            │  ║
║  │   SEJR: {sejr_name[:50]:<50}│  ║
║  │                                                            │  ║
║  │   DATO: {archive_date:<52}│  ║
║  │                                                            │  ║
║  │   SCORE: {total_score}/30{' ':<49}│  ║
║  │                                                            │  ║
║  │   RANG: {rank_name:<53}│  ║
║  │                                                            │  ║
║  └────────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║                     ✅ 3-PASS GENNEMFØRT                         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📊 3-PASS RESULTATER

| Pass | Checkboxes | Score | Forbedring |
|------|------------|-------|------------|
| 🥉 Pass 1 | {p1_checkboxes} | {p1_score}/10 | Baseline |
| 🥈 Pass 2 | {p2_checkboxes} | {p2_score}/10 | {p2_improvement} |
| 🥇 Pass 3 | {p3_checkboxes} | {p3_score}/10 | {p3_improvement} |
| **TOTAL** | **{total_checkboxes}** | **{total_score}/30** | **{total_improvement}** |

---

## 🎯 HVAD BLEV OPNÅET

{learnings['achievement_summary']}

---

## 📚 LÆRING (Kan Genbruges)

### Hvad Lærte Vi
{learnings['learnings']}

### Patterns Identificeret
{learnings['patterns']}

### Genbrugelig Kode/Templates
{learnings['reusable']}

---

## 🔍 EKSEMPEL FOR ANDRE

> **Hvis du er i tvivl om hvordan man gennemfører en sejr, se dette eksempel:**

### Sådan Gjorde Vi

1. **PASS 1 (Fungerende):** {learnings['p1_approach']}
2. **PASS 2 (Forbedret):** {learnings['p2_approach']}
3. **PASS 3 (Optimeret):** {learnings['p3_approach']}

### Tips Til Næste Gang
{learnings['tips']}

---

## 📁 FILER I DENNE ARKIVERING

| Fil | Formål |
|-----|--------|
| `SEJR_DIPLOM.md` | Denne fil - bevis og showcase |
| `CONCLUSION.md` | Semantisk konklusion (kort) |
| `STATUS.yaml` | Final status med scores |
| `AUTO_LOG.jsonl` | Komplet handlingslog |
| `ARCHIVE_METADATA.yaml` | Metadata om arkivering |

---

## ✅ VERIFICERET AF

- **System:** Sejrliste 3-Pass Konkurrence System
- **Dato:** {archive_date}
- **Verification:** auto_verify.py ✅
- **Archive:** auto_archive.py ✅

---

```
════════════════════════════════════════════════════════════════════
                    DETTE DIPLOM ER PERMANENT
           Kan bruges som reference og bevis for arbejde
════════════════════════════════════════════════════════════════════
```
"""

    diplom_file = archive_path / "SEJR_DIPLOM.md"
    diplom_file.write_text(diplom_content, encoding="utf-8")
    return diplom_file


def create_archive_conclusion(sejr_path: Path, archive_path: Path, status: dict):
    """Create comprehensive archive conclusion file."""
    conclusion = extract_semantic_conclusion(sejr_path)

    # Create CONCLUSION.md
    conclusion_file = archive_path / "CONCLUSION.md"

    content = f"""# {sejr_path.name}

**Archived:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Status:** ✅ 3-PASS COMPLETE

---

## 📊 FINAL SCORES

| Pass | Score |
|------|-------|
| Pass 1 | {status.get('pass_1_score', 'N/A')}/10 |
| Pass 2 | {status.get('pass_2_score', 'N/A')}/10 |
| Pass 3 | {status.get('pass_3_score', 'N/A')}/10 |
| **TOTAL** | **{status.get('total_score', 'N/A')}/30** |

---

"""

    if conclusion:
        content += conclusion
    else:
        content += """## SEMANTISK KONKLUSION

*Konklusion ikke udfyldt i SEJR_LISTE.md*

### Hvad Lærte Vi
_Ikke dokumenteret_

### Hvad Kan Genbruges
_Ikke dokumenteret_
"""

    content += f"""

---

## ARCHIVE METADATA

- **Original path:** `{sejr_path}`
- **Archived by:** auto_archive.py (DNA Layer 5)
- **Archive timestamp:** {datetime.now().isoformat()}
- **3-Pass verified:** ✅
"""

    conclusion_file.write_text(content, encoding="utf-8")
    return conclusion_file


def archive_sejr(sejr_name: str, system_path: Path, force: bool = False):
    """Archive a completed sejr liste with 3-pass verification."""
    sejr_path = system_path / "10_ACTIVE" / sejr_name

    if not sejr_path.exists():
        print(f"❌ Sejr not found: {sejr_name}")
        return False

    # Check 3-pass completion
    check = check_3pass_complete(sejr_path)

    if not check["can_archive"] and not force:
        print(f"\n🔒 ARKIVERING BLOKERET for: {sejr_name}")
        print(f"\n   Årsag:{check['reason']}")
        print(f"\n   Current pass: {check.get('current_pass', '?')}/3")
        print(f"   Total score: {check.get('total_score', 0)}/30")
        print(f"\n   Kør først: python scripts/auto_verify.py --sejr \"{sejr_name}\"")
        print(f"   Eller brug --force for at omgå (IKKE ANBEFALET)")
        return False

    if force and not check["can_archive"]:
        print(f"\n⚠️  FORCE ARCHIVE - Omgår 3-pass verification!")
        print(f"   Dette er IKKE i overensstemmelse med Sejrliste System regler.")
        print(f"   Årsag for blokering:{check['reason']}")
        print()

    print(f"📦 Archiving: {sejr_name}\n")

    # Create archive directory
    archive_dir = system_path / "90_ARCHIVE"
    archive_dir.mkdir(exist_ok=True)

    # Create timestamped archive folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = archive_dir / f"{sejr_name}_{timestamp}"
    archive_path.mkdir(exist_ok=True)

    print(f"📁 Archive location: {archive_path}")

    # Get final status
    status = parse_yaml_simple(sejr_path / "STATUS.yaml")

    # Create conclusion file with scores
    conclusion_file = create_archive_conclusion(sejr_path, archive_path, status)
    print(f"✅ Saved conclusion: {conclusion_file}")

    # Generate SEJR DIPLOM
    diplom_file = generate_sejr_diplom(sejr_path, archive_path, status)
    rank_name, rank_emoji = get_rank_from_score(status.get('total_score', 0))
    print(f"🏆 Generated diplom: {diplom_file}")
    print(f"   {rank_emoji} RANG: {rank_name}")

    # Copy important files
    for file_name in ["STATUS.yaml", "AUTO_LOG.jsonl"]:
        src = sejr_path / file_name
        if src.exists():
            dst = archive_path / file_name
            shutil.copy2(src, dst)
            print(f"✅ Copied: {file_name}")

    # Create archive metadata
    metadata = {
        'sejr_name': sejr_name,
        'archived_at': datetime.now().isoformat(),
        'original_path': str(sejr_path),
        'archive_path': str(archive_path),
        'archived_by': 'auto_archive.py',
        'force_archived': force and not check["can_archive"],
        'pass_1_score': status.get('pass_1_score', 0),
        'pass_2_score': status.get('pass_2_score', 0),
        'pass_3_score': status.get('pass_3_score', 0),
        'total_score': status.get('total_score', 0),
        'three_pass_verified': check["can_archive"],
    }

    metadata_file = archive_path / "ARCHIVE_METADATA.yaml"
    write_yaml_simple(metadata_file, metadata)
    print(f"✅ Created: {metadata_file}")

    # Remove from 10_ACTIVE
    print(f"\n🗑️  Removing from 10_ACTIVE: {sejr_path}")
    shutil.rmtree(sejr_path)

    print(f"\n✅ ARCHIVE COMPLETE")
    print(f"   3-Pass verified: {'✅' if check['can_archive'] else '❌ (forced)'}")
    print(f"   Total score: {status.get('total_score', 0)}/30")
    print(f"   {rank_emoji} Rang: {rank_name}")
    print(f"   Location: {archive_path}")

    # Update archive index
    print(f"\n📋 Updating archive index...")
    update_archive_index(system_path)

    return True


def update_archive_index(system_path: Path):
    """Update INDEX.md in 90_ARCHIVE/ with all completed sejr."""
    archive_dir = system_path / "90_ARCHIVE"

    if not archive_dir.exists():
        return

    # Collect all archived sejr with their data
    archived_sejr = []

    for folder in sorted(archive_dir.iterdir(), reverse=True):
        if not folder.is_dir() or folder.name.startswith('.'):
            continue

        status_file = folder / "STATUS.yaml"
        metadata_file = folder / "ARCHIVE_METADATA.yaml"

        status = parse_yaml_simple(status_file) if status_file.exists() else {}
        metadata = parse_yaml_simple(metadata_file) if metadata_file.exists() else {}

        total_score = status.get('total_score', 0)
        rank_name, rank_emoji = get_rank_from_score(total_score)

        archived_sejr.append({
            'name': folder.name,
            'path': folder,
            'total_score': total_score,
            'pass_1_score': status.get('pass_1_score', 0),
            'pass_2_score': status.get('pass_2_score', 0),
            'pass_3_score': status.get('pass_3_score', 0),
            'rank_name': rank_name,
            'rank_emoji': rank_emoji,
            'archived_at': metadata.get('archived_at', 'Unknown'),
            'has_diplom': (folder / "SEJR_DIPLOM.md").exists(),
        })

    # Generate INDEX.md
    total_archived = len(archived_sejr)
    grand_admirals = sum(1 for s in archived_sejr if s['total_score'] >= 27)
    admirals = sum(1 for s in archived_sejr if 24 <= s['total_score'] < 27)
    avg_score = sum(s['total_score'] for s in archived_sejr) / total_archived if total_archived > 0 else 0

    content = f"""# 🏆 SEJRLISTE ARKIV INDEX

> **Permanent bevis på alt færdiggjort arbejde**

---

## 📊 STATISTIK

| Metric | Værdi |
|--------|-------|
| **Total Arkiveret** | {total_archived} sejr |
| **Grand Admiral (27-30)** | {grand_admirals} |
| **Admiral (24-26)** | {admirals} |
| **Gennemsnitlig Score** | {avg_score:.1f}/30 |

---

## 🎖️ ALLE FÆRDIGE SEJR

| Rang | Sejr | Score | P1 | P2 | P3 | Diplom |
|------|------|-------|----|----|----|----|
"""

    for sejr in archived_sejr:
        diplom_link = f"[🏆]({sejr['name']}/SEJR_DIPLOM.md)" if sejr['has_diplom'] else "❌"
        content += f"| {sejr['rank_emoji']} {sejr['rank_name']} | [{sejr['name'][:40]}]({sejr['name']}/) | **{sejr['total_score']}/30** | {sejr['pass_1_score']} | {sejr['pass_2_score']} | {sejr['pass_3_score']} | {diplom_link} |\n"

    content += f"""

---

## 🔍 SÅDAN BRUGER DU ARKIVET

1. **Find inspiration:** Se hvordan andre sejr blev gennemført
2. **Lær af mønstre:** Tjek SEJR_DIPLOM.md for læring og tips
3. **Genbrug kode:** Se "Hvad Kan Genbruges" sektionen i diplomet
4. **Bevis arbejde:** Brug diplomet som reference

---

## 📁 MAPPE STRUKTUR

Hver arkiveret sejr indeholder:

```
{'{sejr_name}_TIMESTAMP'}/
├── SEJR_DIPLOM.md          # 🏆 Bevis og showcase
├── CONCLUSION.md           # Semantisk konklusion
├── STATUS.yaml             # Final status med scores
├── AUTO_LOG.jsonl          # Komplet handlingslog
└── ARCHIVE_METADATA.yaml   # Metadata om arkivering
```

---

**Sidst opdateret:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Genereret af:** auto_archive.py
"""

    index_file = archive_dir / "INDEX.md"
    index_file.write_text(content, encoding="utf-8")
    print(f"📋 Updated: {index_file}")
    return index_file


def list_completed_sejr(system_path: Path):
    """List all sejr ready for archiving (3-pass complete)."""
    active_dir = system_path / "10_ACTIVE"

    if not active_dir.exists():
        print("ℹ️  No 10_ACTIVE directory")
        return

    ready = []
    not_ready = []

    for sejr_folder in active_dir.iterdir():
        if not sejr_folder.is_dir():
            continue

        check = check_3pass_complete(sejr_folder)

        if check["can_archive"]:
            ready.append({
                'name': sejr_folder.name,
                'path': sejr_folder,
                'score': check.get('total_score', 0)
            })
        else:
            not_ready.append({
                'name': sejr_folder.name,
                'path': sejr_folder,
                'pass': check.get('current_pass', 1),
                'score': check.get('total_score', 0),
                'reason': check.get('reason', 'Unknown')
            })

    print("\n" + "=" * 60)
    print("📦 ARCHIVE STATUS")
    print("=" * 60)

    if ready:
        print(f"\n✅ READY TO ARCHIVE ({len(ready)}):\n")
        for sejr in ready:
            print(f"   🏆 {sejr['name']}")
            print(f"      Score: {sejr['score']}/30")
            print()
        print(f"Archive with: python scripts/auto_archive.py --sejr \"<name>\"")
    else:
        print("\n✅ Ingen sejr klar til arkivering")

    if not_ready:
        print(f"\n🔒 NOT READY ({len(not_ready)}):\n")
        for sejr in not_ready:
            print(f"   ⏳ {sejr['name']}")
            print(f"      Pass: {sejr['pass']}/3 | Score: {sejr['score']}/30")
            print()

    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Archive completed sejr liste (requires 3-pass completion)"
    )
    parser.add_argument("--sejr", help="Name of sejr folder to archive")
    parser.add_argument("--force", action="store_true",
                       help="Force archive even if 3-pass not complete (NOT RECOMMENDED)")
    parser.add_argument("--list", action="store_true",
                       help="List sejr ready for archiving")
    parser.add_argument("--update-index", action="store_true",
                       help="Update INDEX.md in 90_ARCHIVE/")
    parser.add_argument("--generate-diploms", action="store_true",
                       help="Generate SEJR_DIPLOM.md for all archived sejr that don't have one")
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent

    if args.update_index:
        update_archive_index(system_path)
    elif args.generate_diploms:
        # Generate diploms for existing archives
        archive_dir = system_path / "90_ARCHIVE"
        generated = 0
        for folder in archive_dir.iterdir():
            if not folder.is_dir() or folder.name.startswith('.'):
                continue
            diplom_file = folder / "SEJR_DIPLOM.md"
            if not diplom_file.exists():
                status = parse_yaml_simple(folder / "STATUS.yaml")
                if status:
                    generate_sejr_diplom(folder, folder, status)
                    rank_name, rank_emoji = get_rank_from_score(status.get('total_score', 0))
                    print(f"🏆 Generated: {folder.name} ({rank_emoji} {rank_name})")
                    generated += 1
        print(f"\n✅ Generated {generated} diploms")
        update_archive_index(system_path)
    elif args.list:
        list_completed_sejr(system_path)
    elif args.sejr:
        archive_sejr(args.sejr, system_path, force=args.force)
    else:
        print("Usage: auto_archive.py --sejr <name> [--force]")
        print("   or: auto_archive.py --list")
        print("\n⚠️  BEMÆRK: Arkivering kræver 3-pass completion!")
        print("   - Pass 1 ✅")
        print("   - Pass 2 ✅ (score > Pass 1)")
        print("   - Pass 3 ✅ (score > Pass 2)")
        print("   - Final verification ✅ (5+ tests)")
        print("   - Total score >= 24/30")
