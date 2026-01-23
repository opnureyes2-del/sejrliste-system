#!/usr/bin/env python3
"""
Generate new SEJR liste from template
Part of SEJR LISTE SYSTEM - DNA Layer 7 (SELF-OPTIMIZING)
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

def generate_sejr(name: str, system_path: Path):
    """Generate new sejr liste folder + files"""
    # Create folder name
    date = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{name.replace(' ', '_').upper()}_{date}"
    sejr_path = system_path / "10_ACTIVE" / folder_name

    # Create folder
    sejr_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {sejr_path}")

    # Copy template
    template_path = system_path / "00_TEMPLATES" / "SEJR_TEMPLATE.md"
    sejr_file = sejr_path / "SEJR_LISTE.md"

    if template_path.exists():
        # Read template
        with open(template_path, 'r') as f:
            content = f.read()

        # Replace placeholders
        content = content.replace("{OPGAVE_NAVN}", name)
        content = content.replace("{DATO}", datetime.now().strftime("%Y-%m-%d %H:%M"))
        content = content.replace("{OWNER}", "Kv1nt + Rasmus")

        # Write sejr liste
        with open(sejr_file, 'w') as f:
            f.write(content)

        print(f"✅ Generated: {sejr_file}")
    else:
        print(f"❌ Template not found: {template_path}")
        return False

    # Create AUTO_LOG.jsonl
    log_file = sejr_path / "AUTO_LOG.jsonl"
    with open(log_file, 'w') as f:
        import json
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "sejr_created",
            "name": name,
            "path": str(sejr_path)
        }
        f.write(json.dumps(log_entry) + "\n")
    print(f"✅ Created: {log_file}")

    # Create VERIFY_STATUS.yaml
    status_file = sejr_path / "VERIFY_STATUS.yaml"
    with open(status_file, 'w') as f:
        f.write(f"""# Auto-generated verification status
sejr_name: "{name}"
created: "{datetime.now().isoformat()}"
status: "in_progress"
phases_complete:
  optimization: false
  planning: false
  development: false
  verification: false
  git_workflow: false
""")
    print(f"✅ Created: {status_file}")

    print(f"\n🎯 SEJR LISTE READY: {sejr_file}")
    print(f"   Edit this file to track your progress!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate new SEJR liste")
    parser.add_argument("--name", required=True, help="Name of the sejr (e.g., 'Deploy HYBRID Agents')")
    args = parser.parse_args()

    # Find system path
    system_path = Path(__file__).parent.parent

    generate_sejr(args.name, system_path)
