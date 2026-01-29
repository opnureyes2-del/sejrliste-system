#!/usr/bin/env python3
"""
Model Router — Intelligent Model Routing for Cirkelline
=========================================================
Vælger den rigtige AI model baseret på opgavetype.

Brug:
    python3 scripts/model_router.py "Forklar hvad denne funktion gør"
    python3 scripts/model_router.py --classify "Skriv en login komponent"
    python3 scripts/model_router.py --test   # Test alle routes
    python3 scripts/model_router.py --local "Hvad er en variabel?"  # Kør lokalt

Regler fra 01_DECISION_MATRIX.md:
    - Opus  → Arkitektur, planlægning, komplekse beslutninger, pattern analyse
    - Sonnet → Kode skrivning, refactoring, fil-redigering, git
    - Haiku  → Verifikation, simple checks, logging
    - Ollama → Forklaringer, outlines, brainstorm, simpel formatting (GRATIS)
"""

import sys

# ============================================================
# MODEL ROUTING TABLE
# Fra: HOW TO USE A CLAUDE OPUS/01_DECISION_MATRIX.md
# ============================================================

ROUTES = {
    "opus": {
        "keywords": [
            "arkitektur", "architecture", "design", "planlæg", "plan",
            "strategi", "strategy", "beslut", "decision", "analysér",
            "analyze", "pattern", "mønster", "complex", "kompleks",
            "predict", "forudsig", "optimer", "optimize", "research",
            "alternativ", "sammenlign", "compare", "evaluate", "evaluér",
            "phase 0", "phase 1", "dna lag 4", "dna lag 6", "dna lag 7",
            "self-improving", "self-optimizing", "predictive",
        ],
        "model_id": "claude-opus-4-5-20251101",
        "cost": "$$$",
        "description": "Arkitektur, strategi, patterns, komplekse beslutninger",
        "token_budget": 4000,
    },
    "sonnet": {
        "keywords": [
            "skriv kode", "write code", "implement", "implementér",
            "refactor", "redigér", "edit", "byg", "build", "opret",
            "create", "fix", "fiks", "commit", "push", "git",
            "component", "komponent", "funktion", "function", "class",
            "klasse", "modul", "module", "migration",
            "phase 2", "phase 4", "dna lag 5", "self-archiving",
            "review", "bug", "fejl", "ændring", "change", "update",
            "opdater", "tilføj", "add", "slet", "delete", "remove",
        ],
        "model_id": "claude-sonnet-4-20250514",
        "cost": "$$",
        "description": "Kode skrivning, refactoring, git workflow",
        "token_budget": 3000,
    },
    "haiku": {
        "keywords": [
            "verificér", "verify", "check", "tjek", "status",
            "format", "lint", "test result", "test", "log", "simple",
            "simpel", "ja/nej", "yes/no", "count", "tæl",
            "list", "find", "søg inden i", "short",
            "phase 3", "dna lag 2", "dna lag 3",
            "self-documenting", "self-verifying",
        ],
        "model_id": "claude-haiku",
        "cost": "$",
        "description": "Verifikation, checks, logging, simple spørgsmål",
        "token_budget": 1000,
    },
    "ollama": {
        "keywords": [
            "forklar", "explain", "hvad er", "what is", "outline",
            "brainstorm", "idé", "idea", "simpel", "basic",
            "begynder", "beginner", "tutorial", "eksempel",
            "example", "vis mig", "show me", "definer", "define",
            "summary", "opsummér", "oversæt", "translate",
            "formatting", "formatér",
        ],
        "model_id": "ollama/llama3.2",
        "cost": "GRATIS",
        "description": "Forklaringer, brainstorm, simple spørgsmål (GRATIS)",
        "token_budget": 0,  # Gratis
    },
}

# DNA Lag → Model mapping
DNA_MODEL_MAP = {
    1: None,        # SELF-AWARE: Passiv metadata
    2: "haiku",     # SELF-DOCUMENTING: Auto-log
    3: "haiku",     # SELF-VERIFYING: Checks
    4: "opus",      # SELF-IMPROVING: Pattern analyse
    5: "sonnet",    # SELF-ARCHIVING: Konklusion
    6: "opus",      # PREDICTIVE: Forudsigelser
    7: "opus",      # SELF-OPTIMIZING: Research
}

# Sejr Phase → Model mapping
PHASE_MODEL_MAP = {
    0: "opus",      # Optimization: 3 alternativer
    1: "opus",      # Planning: Arkitektur
    2: "sonnet",    # Development: Kode
    3: "haiku",     # Verification: Tests
    4: "sonnet",    # Git: Commits
}


def classify_task(task_description: str) -> dict:
    """Klassificér en opgave og find den rigtige model."""
    task_lower = task_description.lower()

    scores = {}
    for model_name, config in ROUTES.items():
        score = 0
        matched_keywords = []
        for keyword in config["keywords"]:
            if keyword in task_lower:
                score += 1
                matched_keywords.append(keyword)
        scores[model_name] = {
            "score": score,
            "matched": matched_keywords,
        }

    # Find bedste match
    best_model = max(scores, key=lambda k: scores[k]["score"])

    # Hvis ingen keywords matchede, default til sonnet (god all-rounder)
    if scores[best_model]["score"] == 0:
        best_model = "sonnet"

    config = ROUTES[best_model]
    return {
        "model": best_model,
        "model_id": config["model_id"],
        "cost": config["cost"],
        "description": config["description"],
        "token_budget": config["token_budget"],
        "confidence": min(scores[best_model]["score"] / 3, 1.0),
        "matched_keywords": scores[best_model]["matched"],
        "all_scores": {k: v["score"] for k, v in scores.items()},
    }


def run_local(prompt: str) -> str:
    """Kør en opgave med Ollama (lokal, gratis)."""
    try:
        import ollama
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except ImportError:
        return "❌ ollama Python pakke ikke installeret. Kør: pip install ollama"
    except Exception as e:
        return f"❌ Ollama fejl: {e}"


def test_routing():
    """Test model routing med eksempler."""
    test_cases = [
        ("Forklar hvad en variabel er", "ollama"),
        ("Design arkitekturen for login systemet", "opus"),
        ("Skriv kode til en login komponent", "sonnet"),
        ("Verificér at alle tests passerer", "haiku"),
        ("Hvad er de 3 bedste alternativer til dette?", "opus"),
        ("Commit og push til git", "sonnet"),
        ("Tjek status på deployment", "haiku"),
        ("Brainstorm idéer til UI design", "ollama"),
        ("Analysér patterns i fejl-log", "opus"),
        ("Refactor denne funktion", "sonnet"),
        ("Hvad er LINEN Framework?", "ollama"),
        ("Format denne markdown fil", "haiku"),
    ]

    print("🧪 Model Routing Test")
    print("=" * 70)

    correct = 0
    for task, expected in test_cases:
        result = classify_task(task)
        actual = result["model"]
        match = "✅" if actual == expected else "❌"
        if actual == expected:
            correct += 1
        print(f"  {match} \"{task}\"")
        print(f"      → {actual} (forventet: {expected}) | {result['cost']} | Keywords: {result['matched_keywords']}")
        print()

    print(f"Score: {correct}/{len(test_cases)} ({correct/len(test_cases)*100:.0f}%)")
    return correct / len(test_cases)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    if sys.argv[1] == "--test":
        test_routing()
    elif sys.argv[1] == "--classify":
        task = " ".join(sys.argv[2:])
        result = classify_task(task)
        print(f"\n📋 Opgave: \"{task}\"")
        print(f"🤖 Model: {result['model']} ({result['model_id']})")
        print(f"💰 Pris: {result['cost']}")
        print(f"📊 Confidence: {result['confidence']:.0%}")
        print(f"🔑 Keywords: {result['matched_keywords']}")
        print(f"📏 Token budget: {result['token_budget']}")
        print(f"\n📈 Alle scores: {result['all_scores']}")
    elif sys.argv[1] == "--local":
        prompt = " ".join(sys.argv[2:])
        print(f"🦙 Ollama (llama3.2): \"{prompt}\"")
        print("-" * 40)
        print(run_local(prompt))
    else:
        task = " ".join(sys.argv[1:])
        result = classify_task(task)
        print(f"🤖 {result['model']} ({result['cost']}) → \"{task}\"")
        if result['model'] == 'ollama':
            print("\n🦙 Kører lokalt (GRATIS)...")
            print("-" * 40)
            print(run_local(task))


if __name__ == "__main__":
    main()
