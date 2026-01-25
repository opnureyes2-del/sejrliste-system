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
    print(f"   Location: {archive_path}")

    return True


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
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent

    if args.list:
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
