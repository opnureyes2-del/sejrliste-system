#!/usr/bin/env python3
"""
AI Assistant — Intelligent Task Router for Cirkelline Systemet
===============================================================
Samler model_router, hybrid_generate, token_tools og automation_pipeline
i en samlet AIAssistant klasse der auto-router opgaver.

Brug:
    python3 scripts/ai_assistant.py "Skriv en login funktion"
    python3 scripts/ai_assistant.py --status
    python3 scripts/ai_assistant.py --pipeline scripts/model_router.py
    python3 scripts/ai_assistant.py --route "Design arkitekturen"
    python3 scripts/ai_assistant.py --budget

Fra: Claude Usage Mastery SEJR LISTE, Pass 3 Fase 1
"""

import sys
import os
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict

# Import eksisterende tools
sys.path.insert(0, os.path.dirname(__file__))
from model_router import classify_task, run_local, ROUTES, DNA_MODEL_MAP, PHASE_MODEL_MAP
from token_tools import count_tokens, estimate_cost, count_file_tokens, PRICES
from hybrid_generate import hybrid_generate, show_stats as hybrid_stats


# ============================================================
# DNA LAG TOKEN BUDGETS
# ============================================================

# Token budget per DNA lag (dagligt estimat)
DNA_TOKEN_BUDGETS = {
    1: {"name": "SELF-AWARE", "model": None, "daily_budget": 0,
        "description": "Passiv metadata — ingen AI kald"},
    2: {"name": "SELF-DOCUMENTING", "model": "haiku", "daily_budget": 5000,
        "description": "Auto-log, journal, session notes"},
    3: {"name": "SELF-VERIFYING", "model": "haiku", "daily_budget": 10000,
        "description": "Compliance checks, verification, tests"},
    4: {"name": "SELF-IMPROVING", "model": "opus", "daily_budget": 20000,
        "description": "Pattern analyse, optimering, research"},
    5: {"name": "SELF-ARCHIVING", "model": "sonnet", "daily_budget": 15000,
        "description": "Konklusion, sejrliste review, arkivering"},
    6: {"name": "PREDICTIVE", "model": "opus", "daily_budget": 10000,
        "description": "Forudsigelser, risk analyse, predictions"},
    7: {"name": "SELF-OPTIMIZING", "model": "opus", "daily_budget": 25000,
        "description": "Research, alternative analyse, meta-optimering"},
}


# ============================================================
# AI ASSISTANT KLASSE
# ============================================================

@dataclass
class TaskResult:
    """Resultat af en AI Assistant opgave."""
    task: str
    model: str
    model_id: str
    dna_lag: int | None
    phase: int | None
    tokens_used: int
    cost_usd: float
    output: str
    method: str  # "local", "hybrid", "routed"
    timestamp: str


class AIAssistant:
    """
    Intelligent AI Assistant der auto-router opgaver til den rigtige model.

    Integrerer:
    - Model routing (classify_task)
    - Hybrid generation (lokal draft -> Claude finish)
    - Token budgets per DNA lag
    - Quality pipeline integration
    - Sejrliste system integration
    """

    def __init__(self):
        self.session_log: list[TaskResult] = []
        self.usage_file = os.path.expanduser("~/.project_cache/ai_usage.json")
        self._load_usage()

    def _load_usage(self):
        """Load dagligt forbrug."""
        self.usage = {"date": "", "by_model": {}, "by_dna_lag": {}, "total_cost": 0.0}
        if os.path.isfile(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    self.usage = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        # Reset dagligt
        today = datetime.now().strftime("%Y-%m-%d")
        if self.usage.get("date") != today:
            self.usage = {
                "date": today,
                "by_model": {},
                "by_dna_lag": {},
                "total_cost": 0.0,
            }

    def _save_usage(self):
        """Gem dagligt forbrug."""
        os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f, indent=2, ensure_ascii=False)

    def _track_usage(self, model: str, tokens: int, cost: float,
                     dna_lag: int | None = None):
        """Track token forbrug."""
        # By model
        if model not in self.usage["by_model"]:
            self.usage["by_model"][model] = {"tokens": 0, "cost": 0.0, "calls": 0}
        self.usage["by_model"][model]["tokens"] += tokens
        self.usage["by_model"][model]["cost"] += cost
        self.usage["by_model"][model]["calls"] += 1

        # By DNA lag
        if dna_lag is not None:
            lag_key = str(dna_lag)
            if lag_key not in self.usage["by_dna_lag"]:
                self.usage["by_dna_lag"][lag_key] = {"tokens": 0, "cost": 0.0}
            self.usage["by_dna_lag"][lag_key]["tokens"] += tokens
            self.usage["by_dna_lag"][lag_key]["cost"] += cost

        self.usage["total_cost"] += cost
        self._save_usage()

    def route(self, task: str) -> dict:
        """Klassificer og rout en opgave."""
        classification = classify_task(task)
        return {
            "task": task[:100],
            "model": classification["model"],
            "model_id": classification["model_id"],
            "cost_tier": classification["cost"],
            "confidence": classification["confidence"],
            "keywords": classification["matched_keywords"],
            "token_budget": classification["token_budget"],
            "description": classification["description"],
        }

    def execute(self, task: str, dna_lag: int | None = None,
                phase: int | None = None,
                force_local: bool = False) -> TaskResult:
        """
        Eksekver en opgave med auto-routing.

        Args:
            task: Opgavebeskrivelse
            dna_lag: Specifikt DNA lag (1-7), None for auto-detect
            phase: Sejr phase (0-4), None for auto-detect
            force_local: Tving Ollama (gratis)
        """
        classification = classify_task(task)
        model = classification["model"]

        # Override med DNA lag eller phase model
        if dna_lag and dna_lag in DNA_MODEL_MAP:
            override = DNA_MODEL_MAP[dna_lag]
            if override:
                model = override
        elif phase is not None and phase in PHASE_MODEL_MAP:
            model = PHASE_MODEL_MAP[phase]

        if force_local:
            model = "ollama"

        # Eksekver baseret paa model
        if model == "ollama":
            # Koenr lokalt
            output = run_local(task)
            tokens = count_tokens(output)
            cost = 0.0
            method = "local"
        else:
            # Hybrid: draft lokalt, estimer Claude cost
            result = hybrid_generate(task, draft_only=True)
            output = result["draft"]
            tokens = result["draft_tokens"]
            cost = result["cost_saved_usd"]  # Hvad vi sparede
            method = "hybrid"

        # Track
        self._track_usage(model, tokens, cost, dna_lag)

        task_result = TaskResult(
            task=task[:200],
            model=model,
            model_id=ROUTES[model]["model_id"],
            dna_lag=dna_lag,
            phase=phase,
            tokens_used=tokens,
            cost_usd=cost,
            output=output,
            method=method,
            timestamp=datetime.now(timezone.utc).astimezone().isoformat(),
        )
        self.session_log.append(task_result)
        return task_result

    def run_pipeline(self, filepath: str, quick: bool = False) -> dict:
        """Koer quality pipeline paa en fil."""
        cmd = f"python3 scripts/automation_pipeline.py '{filepath}'"
        if quick:
            cmd += " --quick"

        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,  # nosec B602
                timeout=120,
                cwd=os.path.dirname(os.path.dirname(__file__))
            )
            return {
                "file": filepath,
                "exit_code": result.returncode,
                "output": result.stdout[-2000:] if result.stdout else "",
                "errors": result.stderr[-500:] if result.stderr else "",
            }
        except subprocess.TimeoutExpired:
            return {"file": filepath, "exit_code": -1,
                    "output": "TIMEOUT", "errors": "Pipeline timeout 120s"}

    def budget_status(self) -> dict:
        """Vis token budget status per DNA lag."""
        status = {}
        for lag, config in DNA_TOKEN_BUDGETS.items():
            lag_key = str(lag)
            used = self.usage.get("by_dna_lag", {}).get(lag_key, {})
            tokens_used = used.get("tokens", 0)
            budget = config["daily_budget"]
            remaining = budget - tokens_used
            pct_used = (tokens_used / budget * 100) if budget > 0 else 0

            status[lag] = {
                "name": config["name"],
                "model": config["model"] or "none",
                "budget": budget,
                "used": tokens_used,
                "remaining": max(0, remaining),
                "pct_used": round(pct_used, 1),
                "over_budget": tokens_used > budget,
            }
        return status

    def session_summary(self) -> dict:
        """Vis session sammendrag."""
        total_tokens = sum(r.tokens_used for r in self.session_log)
        total_cost = sum(r.cost_usd for r in self.session_log)
        models_used = {}
        for r in self.session_log:
            if r.model not in models_used:
                models_used[r.model] = 0
            models_used[r.model] += 1

        return {
            "tasks_completed": len(self.session_log),
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost,
            "models_used": models_used,
        }


# ============================================================
# CLI
# ============================================================

def print_route(routing: dict):
    """Print routing resultat."""
    print("=" * 60)
    print("AI ASSISTANT — TASK ROUTING")
    print("=" * 60)
    print(f"  Opgave:      {routing['task']}")
    print(f"  Model:       {routing['model']} ({routing['model_id']})")
    print(f"  Pris:        {routing['cost_tier']}")
    print(f"  Confidence:  {routing['confidence']:.0%}")
    print(f"  Keywords:    {routing['keywords']}")
    print(f"  Budget:      {routing['token_budget']} tokens")
    print(f"  Beskrivelse: {routing['description']}")
    print("=" * 60)


def print_budget(assistant: AIAssistant):
    """Print budget status."""
    status = assistant.budget_status()
    print("=" * 60)
    print("DNA LAG TOKEN BUDGET STATUS")
    print(f"Dato: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    print(f"{'Lag':<5} {'Navn':<20} {'Model':<8} "
          f"{'Budget':>8} {'Brugt':>8} {'Rest':>8} {'%':>6}")
    print("-" * 65)

    total_budget = 0
    total_used = 0

    for lag in sorted(status.keys()):
        s = status[lag]
        flag = " [!]" if s["over_budget"] else ""
        print(f"  {lag:<3} {s['name']:<20} {s['model']:<8} "
              f"{s['budget']:>8,} {s['used']:>8,} {s['remaining']:>8,} "
              f"{s['pct_used']:>5.1f}%{flag}")
        total_budget += s["budget"]
        total_used += s["used"]

    print("-" * 65)
    remaining = total_budget - total_used
    pct = (total_used / total_budget * 100) if total_budget > 0 else 0
    print(f"  {'':3} {'TOTAL':<20} {'':8} "
          f"{total_budget:>8,} {total_used:>8,} {max(0, remaining):>8,} "
          f"{pct:>5.1f}%")
    print("=" * 60)

    # Daily cost
    print(f"\n  Daglig cost:  ${assistant.usage.get('total_cost', 0):.4f}")
    by_model = assistant.usage.get("by_model", {})
    for model_name, model_data in by_model.items():
        print(f"    {model_name}: {model_data['calls']} kald, "
              f"{model_data['tokens']:,} tokens, "
              f"${model_data['cost']:.4f}")


def print_status(assistant: AIAssistant):
    """Print fuld status."""
    print("=" * 60)
    print("AI ASSISTANT STATUS")
    print("=" * 60)

    # Session
    summary = assistant.session_summary()
    print(f"\n--- Session ---")
    print(f"  Opgaver:  {summary['tasks_completed']}")
    print(f"  Tokens:   {summary['total_tokens']:,}")
    print(f"  Cost:     ${summary['total_cost_usd']:.4f}")
    print(f"  Models:   {summary['models_used']}")

    # Budget
    print()
    print_budget(assistant)

    # Hybrid stats
    print()
    hybrid_stats()


def main():
    assistant = AIAssistant()

    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "--status":
        print_status(assistant)

    elif cmd == "--budget":
        print_budget(assistant)

    elif cmd == "--route":
        task = " ".join(sys.argv[2:])
        routing = assistant.route(task)
        print_route(routing)

    elif cmd == "--pipeline":
        filepath = sys.argv[2] if len(sys.argv) > 2 else ""
        if not filepath or not os.path.isfile(filepath):
            print(f"[FAIL] Fil ikke fundet: {filepath}")
            return
        quick = "--quick" in sys.argv
        result = assistant.run_pipeline(filepath, quick=quick)
        print(result["output"])

    elif cmd == "--local":
        task = " ".join(sys.argv[2:])
        result = assistant.execute(task, force_local=True)
        print(f"\n[{result.model.upper()}] ({result.tokens_used} tokens, "
              f"${result.cost_usd:.4f}):")
        print("-" * 40)
        print(result.output)

    else:
        # Auto-execute
        task = " ".join(sys.argv[1:])
        result = assistant.execute(task)
        print(f"\n[{result.model.upper()}] {result.method} "
              f"({result.tokens_used} tokens, ${result.cost_usd:.4f}):")
        print("-" * 40)
        print(result.output)
        print()
        print(f"  Model: {result.model} ({result.model_id})")
        print(f"  Method: {result.method}")
        if result.dna_lag:
            print(f"  DNA Lag: {result.dna_lag}")


if __name__ == "__main__":
    main()
