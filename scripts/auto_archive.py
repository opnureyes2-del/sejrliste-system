#!/usr/bin/env python3
"""
Auto-archive completed sejr lister
Part of SEJR LISTE SYSTEM - DNA Layer 5 (SELF-ARCHIVING)
"""

import argparse
import shutil
import yaml
from pathlib import Path
from datetime import datetime

def extract_semantic_conclusion(sejr_path: Path):
    """Extract only semantic conclusion from SEJR_LISTE.md"""
    sejr_file = sejr_path / "SEJR_LISTE.md"

    if not sejr_file.exists():
        return None

    with open(sejr_file, 'r') as f:
        content = f.read()

    # Find SEMANTISK KONKLUSION section
    conclusion_start = content.find("## SEMANTISK KONKLUSION")

    if conclusion_start == -1:
        return None

    # Extract from start to end of document (or next ## section)
    conclusion_section = content[conclusion_start:]

    # Find where next major section starts (if any)
    next_section = conclusion_section.find("\n## ", len("## SEMANTISK KONKLUSION"))

    if next_section != -1:
        conclusion_section = conclusion_section[:next_section]

    return conclusion_section.strip()

def create_archive_conclusion(sejr_path: Path, archive_path: Path):
    """Create semantic conclusion file in archive"""
    conclusion = extract_semantic_conclusion(sejr_path)

    if not conclusion:
        # Create minimal conclusion
        conclusion = f"""## SEMANTISK KONKLUSION

**Sejr:** {sejr_path.name}
**Archived:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

### Hvad Lærte Vi
*Konklusion ikke udfyldt i SEJR_LISTE.md*

### Status
Sejr blev arkiveret uden fuld konklusion.
"""

    # Save as CONCLUSION.md in archive
    conclusion_file = archive_path / "CONCLUSION.md"

    with open(conclusion_file, 'w') as f:
        f.write(f"# {sejr_path.name}\n\n")
        f.write(f"**Archived:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")
        f.write(conclusion)

    return conclusion_file

def archive_sejr(sejr_name: str, system_path: Path, force: bool = False):
    """Archive a completed sejr liste"""
    sejr_path = system_path / "10_ACTIVE" / sejr_name

    if not sejr_path.exists():
        print(f"❌ Sejr not found: {sejr_name}")
        return False

    # Check if completed (unless forced)
    if not force:
        status_file = sejr_path / "VERIFY_STATUS.yaml"
        if status_file.exists():
            with open(status_file, 'r') as f:
                status = yaml.safe_load(f)

            completion = status.get('completion_percentage', 0)

            if completion < 100:
                print(f"⚠️  Sejr only {completion:.0f}% complete")
                print(f"   Use --force to archive anyway, or complete verification first")
                return False
        else:
            print(f"⚠️  No VERIFY_STATUS.yaml found - cannot confirm completion")
            print(f"   Use --force to archive anyway")
            return False

    print(f"📦 Archiving: {sejr_name}\n")

    # Create archive directory
    archive_dir = system_path / "90_ARCHIVE"
    archive_dir.mkdir(exist_ok=True)

    # Create timestamped archive folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = archive_dir / f"{sejr_name}_{timestamp}"
    archive_path.mkdir(exist_ok=True)

    print(f"📁 Archive location: {archive_path}")

    # Extract and save semantic conclusion
    conclusion_file = create_archive_conclusion(sejr_path, archive_path)
    print(f"✅ Saved conclusion: {conclusion_file}")

    # Copy VERIFY_STATUS.yaml and AUTO_LOG.jsonl (for metrics)
    for file_name in ["VERIFY_STATUS.yaml", "AUTO_LOG.jsonl"]:
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
        'archived_by': 'auto_archive.py'
    }

    metadata_file = archive_path / "ARCHIVE_METADATA.yaml"
    with open(metadata_file, 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False)

    print(f"✅ Created: {metadata_file}")

    # Remove from 10_ACTIVE
    print(f"\n🗑️  Removing from 10_ACTIVE: {sejr_path}")
    shutil.rmtree(sejr_path)

    print(f"\n✅ ARCHIVE COMPLETE")
    print(f"   Semantic conclusion saved, process details discarded")
    print(f"   Location: {archive_path}")

    return True

def list_completed_sejr(system_path: Path):
    """List all completed sejr ready for archiving"""
    active_dir = system_path / "10_ACTIVE"

    if not active_dir.exists():
        print("ℹ️  No 10_ACTIVE directory")
        return

    completed = []

    for sejr_folder in active_dir.iterdir():
        if not sejr_folder.is_dir():
            continue

        status_file = sejr_folder / "VERIFY_STATUS.yaml"
        if status_file.exists():
            with open(status_file, 'r') as f:
                status = yaml.safe_load(f)

            completion = status.get('completion_percentage', 0)

            if completion == 100:
                completed.append({
                    'name': sejr_folder.name,
                    'path': sejr_folder
                })

    if completed:
        print(f"✅ {len(completed)} completed sejr ready for archiving:\n")
        for sejr in completed:
            print(f"   • {sejr['name']}")
        print(f"\nArchive with: python scripts/auto_archive.py --sejr <name>")
    else:
        print("ℹ️  No completed sejr found (0 at 100% completion)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archive completed sejr liste")
    parser.add_argument("--sejr", help="Name of sejr folder to archive")
    parser.add_argument("--force", action="store_true",
                       help="Archive even if not 100% complete")
    parser.add_argument("--list", action="store_true",
                       help="List completed sejr ready for archiving")
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent

    if args.list:
        list_completed_sejr(system_path)
    elif args.sejr:
        archive_sejr(args.sejr, system_path, force=args.force)
    else:
        print("Usage: auto_archive.py --sejr <name> [--force]")
        print("   or: auto_archive.py --list")
