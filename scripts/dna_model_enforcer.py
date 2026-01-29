#!/usr/bin/env python3
"""
DNA Model Enforcer — Sikrer alle 7 DNA lag bruger korrekt model
================================================================
Verificerer at model routing matcher DNA lag specifikationer.
Opdaterer knowledge base automatisk og sikrer quality gates.

Brug:
    python3 scripts/dna_model_enforcer.py              # Fuld check
    python3 scripts/dna_model_enforcer.py --verify     # Kun verifikation
    python3 scripts/dna_model_enforcer.py --update-kb  # Opdater knowledge base
    python3 scripts/dna_model_enforcer.py --report     # Generer rapport

Fra: Claude Usage Mastery SEJR LISTE, Pass 3 Fase 2
"""

import sys
import os
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Import tools
sys.path.insert(0, os.path.dirname(__file__))
from model_router import classify_task, DNA_MODEL_MAP, ROUTES
from token_tools import count_tokens
from ai_assistant import AIAssistant, DNA_TOKEN_BUDGETS


# ============================================================
# DNA LAG VERIFICATION
# ============================================================

# Forventede opgaver per DNA lag — bruges til verifikation
DNA_LAG_TASKS = {
    1: {
        "name": "SELF-AWARE",
        "expected_model": None,
        "test_tasks": [
            # Lag 1 er passiv metadata — ingen AI kald
        ],
        "description": "Passiv: timestamps, versions, state tracking",
    },
    2: {
        "name": "SELF-DOCUMENTING",
        "expected_model": "haiku",
        "test_tasks": [
            "Log denne handling til journal",
            "Dokumenter hvad der lige skete",
            "Opdater session notes",
        ],
        "description": "Auto-dokumentation: journal, session, logs",
    },
    3: {
        "name": "SELF-VERIFYING",
        "expected_model": "haiku",
        "test_tasks": [
            "Verificer at alle filer eksisterer",
            "Tjek status paa deployment",
            "Test om denne funktion virker",
        ],
        "description": "Verifikation: checks, tests, compliance",
    },
    4: {
        "name": "SELF-IMPROVING",
        "expected_model": "opus",
        "test_tasks": [
            "Analyser patterns i fejl-loggen",
            "Design en bedre arkitektur for auth",
            "Optimér denne database query",
        ],
        "description": "Forbedring: patterns, analyse, optimering",
    },
    5: {
        "name": "SELF-ARCHIVING",
        "expected_model": "sonnet",
        "test_tasks": [
            "Skriv konklusion for denne sejrliste",
            "Refactor denne komponent",
            "Implementer arkiverings-funktionen",
        ],
        "description": "Arkivering: konklusion, kode, refactoring",
    },
    6: {
        "name": "PREDICTIVE",
        "expected_model": "opus",
        "test_tasks": [
            "Forudsig hvilke problemer vi faar naeste uge",
            "Evaluér risikoen ved denne arkitektur",
            "Analysér trends i projekt-progress",
        ],
        "description": "Forudsigelse: risk, trends, prediction",
    },
    7: {
        "name": "SELF-OPTIMIZING",
        "expected_model": "opus",
        "test_tasks": [
            "Research de bedste alternativer til Redis",
            "Sammenlign disse 3 frameworks",
            "Evaluér om vi skal skifte database",
        ],
        "description": "Meta-optimering: research, sammenligning, strategi",
    },
}


def verify_dna_routing() -> dict:
    """
    Verificér at model routing matcher DNA lag forventninger.
    Returnerer rapport med pass/fail per lag.
    """
    results = {}
    total_pass = 0
    total_fail = 0
    total_tests = 0

    for lag, config in DNA_LAG_TASKS.items():
        expected = config["expected_model"]
        tests = config["test_tasks"]
        lag_results = {
            "name": config["name"],
            "expected_model": expected or "none",
            "tests": [],
            "pass_count": 0,
            "fail_count": 0,
        }

        if not tests:
            # Lag 1 har ingen tests (passiv)
            lag_results["tests"].append({
                "task": "(passiv — ingen AI kald)",
                "expected": "none",
                "actual": "none",
                "passed": True,
            })
            lag_results["pass_count"] = 1
            total_pass += 1
            total_tests += 1
        else:
            for task in tests:
                classification = classify_task(task)
                actual = classification["model"]
                passed = actual == expected

                lag_results["tests"].append({
                    "task": task,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed,
                    "keywords": classification["matched_keywords"],
                })

                if passed:
                    lag_results["pass_count"] += 1
                    total_pass += 1
                else:
                    lag_results["fail_count"] += 1
                    total_fail += 1
                total_tests += 1

        results[lag] = lag_results

    return {
        "results": results,
        "total_tests": total_tests,
        "total_pass": total_pass,
        "total_fail": total_fail,
        "score_pct": round(total_pass / total_tests * 100, 1) if total_tests > 0 else 0,
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
    }


def update_knowledge_base() -> dict:
    """Opdater ChromaDB knowledge base med nye filer."""
    kb_script = os.path.join(os.path.dirname(__file__), "build_knowledge_base.py")
    if not os.path.isfile(kb_script):
        return {"status": "skip", "reason": "build_knowledge_base.py not found"}

    try:
        result = subprocess.run(
            ["python3", kb_script],
            capture_output=True, text=True, timeout=120,
            cwd=os.path.dirname(os.path.dirname(__file__))
        )
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "output": result.stdout[-1000:] if result.stdout else "",
            "errors": result.stderr[-500:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "reason": "Knowledge base update timeout 120s"}
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def verify_quality_gates() -> dict:
    """Verificér at quality gates koerer ved commit."""
    sejr_dir = os.path.dirname(os.path.dirname(__file__))
    hook_path = os.path.join(sejr_dir, ".git", "hooks", "pre-commit")
    precommit_config = os.path.join(sejr_dir, ".pre-commit-config.yaml")

    checks = {
        "pre_commit_hook": os.path.isfile(hook_path),
        "pre_commit_config": os.path.isfile(precommit_config),
        "hook_executable": os.access(hook_path, os.X_OK) if os.path.isfile(hook_path) else False,
    }

    # Check cron job
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True, text=True, timeout=10
        )
        checks["cron_active"] = "sync_indexes" in result.stdout
        checks["cron_jobs"] = result.stdout.count('\n')
    except Exception:
        checks["cron_active"] = False
        checks["cron_jobs"] = 0

    checks["all_pass"] = all([
        checks["pre_commit_hook"],
        checks["pre_commit_config"],
        checks["hook_executable"],
        checks["cron_active"],
    ])

    return checks


def generate_report(verify_result: dict, kb_result: dict | None,
                    gates_result: dict) -> str:
    """Generer fuld DNA enforcement rapport."""
    lines = []
    lines.append("=" * 70)
    lines.append("DNA MODEL ENFORCEMENT RAPPORT")
    lines.append(f"Dato: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)

    # DNA Routing Verification
    lines.append("\n--- 1. DNA LAG MODEL ROUTING ---\n")
    lines.append(f"Score: {verify_result['total_pass']}/{verify_result['total_tests']} "
                 f"({verify_result['score_pct']}%)\n")

    for lag in sorted(verify_result["results"].keys()):
        r = verify_result["results"][lag]
        status = "[OK]" if r["fail_count"] == 0 else "[FAIL]"
        lines.append(f"  Lag {lag}: {r['name']} ({r['expected_model']}) "
                     f"— {status} ({r['pass_count']}/{r['pass_count'] + r['fail_count']})")
        for test in r["tests"]:
            icon = "[OK]" if test["passed"] else "[FAIL]"
            lines.append(f"    {icon} \"{test['task']}\" → {test['actual']}")
            if not test["passed"]:
                lines.append(f"         Forventet: {test['expected']}, "
                             f"Keywords: {test.get('keywords', [])}")

    # Quality Gates
    lines.append("\n--- 2. QUALITY GATES ---\n")
    for check, value in gates_result.items():
        if check == "all_pass":
            continue
        icon = "[OK]" if value else "[FAIL]"
        lines.append(f"  {icon} {check}: {value}")
    overall = "[OK]" if gates_result["all_pass"] else "[FAIL]"
    lines.append(f"\n  Overall: {overall}")

    # Knowledge Base
    if kb_result:
        lines.append("\n--- 3. KNOWLEDGE BASE ---\n")
        lines.append(f"  Status: {kb_result.get('status', 'unknown')}")
        if kb_result.get("output"):
            for line in kb_result["output"].split('\n')[-5:]:
                if line.strip():
                    lines.append(f"  {line.strip()}")

    # Token Budgets
    lines.append("\n--- 4. TOKEN BUDGETS ---\n")
    assistant = AIAssistant()
    budget_status = assistant.budget_status()
    for lag in sorted(budget_status.keys()):
        s = budget_status[lag]
        flag = " [OVER BUDGET]" if s["over_budget"] else ""
        lines.append(f"  Lag {lag} ({s['name']}): "
                     f"{s['used']:,}/{s['budget']:,} tokens "
                     f"({s['pct_used']:.1f}%){flag}")

    # Summary
    lines.append("\n" + "=" * 70)
    all_ok = (verify_result["total_fail"] == 0
              and gates_result["all_pass"])
    status_text = "ALL CHECKS PASSED" if all_ok else "ISSUES FOUND"
    lines.append(f"STATUS: {status_text}")
    lines.append(f"  Routing: {verify_result['score_pct']}%")
    lines.append(f"  Gates: {'OK' if gates_result['all_pass'] else 'FAIL'}")
    if kb_result:
        lines.append(f"  Knowledge Base: {kb_result.get('status', '?')}")
    lines.append("=" * 70)

    return "\n".join(lines)


# ============================================================
# CLI
# ============================================================

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        result = verify_dna_routing()
        print(f"\nDNA Routing Verification: "
              f"{result['total_pass']}/{result['total_tests']} "
              f"({result['score_pct']}%)\n")
        for lag in sorted(result["results"].keys()):
            r = result["results"][lag]
            status = "[OK]" if r["fail_count"] == 0 else "[FAIL]"
            print(f"  Lag {lag}: {r['name']} — {status}")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--update-kb":
        print("[KB] Opdaterer knowledge base...")
        result = update_knowledge_base()
        print(f"Status: {result['status']}")
        if result.get("output"):
            print(result["output"][-500:])
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        verify = verify_dna_routing()
        gates = verify_quality_gates()
        report = generate_report(verify, None, gates)
        print(report)

        # Gem rapport
        report_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "10_ACTIVE", "CLAUDE_USAGE_MASTERY_2026-01-27",
            "DNA_ENFORCEMENT_REPORT.md"
        )
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\nRapport gemt: {report_path}")
        return

    # Default: fuld check
    print("[1/4] Verificerer DNA lag routing...")
    verify = verify_dna_routing()

    print(f"[2/4] Tjekker quality gates...")
    gates = verify_quality_gates()

    print(f"[3/4] Opdaterer knowledge base...")
    kb = update_knowledge_base()

    print(f"[4/4] Genererer rapport...")
    report = generate_report(verify, kb, gates)
    print(report)

    # Gem rapport
    report_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "10_ACTIVE", "CLAUDE_USAGE_MASTERY_2026-01-27",
        "DNA_ENFORCEMENT_REPORT.md"
    )
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\nRapport gemt: {report_path}")


if __name__ == "__main__":
    main()
