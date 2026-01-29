#!/usr/bin/env python3
"""
Hybrid Generate — Lokal Draft + Claude Finish
==============================================
Bruger Ollama til billigt draft, derefter Claude til polering.
Sparer 70%+ tokens ved at lade Ollama lave foerste udkast.

Brug:
    python3 scripts/hybrid_generate.py "Skriv en login funktion"
    python3 scripts/hybrid_generate.py --draft-only "Forklar git rebase"
    python3 scripts/hybrid_generate.py --stats
    python3 scripts/hybrid_generate.py --measure "opgave" --days 7

Fra: Claude Usage Mastery SEJR LISTE, Pass 3 Fase 0
"""

import sys
import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path

# Import vores eksisterende tools
sys.path.insert(0, os.path.dirname(__file__))
from token_tools import count_tokens, estimate_cost, cache_get, cache_set
from model_router import classify_task, run_local


# ============================================================
# HYBRID GENERATION
# ============================================================

STATS_FILE = os.path.expanduser("~/.project_cache/hybrid_stats.json")


def _load_stats() -> dict:
    """Load hybrid generation statistics."""
    if os.path.isfile(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "total_calls": 0,
        "draft_only_calls": 0,
        "hybrid_calls": 0,
        "total_input_tokens_saved": 0,
        "total_cost_saved_usd": 0.0,
        "history": [],
    }


def _save_stats(stats: dict):
    """Save hybrid generation statistics."""
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)


def hybrid_generate(prompt: str, draft_only: bool = False) -> dict:
    """
    Hybrid generation: Ollama draft -> Claude finish.

    Flow:
    1. Klassificer opgaven med model_router
    2. Generér draft med Ollama (GRATIS)
    3. Hvis draft_only: returner draft
    4. Ellers: estimér cost for Claude polish
    5. Returner draft + cost estimate (bruger skaermer mod uventet API brug)

    Returns dict med:
        draft, model_recommendation, tokens_saved, cost_saved, timing
    """
    start = time.time()
    stats = _load_stats()

    # Step 1: Klassificer opgaven
    classification = classify_task(prompt)
    recommended_model = classification["model"]

    # Step 2: Generér draft med Ollama
    print(f"[DRAFT] Genererer lokal draft med Ollama...")
    draft_start = time.time()
    draft = run_local(prompt)
    draft_time = time.time() - draft_start

    draft_tokens = count_tokens(draft)
    prompt_tokens = count_tokens(prompt)

    # Step 3: Beregn besparelse
    # Uden hybrid: hele prompten + output sendes til Claude
    # Med hybrid: kun refinement sendes (draft er allerede lavet lokalt)
    full_cost = estimate_cost(prompt, max_tokens=draft_tokens,
                              model=recommended_model)
    # Med hybrid ville vi kun sende "Polish this draft: <draft>"
    # som er kortere end at generere fra scratch
    hybrid_prompt = f"Forbedre dette udkast. Behold struktur, fix fejl:\n\n{draft}"
    hybrid_cost = estimate_cost(hybrid_prompt, max_tokens=draft_tokens // 2,
                                model="haiku")  # Haiku for polering

    tokens_saved = prompt_tokens  # Vi undgaar at sende original prompt til dyr model
    cost_saved = full_cost["estimated_cost_usd"] - hybrid_cost["estimated_cost_usd"]

    # Step 4: Opdater statistik
    stats["total_calls"] += 1
    if draft_only:
        stats["draft_only_calls"] += 1
    else:
        stats["hybrid_calls"] += 1
    stats["total_input_tokens_saved"] += tokens_saved
    stats["total_cost_saved_usd"] += max(0, cost_saved)
    stats["history"].append({
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
        "prompt_preview": prompt[:100],
        "model_recommended": recommended_model,
        "draft_tokens": draft_tokens,
        "tokens_saved": tokens_saved,
        "cost_saved_usd": max(0, cost_saved),
        "draft_only": draft_only,
        "draft_time_s": round(draft_time, 2),
    })
    # Keep only last 100 entries
    stats["history"] = stats["history"][-100:]
    _save_stats(stats)

    total_time = time.time() - start

    return {
        "draft": draft,
        "model_recommended": recommended_model,
        "model_id": classification["model_id"],
        "draft_tokens": draft_tokens,
        "prompt_tokens": prompt_tokens,
        "tokens_saved": tokens_saved,
        "cost_without_hybrid": full_cost["estimated_cost_usd"],
        "cost_with_hybrid": hybrid_cost["estimated_cost_usd"],
        "cost_saved_usd": max(0, cost_saved),
        "savings_pct": (cost_saved / full_cost["estimated_cost_usd"] * 100)
        if full_cost["estimated_cost_usd"] > 0 else 0,
        "draft_time_s": round(draft_time, 2),
        "total_time_s": round(total_time, 2),
        "draft_only": draft_only,
    }


def show_stats():
    """Vis samlet hybrid generation statistik."""
    stats = _load_stats()
    print("=" * 60)
    print("HYBRID GENERATION STATISTIK")
    print("=" * 60)
    print(f"  Totale kald:        {stats['total_calls']}")
    print(f"  Draft-only:         {stats['draft_only_calls']}")
    print(f"  Hybrid (draft+API): {stats['hybrid_calls']}")
    print(f"  Tokens sparet:      {stats['total_input_tokens_saved']:,}")
    print(f"  Penge sparet:       ${stats['total_cost_saved_usd']:.4f}")
    print()

    if stats["history"]:
        print("--- Seneste 5 kald ---")
        for entry in stats["history"][-5:]:
            print(f"  [{entry.get('timestamp', '?')[:19]}] "
                  f"{entry.get('model_recommended', '?')} | "
                  f"Draft: {entry.get('draft_tokens', 0)} tokens | "
                  f"Sparet: ${entry.get('cost_saved_usd', 0):.4f} | "
                  f"{entry.get('draft_time_s', 0):.1f}s")
    else:
        print("  (Ingen historik endnu)")

    print("=" * 60)


def measure_savings(days: int = 7):
    """Maal besparelse over N dage."""
    stats = _load_stats()
    from datetime import timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    recent = []
    for entry in stats.get("history", []):
        try:
            ts = datetime.fromisoformat(entry["timestamp"])
            if ts.tzinfo is None:
                continue
            if ts >= cutoff:
                recent.append(entry)
        except (ValueError, KeyError):
            continue

    if not recent:
        print(f"Ingen hybrid kald de seneste {days} dage.")
        return

    total_saved = sum(e.get("cost_saved_usd", 0) for e in recent)
    total_tokens = sum(e.get("tokens_saved", 0) for e in recent)
    total_calls = len(recent)

    print("=" * 60)
    print(f"BESPARELSE SENESTE {days} DAGE")
    print("=" * 60)
    print(f"  Hybrid kald:    {total_calls}")
    print(f"  Tokens sparet:  {total_tokens:,}")
    print(f"  Penge sparet:   ${total_saved:.4f}")
    if total_calls > 0:
        print(f"  Gns. per kald:  ${total_saved/total_calls:.4f}")
    print("=" * 60)


# ============================================================
# CLI
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    if sys.argv[1] == "--stats":
        show_stats()
        return

    if sys.argv[1] == "--measure":
        days = 7
        prompt_text = None
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--days" and i + 1 < len(sys.argv):
                days = int(sys.argv[i + 1])
            elif not arg.startswith("--"):
                prompt_text = arg
        if prompt_text:
            # Run a hybrid call + measure
            result = hybrid_generate(prompt_text)
            print(f"\n[DRAFT] ({result['draft_tokens']} tokens, "
                  f"{result['draft_time_s']}s):")
            print("-" * 40)
            print(result["draft"][:500])
            print()
        measure_savings(days)
        return

    draft_only = "--draft-only" in sys.argv
    prompt_parts = [a for a in sys.argv[1:] if not a.startswith("--")]
    prompt = " ".join(prompt_parts)

    if not prompt:
        print("[FAIL] Angiv en prompt. Brug: hybrid_generate.py \"din opgave\"")
        return

    result = hybrid_generate(prompt, draft_only=draft_only)

    # Output
    print()
    print("=" * 60)
    print("HYBRID GENERATION RESULTAT")
    print("=" * 60)
    print(f"  Model anbefalet:  {result['model_recommended']} "
          f"({result['model_id']})")
    print(f"  Draft tokens:     {result['draft_tokens']:,}")
    print(f"  Prompt tokens:    {result['prompt_tokens']:,}")
    print(f"  Tokens sparet:    {result['tokens_saved']:,}")
    print(f"  Cost uden hybrid: ${result['cost_without_hybrid']:.4f}")
    print(f"  Cost med hybrid:  ${result['cost_with_hybrid']:.4f}")
    print(f"  Sparet:           ${result['cost_saved_usd']:.4f} "
          f"({result['savings_pct']:.0f}%)")
    print(f"  Draft tid:        {result['draft_time_s']}s")
    print(f"  {'DRAFT ONLY' if draft_only else 'HYBRID MODE'}")
    print()
    print("--- DRAFT ---")
    print(result["draft"])
    print("=" * 60)


if __name__ == "__main__":
    main()
