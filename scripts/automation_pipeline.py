#!/usr/bin/env python3
"""
Automation Pipeline — AI-Assisteret Development Pipeline
==========================================================
Kører kvalitets-pipeline på Python-filer: syntax → linting → security → rapport.

Brug:
    python3 scripts/automation_pipeline.py <fil.py>                # Fuld pipeline
    python3 scripts/automation_pipeline.py <fil.py> --quick        # Kun syntax + lint
    python3 scripts/automation_pipeline.py <fil.py> --with-ollama  # + Ollama code review

Fra: HOW TO USE A CLAUDE OPUS/06_AUTOMATION_PIPELINE.md
Tilpasset til lokalt system (ingen Docker, ingen API keys nødvendige).
"""

import subprocess
import sys
import os
import json
from datetime import datetime

# Farver for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def run_step(name, cmd, cwd=None):
    """Kør et pipeline step og returnér resultat."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}Step: {name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=60, cwd=cwd
        )

        if result.returncode == 0:
            print(f"{GREEN}✅ {name}: PASSED{RESET}")
            if result.stdout.strip():
                print(result.stdout[:500])
            return {"status": "pass", "output": result.stdout, "errors": 0}
        else:
            output = result.stdout + result.stderr
            error_count = output.count('\n')
            print(f"{YELLOW}⚠️  {name}: {error_count} issues{RESET}")
            if output.strip():
                # Show first 20 lines
                lines = output.strip().split('\n')
                for line in lines[:20]:
                    print(f"  {line}")
                if len(lines) > 20:
                    print(f"  ... og {len(lines) - 20} mere")
            return {"status": "warn", "output": output, "errors": error_count}
    except subprocess.TimeoutExpired:
        print(f"{RED}❌ {name}: TIMEOUT (60s){RESET}")
        return {"status": "timeout", "output": "", "errors": 1}
    except Exception as e:
        print(f"{RED}❌ {name}: ERROR - {e}{RESET}")
        return {"status": "error", "output": str(e), "errors": 1}


def run_ollama_review(filepath):
    """Kør Ollama code review (gratis, lokalt)."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}Step: Ollama Code Review (GRATIS){RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    try:
        import ollama

        # Læs filen (max 200 linjer for at spare tokens)
        with open(filepath, 'r') as f:
            code_lines = f.readlines()

        if len(code_lines) > 200:
            code = ''.join(code_lines[:200])
            code += f"\n# ... ({len(code_lines) - 200} more lines)"
        else:
            code = ''.join(code_lines)

        response = ollama.chat(
            model="codellama",
            messages=[{
                "role": "user",
                "content": f"Review this Python code. List the 3 most important improvements:\n\n```python\n{code}\n```"
            }]
        )
        review = response['message']['content']
        print(f"{GREEN}🦙 Code Review:{RESET}")
        print(review[:1000])
        return {"status": "pass", "output": review, "errors": 0}

    except ImportError:
        print(f"{YELLOW}⚠️  ollama ikke installeret (pip install ollama){RESET}")
        return {"status": "skip", "output": "ollama not installed", "errors": 0}
    except Exception as e:
        print(f"{YELLOW}⚠️  Ollama ikke tilgængelig: {e}{RESET}")
        return {"status": "skip", "output": str(e), "errors": 0}


def count_issues(results):
    """Tæl totale issues."""
    total = 0
    for step, result in results.items():
        if result["status"] in ("warn", "error", "timeout"):
            total += result["errors"]
    return total


def generate_report(filepath, results, duration):
    """Generér pipeline rapport."""
    filename = os.path.basename(filepath)
    total_issues = count_issues(results)
    passed = sum(1 for r in results.values() if r["status"] == "pass")
    total = len(results)

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}📊 PIPELINE RAPPORT: {filename}{RESET}")
    print(f"{'='*60}")
    print(f"📅 Dato: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"⏱️  Varighed: {duration:.1f}s")
    print(f"📋 Steps: {passed}/{total} passed")
    print(f"⚠️  Issues: {total_issues}")
    print()

    for step, result in results.items():
        status_icon = {
            "pass": f"{GREEN}✅",
            "warn": f"{YELLOW}⚠️ ",
            "error": f"{RED}❌",
            "timeout": f"{RED}⏰",
            "skip": f"{BLUE}⏭️ ",
        }.get(result["status"], "❓")
        print(f"  {status_icon} {step}: {result['status'].upper()}{RESET}"
              + (f" ({result['errors']} issues)" if result['errors'] > 0 else ""))

    # Kvalitets-score
    if total > 0:
        score = (passed / total) * 10
        print(f"\n📈 Kvalitets-score: {score:.1f}/10")

        if score >= 8:
            print(f"{GREEN}🏆 KVALITET: GOD — klar til commit{RESET}")
        elif score >= 5:
            print(f"{YELLOW}🔧 KVALITET: OK — fix issues før commit{RESET}")
        else:
            print(f"{RED}🚨 KVALITET: LAV — kræver arbejde{RESET}")

    print(f"\n{'='*60}")
    return total_issues


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    filepath = sys.argv[1]
    quick_mode = "--quick" in sys.argv
    with_ollama = "--with-ollama" in sys.argv

    if not os.path.isfile(filepath):
        print(f"❌ Fil ikke fundet: {filepath}")
        return

    if not filepath.endswith('.py'):
        print(f"⚠️  Ikke en Python fil: {filepath}")
        return

    print(f"{BOLD}🚀 AUTOMATION PIPELINE — {os.path.basename(filepath)}{RESET}")
    print(f"Mode: {'Quick' if quick_mode else 'Full'}"
          + (" + Ollama" if with_ollama else ""))
    print(f"Fil: {filepath}")

    start_time = datetime.now()
    results = {}

    # Step 1: Syntax check (ALTID)
    results["Syntax Check"] = run_step(
        "Syntax Check",
        f"python3 -m py_compile '{filepath}'"
    )

    # Step 2: Linting (ALTID)
    results["Flake8 Linting"] = run_step(
        "Flake8 Linting",
        f"flake8 --count --statistics '{filepath}'"
    )

    if not quick_mode:
        # Step 3: Security scan
        results["Bandit Security"] = run_step(
            "Bandit Security Scan",
            f"bandit -r '{filepath}' -ll"  # Kun Medium+ severity
        )

        # Step 4: Line count + complexity
        results["Code Metrics"] = run_step(
            "Code Metrics",
            f"wc -l '{filepath}' && echo '---' && "
            f"python3 -c \"import ast; tree = ast.parse(open('{filepath}').read()); "
            f"funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]; "
            f"classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]; "
            f"print(f'Functions: {{len(funcs)}}'); print(f'Classes: {{len(classes)}}')\""
        )

    # Step 5: Ollama code review (valgfrit)
    if with_ollama:
        results["Ollama Review"] = run_ollama_review(filepath)

    # Rapport
    duration = (datetime.now() - start_time).total_seconds()
    total_issues = generate_report(filepath, results, duration)

    return total_issues


if __name__ == "__main__":
    issues = main()
    if issues and issues > 0:
        sys.exit(1)
