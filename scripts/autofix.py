#!/usr/bin/env python3
"""
AUTOFIX - Unified System Maintenance CLI
=========================================

Konsoliderer 8 bash/python scripts til 1 Python modul med subcommands.

Usage:
    python autofix.py logs --cleanup              # Cleanup old logs
    python autofix.py db --backup                 # Backup all databases
    python autofix.py db --list                   # List databases
    python autofix.py deploy --system             # Deploy integration to projects
    python autofix.py verify --integrations       # Verify all integrations
    python autofix.py monitor --health            # Run health checks
    python autofix.py status                      # Show overall status

Created: 2026-02-05 (AUTOFIX_SCRIPTS_KONSOLIDERING sejr)
Replaces: auto_cleanup_logs.sh, daily_db_backup.sh, deploy_unified_system.sh,
          monitor_system.py, verify_all_integrations.py
"""

import argparse
import asyncio
import gzip
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import shutil

# =============================================================================
# CONFIGURATION
# =============================================================================

ELLE_ROOT = Path("/home/rasmus/Desktop/ELLE.md")
PROJECTS_ROOT = Path("/home/rasmus/Desktop/projekts/projects")
LOGS_DIR = ELLE_ROOT / "LOGS"
BACKUPS_DIR = ELLE_ROOT / "BACKUPS" / "databases"
REPORTS_DIR = ELLE_ROOT / "REPORTS"
AGENTS_ROOT = ELLE_ROOT / "AGENTS" / "agents"

# Database configurations (8 databases)
DATABASES = [
    {"name": "kommando_central", "port": 5540, "user": "kc_admin", "password": "kc_secure_2025", "database": "kommando_central"},
    {"name": "integration_hub", "port": 5538, "user": "hub_user", "password": "hub_secure_2025", "database": "integration_hub"},
    {"name": "intro_knowledge", "port": 5536, "user": "intro_user", "password": "intro_secure_2025", "database": "intro_knowledge"},
    {"name": "elle_knowledge", "port": 5537, "user": "elle_user", "password": "elle_secure_2025", "database": "elle_knowledge"},
    {"name": "kommandor", "port": 5535, "user": "kommandor", "password": "kommandor_secure_2025", "database": "kommandor_system"},
    {"name": "cosmic_library", "port": 5534, "user": "cosmic_library", "password": "cosmic_secure_password_2025", "database": "cosmic_library"},
    {"name": "ckc_admin", "port": 5533, "user": "ckc_admin", "password": "ckc_secure_password", "database": "ckc_admin"},
    {"name": "cc", "port": 5433, "user": "cirkelline", "password": "cirkelline123", "database": "command_center"},
]

# Projects for integration deployment
PROJECTS = [
    "kommandor-og-agenter",
    "cirkelline-kv1ntos",
    "commander-and-agent",
    "cirkelline-consulting",
    "cirkelline-agents",
    "lib-admin",
    "commando-center",
    "cosmic-library",
]

# Core integration files
CORE_FILES = [
    "event_bus.py",
    "cache_manager.py",
    "unified_query_api.py",
    "master_orchestrator.py",
    "cross_db_sync.py",
    "file_watcher.py",
]

# Colors
class C:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# =============================================================================
# LOGS COMMANDS
# =============================================================================

def cmd_logs_cleanup(args):
    """Cleanup old log files (replaces auto_cleanup_logs.sh)"""
    print(f"{C.BLUE}🧹 AUTOFIX: Log Cleanup{C.RESET}")
    print("=" * 60)

    deleted = 0
    kept = 0

    # Cleanup PRODUKTION agent logs (>24h)
    produktion = ELLE_ROOT / "PRODUKTION"
    if produktion.exists():
        for agent_dir in produktion.iterdir():
            if agent_dir.is_dir():
                cutoff = datetime.now() - timedelta(hours=24)
                for f in agent_dir.glob("*.json"):
                    if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                        f.unlink()
                        deleted += 1
                    else:
                        kept += 1

    # Cleanup REPORTS (>7 days)
    if REPORTS_DIR.exists():
        cutoff = datetime.now() - timedelta(days=7)
        for f in REPORTS_DIR.glob("**/*.json"):
            if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                f.unlink()
                deleted += 1

    # Cleanup LOGS (>30 days)
    if LOGS_DIR.exists():
        cutoff = datetime.now() - timedelta(days=30)
        for f in LOGS_DIR.glob("*.log"):
            if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                f.unlink()
                deleted += 1

    print(f"  {C.GREEN}✅ Deleted:{C.RESET} {deleted} old files")
    print(f"  {C.CYAN}📁 Kept:{C.RESET} {kept} recent files")

    # Log action
    log_action("logs_cleanup", {"deleted": deleted, "kept": kept})
    return 0

# =============================================================================
# DATABASE COMMANDS
# =============================================================================

def cmd_db_backup(args):
    """Backup all databases (replaces daily_db_backup.sh)"""
    print(f"{C.BLUE}💾 AUTOFIX: Database Backup{C.RESET}")
    print("=" * 60)

    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    success = 0
    failed = 0

    for db in DATABASES:
        backup_file = BACKUPS_DIR / f"{db['name']}_{timestamp}.sql.gz"
        print(f"  📦 {db['name']} (port {db['port']})... ", end="", flush=True)

        try:
            # Run pg_dump
            env = {"PGPASSWORD": db["password"]}
            result = subprocess.run(
                ["pg_dump", "-h", "localhost", "-p", str(db["port"]),
                 "-U", db["user"], db["database"]],
                capture_output=True,
                timeout=120,
                env={**dict(subprocess.os.environ), **env}
            )

            if result.returncode == 0:
                # Compress and save
                with gzip.open(backup_file, 'wb') as f:
                    f.write(result.stdout)
                size = backup_file.stat().st_size / 1024  # KB
                print(f"{C.GREEN}✅{C.RESET} ({size:.1f} KB)")
                success += 1
            else:
                print(f"{C.RED}❌ pg_dump failed{C.RESET}")
                failed += 1
        except subprocess.TimeoutExpired:
            print(f"{C.RED}❌ timeout{C.RESET}")
            failed += 1
        except FileNotFoundError:
            print(f"{C.YELLOW}⚠️ pg_dump not found{C.RESET}")
            failed += 1
        except Exception as e:
            print(f"{C.RED}❌ {e}{C.RESET}")
            failed += 1

    # Cleanup old backups (>7 days)
    retention_days = args.retention if hasattr(args, 'retention') else 7
    cutoff = datetime.now() - timedelta(days=retention_days)
    old_deleted = 0
    for f in BACKUPS_DIR.glob("*.sql.gz"):
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            f.unlink()
            old_deleted += 1

    print()
    print(f"  {C.GREEN}✅ Success:{C.RESET} {success}/{len(DATABASES)}")
    print(f"  {C.RED}❌ Failed:{C.RESET} {failed}/{len(DATABASES)}")
    print(f"  🗑️  Old backups deleted: {old_deleted}")

    log_action("db_backup", {"success": success, "failed": failed, "old_deleted": old_deleted})
    return 0 if failed == 0 else 1

def cmd_db_list(args):
    """List all configured databases"""
    print(f"{C.BLUE}📋 AUTOFIX: Database List{C.RESET}")
    print("=" * 60)
    print(f"{'Name':<20} {'Port':<8} {'Database':<25} {'User':<15}")
    print("-" * 60)
    for db in DATABASES:
        print(f"{db['name']:<20} {db['port']:<8} {db['database']:<25} {db['user']:<15}")
    return 0

# =============================================================================
# DEPLOY COMMANDS
# =============================================================================

def cmd_deploy_system(args):
    """Deploy integration system to all projects (replaces deploy_unified_system.sh)"""
    print(f"{C.BLUE}🚀 AUTOFIX: Deploy Integration System{C.RESET}")
    print("=" * 60)

    deployed = 0
    failed = 0
    skipped = 0

    for project_name in PROJECTS:
        project_path = PROJECTS_ROOT / project_name

        if not project_path.exists():
            print(f"  {C.YELLOW}⚠️ SKIP:{C.RESET} {project_name} (not found)")
            skipped += 1
            continue

        print(f"  📦 {project_name}... ", end="", flush=True)

        integration_dir = project_path / "integration"
        integration_dir.mkdir(exist_ok=True)

        files_copied = 0
        for filename in CORE_FILES:
            src = AGENTS_ROOT / filename
            if src.exists():
                shutil.copy2(src, integration_dir / filename)
                files_copied += 1

        # Create __init__.py
        init_content = '''"""
ELLE Unified Integration System
================================
Provides access to Event Bus, Cache Manager, Unified Query API,
Master Orchestrator, Cross-DB Sync, and File Watcher.
"""

__version__ = '2.0.0'
__author__ = 'ELLE.md System'
'''
        (integration_dir / "__init__.py").write_text(init_content)
        files_copied += 1

        if files_copied > 0:
            print(f"{C.GREEN}✅ {files_copied} files{C.RESET}")
            deployed += 1
        else:
            print(f"{C.RED}❌ no files{C.RESET}")
            failed += 1

    print()
    print(f"  {C.GREEN}✅ Deployed:{C.RESET} {deployed}/{len(PROJECTS)}")
    print(f"  {C.YELLOW}⚠️ Skipped:{C.RESET} {skipped}")
    print(f"  {C.RED}❌ Failed:{C.RESET} {failed}")

    log_action("deploy_system", {"deployed": deployed, "skipped": skipped, "failed": failed})
    return 0 if failed == 0 else 1

# =============================================================================
# VERIFY COMMANDS
# =============================================================================

def cmd_verify_integrations(args):
    """Verify all integrations (replaces verify_all_integrations.py)"""
    print(f"{C.BLUE}🔍 AUTOFIX: Verify Integrations{C.RESET}")
    print("=" * 60)

    results = []

    for project_name in PROJECTS:
        project_path = PROJECTS_ROOT / project_name
        integration_dir = project_path / "integration"

        result = {
            "project": project_name,
            "exists": project_path.exists(),
            "integration_dir": integration_dir.exists(),
            "files": [],
            "status": "unknown"
        }

        if not project_path.exists():
            result["status"] = "missing"
            print(f"  {C.RED}❌ {project_name}: project not found{C.RESET}")
        elif not integration_dir.exists():
            result["status"] = "no_integration"
            print(f"  {C.YELLOW}⚠️ {project_name}: no integration dir{C.RESET}")
        else:
            # Check files
            for filename in CORE_FILES + ["__init__.py"]:
                if (integration_dir / filename).exists():
                    result["files"].append(filename)

            coverage = len(result["files"]) / (len(CORE_FILES) + 1) * 100
            if coverage == 100:
                result["status"] = "complete"
                print(f"  {C.GREEN}✅ {project_name}: 100% ({len(result['files'])} files){C.RESET}")
            elif coverage > 50:
                result["status"] = "partial"
                print(f"  {C.YELLOW}⚠️ {project_name}: {coverage:.0f}% ({len(result['files'])} files){C.RESET}")
            else:
                result["status"] = "incomplete"
                print(f"  {C.RED}❌ {project_name}: {coverage:.0f}% ({len(result['files'])} files){C.RESET}")

        results.append(result)

    # Summary
    complete = sum(1 for r in results if r["status"] == "complete")
    partial = sum(1 for r in results if r["status"] == "partial")
    missing = sum(1 for r in results if r["status"] in ["missing", "no_integration", "incomplete"])

    print()
    print(f"  {C.GREEN}✅ Complete:{C.RESET} {complete}/{len(PROJECTS)}")
    print(f"  {C.YELLOW}⚠️ Partial:{C.RESET} {partial}/{len(PROJECTS)}")
    print(f"  {C.RED}❌ Missing:{C.RESET} {missing}/{len(PROJECTS)}")

    log_action("verify_integrations", {"complete": complete, "partial": partial, "missing": missing})
    return 0 if missing == 0 else 1

# =============================================================================
# MONITOR COMMANDS
# =============================================================================

def cmd_monitor_health(args):
    """Run health checks (replaces monitor_system.py)"""
    print(f"{C.BLUE}🏥 AUTOFIX: Health Monitor{C.RESET}")
    print("=" * 60)

    checks = {
        "docker": check_docker(),
        "databases": check_databases(),
        "disk": check_disk(),
        "services": check_services(),
    }

    healthy = sum(1 for v in checks.values() if v["status"] == "healthy")
    total = len(checks)

    print()
    for name, result in checks.items():
        status_icon = "✅" if result["status"] == "healthy" else "❌"
        color = C.GREEN if result["status"] == "healthy" else C.RED
        print(f"  {status_icon} {color}{name}: {result['message']}{C.RESET}")

    print()
    print(f"  Overall: {healthy}/{total} checks passed")

    log_action("monitor_health", checks)
    return 0 if healthy == total else 1

def check_docker() -> Dict:
    """Check Docker containers"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=10
        )
        containers = [c for c in result.stdout.strip().split('\n') if c]
        return {"status": "healthy", "message": f"{len(containers)} containers running"}
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}

def check_databases() -> Dict:
    """Check database connectivity"""
    online = 0
    for db in DATABASES:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", "localhost", "-p", str(db["port"])],
                capture_output=True, timeout=5
            )
            if result.returncode == 0:
                online += 1
        except:
            pass

    if online == len(DATABASES):
        return {"status": "healthy", "message": f"{online}/{len(DATABASES)} databases online"}
    else:
        return {"status": "unhealthy", "message": f"{online}/{len(DATABASES)} databases online"}

def check_disk() -> Dict:
    """Check disk space"""
    try:
        total, used, free = shutil.disk_usage("/home/rasmus")
        percent = used / total * 100
        free_gb = free / (1024**3)
        if percent < 80:
            return {"status": "healthy", "message": f"{free_gb:.1f} GB free ({percent:.0f}% used)"}
        else:
            return {"status": "unhealthy", "message": f"Only {free_gb:.1f} GB free ({percent:.0f}% used)"}
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}

def check_services() -> Dict:
    """Check systemd services"""
    services_to_check = [
        "cirkelline-backend",
        "cirkelline-frontend",
        "cosmic-library",
        "admiral-hq",
    ]
    running = 0
    for svc in services_to_check:
        try:
            result = subprocess.run(
                ["systemctl", "--user", "is-active", svc],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip() == "active":
                running += 1
        except:
            pass

    return {"status": "healthy" if running > 0 else "unhealthy",
            "message": f"{running}/{len(services_to_check)} services running"}

# =============================================================================
# STATUS COMMAND
# =============================================================================

def cmd_status(args):
    """Show overall system status"""
    print(f"{C.BLUE}📊 AUTOFIX: System Status{C.RESET}")
    print("=" * 60)

    # Log files
    log_count = len(list(LOGS_DIR.glob("*.log"))) if LOGS_DIR.exists() else 0
    print(f"  📁 Log files: {log_count}")

    # Backups
    backup_count = len(list(BACKUPS_DIR.glob("*.sql.gz"))) if BACKUPS_DIR.exists() else 0
    print(f"  💾 Database backups: {backup_count}")

    # Projects
    projects_found = sum(1 for p in PROJECTS if (PROJECTS_ROOT / p).exists())
    print(f"  📦 Projects found: {projects_found}/{len(PROJECTS)}")

    # Databases
    dbs_online = 0
    for db in DATABASES:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", "localhost", "-p", str(db["port"])],
                capture_output=True, timeout=5
            )
            if result.returncode == 0:
                dbs_online += 1
        except:
            pass
    print(f"  🗄️  Databases online: {dbs_online}/{len(DATABASES)}")

    # Last action
    action_log = LOGS_DIR / "autofix_actions.jsonl"
    if action_log.exists():
        lines = action_log.read_text().strip().split('\n')
        if lines:
            last = json.loads(lines[-1])
            print(f"  ⏰ Last action: {last['action']} at {last['timestamp'][:19]}")

    return 0

# =============================================================================
# LOGGING
# =============================================================================

def log_action(action: str, data: Dict):
    """Log action to JSONL file"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / "autofix_actions.jsonl"

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "data": data
    }

    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="AUTOFIX - Unified System Maintenance CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python autofix.py logs --cleanup              # Cleanup old logs
  python autofix.py db --backup                 # Backup all databases
  python autofix.py db --list                   # List databases
  python autofix.py deploy --system             # Deploy integration
  python autofix.py verify --integrations       # Verify integrations
  python autofix.py monitor --health            # Health checks
  python autofix.py status                      # System status
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # logs command
    logs_parser = subparsers.add_parser("logs", help="Log management")
    logs_parser.add_argument("--cleanup", action="store_true", help="Cleanup old logs")

    # db command
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_parser.add_argument("--backup", action="store_true", help="Backup all databases")
    db_parser.add_argument("--list", action="store_true", help="List databases")
    db_parser.add_argument("--retention", type=int, default=7, help="Backup retention days")

    # deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deployment operations")
    deploy_parser.add_argument("--system", action="store_true", help="Deploy integration system")

    # verify command
    verify_parser = subparsers.add_parser("verify", help="Verification operations")
    verify_parser.add_argument("--integrations", action="store_true", help="Verify integrations")

    # monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Monitoring operations")
    monitor_parser.add_argument("--health", action="store_true", help="Run health checks")

    # status command
    subparsers.add_parser("status", help="Show system status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to command
    if args.command == "logs" and args.cleanup:
        return cmd_logs_cleanup(args)
    elif args.command == "db":
        if args.backup:
            return cmd_db_backup(args)
        elif args.list:
            return cmd_db_list(args)
        else:
            db_parser.print_help()
            return 1
    elif args.command == "deploy" and args.system:
        return cmd_deploy_system(args)
    elif args.command == "verify" and args.integrations:
        return cmd_verify_integrations(args)
    elif args.command == "monitor" and args.health:
        return cmd_monitor_health(args)
    elif args.command == "status":
        return cmd_status(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
