#!/usr/bin/env python3
"""
Auto-verify sejr liste completion
Part of SEJR LISTE SYSTEM - DNA Layer 3 (SELF-VERIFYING)
"""

import argparse
import subprocess
import yaml
from pathlib import Path
from datetime import datetime

def extract_verify_commands(sejr_file: Path):
    """Extract all verify commands from SEJR_LISTE.md"""
    with open(sejr_file, 'r') as f:
        content = f.read()

    # Find all lines with "Verify:" pattern
    verify_commands = []
    for line in content.split('\n'):
        if 'Verify:' in line or 'verify:' in line:
            # Extract command (between backticks)
            if '`' in line:
                cmd = line.split('`')[1]
                verify_commands.append(cmd)

    return verify_commands

def run_verification(sejr_path: Path):
    """Run all verify commands for a sejr liste"""
    sejr_file = sejr_path / "SEJR_LISTE.md"
    status_file = sejr_path / "VERIFY_STATUS.yaml"

    if not sejr_file.exists():
        print(f"❌ SEJR_LISTE.md not found in {sejr_path}")
        return False

    print(f"🔍 Verifying: {sejr_path.name}\n")

    # Extract verify commands
    commands = extract_verify_commands(sejr_file)

    if not commands:
        print("⚠️  No verify commands found in SEJR_LISTE.md")
        return False

    # Run each command
    results = []
    for i, cmd in enumerate(commands, 1):
        print(f"[{i}/{len(commands)}] Running: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=sejr_path
            )

            success = result.returncode == 0
            results.append({
                'command': cmd,
                'success': success,
                'stdout': result.stdout[:200] if result.stdout else '',
                'stderr': result.stderr[:200] if result.stderr else ''
            })

            status = "✅" if success else "❌"
            print(f"  {status} Exit code: {result.returncode}\n")

        except subprocess.TimeoutExpired:
            print(f"  ⏱️  Timeout (>30s)\n")
            results.append({'command': cmd, 'success': False, 'error': 'timeout'})
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
            results.append({'command': cmd, 'success': False, 'error': str(e)})

    # Update VERIFY_STATUS.yaml
    if status_file.exists():
        with open(status_file, 'r') as f:
            status = yaml.safe_load(f)
    else:
        status = {}

    status['last_verification'] = datetime.now().isoformat()
    status['total_checks'] = len(results)
    status['passed_checks'] = sum(1 for r in results if r.get('success'))
    status['failed_checks'] = len(results) - status['passed_checks']
    status['completion_percentage'] = (status['passed_checks'] / len(results) * 100) if results else 0

    # Determine phase completion
    completion = status['completion_percentage']
    if completion == 100:
        status['status'] = 'completed'
        print(f"\n🎉 SEJR COMPLETE - 100% verified!")
    elif completion >= 75:
        status['status'] = 'nearly_complete'
        print(f"\n⚡ {completion:.0f}% complete - almost there!")
    elif completion >= 50:
        status['status'] = 'in_progress'
        print(f"\n🔵 {completion:.0f}% complete - good progress")
    else:
        status['status'] = 'early_stage'
        print(f"\n🟡 {completion:.0f}% complete - keep going")

    with open(status_file, 'w') as f:
        yaml.dump(status, f, default_flow_style=False, allow_unicode=True)

    print(f"\n📊 Status updated: {status_file}")
    return status['completion_percentage'] == 100

def verify_all(system_path: Path):
    """Verify all active sejr lister"""
    active_dir = system_path / "10_ACTIVE"

    if not active_dir.exists():
        print("❌ No 10_ACTIVE directory found")
        return

    sejr_folders = [f for f in active_dir.iterdir() if f.is_dir()]

    if not sejr_folders:
        print("ℹ️  No active sejr lister found in 10_ACTIVE/")
        return

    print(f"Found {len(sejr_folders)} active sejr lister\n")
    print("=" * 60)

    for sejr_path in sejr_folders:
        run_verification(sejr_path)
        print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-verify sejr liste completion")
    parser.add_argument("--sejr", help="Specific sejr folder name to verify")
    parser.add_argument("--all", action="store_true", help="Verify all active sejr lister")
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent

    if args.all:
        verify_all(system_path)
    elif args.sejr:
        sejr_path = system_path / "10_ACTIVE" / args.sejr
        if sejr_path.exists():
            run_verification(sejr_path)
        else:
            print(f"❌ Sejr folder not found: {sejr_path}")
    else:
        # Default: verify all
        verify_all(system_path)
