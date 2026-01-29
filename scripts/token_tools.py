#!/usr/bin/env python3
"""
Token Tools — Token Counting, Cost Estimation & Local Caching
================================================================
Praktiske tools til token-bevidst AI brug.

Brug:
    python3 scripts/token_tools.py count "Din tekst her"
    python3 scripts/token_tools.py cost "Din tekst" --model opus --max-tokens 2000
    python3 scripts/token_tools.py count-file masterpiece_en.py
    python3 scripts/token_tools.py cache-stats

Fra: HOW TO USE A CLAUDE OPUS/02_TOKEN_OPTIMIZATION.md
"""

import sys
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

# ============================================================
# TOKEN COUNTING
# ============================================================

def count_tokens(text: str) -> int:
    """Tæl tokens i en tekst med tiktoken."""
    try:
        import tiktoken
        # cl100k_base er encoding for GPT-4/Claude (nærmeste approx)
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except ImportError:
        # Fallback: ca. 4 chars per token
        return len(text) // 4


def count_file_tokens(filepath: str) -> dict:
    """Tæl tokens i en fil."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    tokens = count_tokens(content)
    lines = content.count('\n') + 1
    chars = len(content)

    return {
        "file": os.path.basename(filepath),
        "path": filepath,
        "tokens": tokens,
        "lines": lines,
        "chars": chars,
        "chars_per_token": chars / tokens if tokens > 0 else 0,
    }


# ============================================================
# COST ESTIMATION
# ============================================================

# Priser per million tokens (circa, 2025):
PRICES = {
    "opus": {"input": 15.0, "output": 75.0, "cached_input": 1.5},
    "sonnet": {"input": 3.0, "output": 15.0, "cached_input": 0.3},
    "haiku": {"input": 0.25, "output": 1.25, "cached_input": 0.025},
    "ollama": {"input": 0.0, "output": 0.0, "cached_input": 0.0},
}


def estimate_cost(text: str, max_tokens: int = 1024,
                  model: str = "sonnet", cached: bool = False) -> dict:
    """Estimér pris FØR API kald."""
    input_tokens = count_tokens(text)
    prices = PRICES.get(model, PRICES["sonnet"])

    input_price = prices["cached_input"] if cached else prices["input"]
    cost = (input_tokens * input_price + max_tokens * prices["output"]) / 1_000_000

    return {
        "model": model,
        "input_tokens": input_tokens,
        "max_output_tokens": max_tokens,
        "cached": cached,
        "estimated_cost_usd": cost,
        "savings_if_cached": (
            (input_tokens * (prices["input"] - prices["cached_input"])) / 1_000_000
            if not cached else 0
        ),
    }


# ============================================================
# LOCAL FILE CACHE (ingen Redis nødvendig)
# ============================================================

CACHE_DIR = os.path.expanduser("~/.project_cache")


def _ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def cache_get(key: str) -> str | None:
    """Hent fra lokal fil-cache."""
    _ensure_cache_dir()
    cache_file = os.path.join(CACHE_DIR, hashlib.md5(key.encode(), usedforsecurity=False).hexdigest())
    if os.path.isfile(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
        # Check TTL (1 time default)
        cached_at = datetime.fromisoformat(data.get("cached_at", "2000-01-01"))
        ttl = data.get("ttl", 3600)
        age = (datetime.now() - cached_at).total_seconds()
        if age < ttl:
            return data.get("value")
        else:
            os.remove(cache_file)  # Expired
    return None


def cache_set(key: str, value: str, ttl: int = 3600):
    """Gem i lokal fil-cache."""
    _ensure_cache_dir()
    cache_file = os.path.join(CACHE_DIR, hashlib.md5(key.encode(), usedforsecurity=False).hexdigest())
    data = {
        "key": key[:200],  # Truncated for readability
        "value": value,
        "cached_at": datetime.now().isoformat(),
        "ttl": ttl,
    }
    with open(cache_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def cache_stats() -> dict:
    """Vis cache statistik."""
    _ensure_cache_dir()
    files = list(Path(CACHE_DIR).glob("*"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    return {
        "entries": len(files),
        "total_size_kb": total_size / 1024,
        "cache_dir": CACHE_DIR,
    }


def cached_ollama_call(prompt: str, model: str = "llama3.2",
                       ttl: int = 3600) -> str:
    """Ollama kald med lokal fil-cache. Gentag = GRATIS."""
    cached = cache_get(f"ollama:{model}:{prompt}")
    if cached:
        print("💰 Svar fra cache (0 tokens, 0 API kald)")
        return cached

    try:
        import ollama
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response['message']['content']
        cache_set(f"ollama:{model}:{prompt}", result, ttl)
        return result
    except Exception as e:
        return f"❌ Fejl: {e}"


# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "count":
        if len(sys.argv) < 3:
            print("Brug: python3 token_tools.py count \"din tekst\"")
            print("      python3 token_tools.py count <fil>  (auto-detect)")
            return
        arg = " ".join(sys.argv[2:])
        # Auto-detect: if argument is a file path, read and count file
        if os.path.isfile(arg):
            result = count_file_tokens(arg)
            print(f"📁 Fil: {result['file']}")
            print(f"📊 Tokens: {result['tokens']:,}")
            print(f"📏 Linjer: {result['lines']:,}")
            print(f"📝 Tegn: {result['chars']:,}")
            print(f"📊 Tegn/token: {result['chars_per_token']:.1f}")
            for model in ["opus", "sonnet", "haiku", "ollama"]:
                cost = estimate_cost("x" * result['chars'], 1024, model)
                print(f"  💰 {model}: ${cost['estimated_cost_usd']:.4f}"
                      f" (input: {result['tokens']:,} tokens)")
        else:
            text = arg
            tokens = count_tokens(text)
            print(f"📊 Tekst: \"{text[:80]}{'...' if len(text) > 80 else ''}\"")
            print(f"📊 Tokens: {tokens:,}")
            print(f"📊 Tegn: {len(text):,}")
            print(f"📊 Tegn/token: {len(text)/tokens:.1f}" if tokens > 0 else "")

    elif cmd == "count-file":
        if len(sys.argv) < 3:
            print("Brug: python3 token_tools.py count-file <fil>")
            return
        filepath = sys.argv[2]
        if not os.path.isfile(filepath):
            print(f"❌ Fil ikke fundet: {filepath}")
            return
        result = count_file_tokens(filepath)
        print(f"📁 Fil: {result['file']}")
        print(f"📊 Tokens: {result['tokens']:,}")
        print(f"📏 Linjer: {result['lines']:,}")
        print(f"📝 Tegn: {result['chars']:,}")
        print(f"📊 Tegn/token: {result['chars_per_token']:.1f}")

        # Vis cost for at sende hele filen
        for model in ["opus", "sonnet", "haiku", "ollama"]:
            cost = estimate_cost("x" * result['chars'], 1024, model)
            print(f"  💰 {model}: ${cost['estimated_cost_usd']:.4f}"
                  f" (input: {result['tokens']:,} tokens)")

    elif cmd == "cost":
        text = sys.argv[2] if len(sys.argv) > 2 else "test"
        model = "sonnet"
        max_tokens = 1024
        for i, arg in enumerate(sys.argv[3:]):
            if arg == "--model" and i + 4 < len(sys.argv):
                model = sys.argv[i + 4]
            if arg == "--max-tokens" and i + 4 < len(sys.argv):
                max_tokens = int(sys.argv[i + 4])

        result = estimate_cost(text, max_tokens, model)
        print(f"📊 Model: {result['model']}")
        print(f"📊 Input tokens: {result['input_tokens']:,}")
        print(f"📊 Max output: {result['max_output_tokens']:,}")
        print(f"💰 Estimeret pris: ${result['estimated_cost_usd']:.6f}")
        if result['savings_if_cached'] > 0:
            print(f"💰 Besparelse med cache: "
                  f"${result['savings_if_cached']:.6f} (90%)")

    elif cmd == "cache-stats":
        stats = cache_stats()
        print(f"📊 Cache Statistik")
        print(f"{'='*30}")
        print(f"📦 Entries: {stats['entries']}")
        print(f"📏 Størrelse: {stats['total_size_kb']:.1f} KB")
        print(f"📁 Mappe: {stats['cache_dir']}")

    else:
        print(f"Ukendt kommando: {cmd}")
        print("Brug: count | count-file | cost | cache-stats")


if __name__ == "__main__":
    main()
