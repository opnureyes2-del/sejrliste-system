#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
               AUTO_OPTIMIZE.PY - SELVOPTIMERENDE TEMPLATE SYSTEM
═══════════════════════════════════════════════════════════════════════════════

DNA Lag 7: SELF-OPTIMIZING

FORMÅL:
  - Læser mønstre fra alle gennemførte sejr
  - Genererer PERSONALISEREDE tips til nye sejr
  - Opdaterer templates med best practices
  - Forbedrer systemet for HVER eneste sejr

INSPIRATION FRA ALLE PROJEKTER:
  - Cirkelline: Chakra-farvet feedback
  - INTRO: Systematisk dokumentation
  - ELLE: Kv1nt partnership wisdom
  - Admiral Orders: Obligatoriske kvalitetskrav

═══════════════════════════════════════════════════════════════════════════════
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Paths
SYSTEM_PATH = Path(__file__).parent.parent
PATTERNS_FILE = SYSTEM_PATH / "_CURRENT" / "PATTERNS.json"
LEARNED_TIPS_FILE = SYSTEM_PATH / "_CURRENT" / "LEARNED_TIPS.md"
TEMPLATES_DIR = SYSTEM_PATH / "00_TEMPLATES"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"

# ═══════════════════════════════════════════════════════════════════════════════
# PATTERN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def load_patterns() -> Dict:
    """Load learned patterns from PATTERNS.json"""
    if PATTERNS_FILE.exists():
        return json.loads(PATTERNS_FILE.read_text())
    return {"learned_patterns": []}


def get_top_patterns(patterns: Dict, n: int = 10) -> List[Dict]:
    """Get top N patterns by confidence"""
    all_patterns = patterns.get("learned_patterns", [])
    sorted_patterns = sorted(all_patterns, key=lambda p: p.get("confidence", 0), reverse=True)
    return sorted_patterns[:n]


def categorize_patterns(patterns: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize patterns by type"""
    categories = {
        "bugs": [],
        "workflows": [],
        "tools": [],
        "technical": [],
        "success": [],
        "reusable": [],
        "other": []
    }

    for p in patterns:
        pattern_text = p.get("pattern", "").lower()
        if "bug" in pattern_text:
            categories["bugs"].append(p)
        elif "workflow" in pattern_text:
            categories["workflows"].append(p)
        elif "tool" in pattern_text:
            categories["tools"].append(p)
        elif "technical" in pattern_text:
            categories["technical"].append(p)
        elif "success" in pattern_text:
            categories["success"].append(p)
        elif "reusable" in pattern_text:
            categories["reusable"].append(p)
        else:
            categories["other"].append(p)

    return categories


# ═══════════════════════════════════════════════════════════════════════════════
# TIP GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_tips_for_sejr(patterns: Dict, sejr_type: str = "general") -> str:
    """Generate personalized tips based on learned patterns"""
    tips = []
    all_patterns = patterns.get("learned_patterns", [])
    categories = categorize_patterns(all_patterns)

    # Header
    tips.append("# LÆRTE TIPS - Baseret på tidligere sejr")
    tips.append("")
    tips.append(f"*Genereret: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    tips.append(f"*Baseret på: {len(all_patterns)} mønstre fra {patterns.get('system', {}).get('total_patterns', 0)} sejr*")
    tips.append("")

    # Success rate
    for p in categories["success"]:
        tips.append("## SUCCESS RATE")
        tips.append(f"- {p['pattern']}")
        tips.append(f"- **Optimering:** {p.get('optimization', 'N/A')}")
        tips.append("")
        break

    # Bug warnings
    if categories["bugs"]:
        tips.append("## KENDTE FALDGRUBER")
        for p in categories["bugs"][:3]:  # Top 3 bugs
            tips.append(f"- {p['pattern']}")
            tips.append(f"  - **Forebyg:** {p.get('prevention', 'N/A')}")
        tips.append("")

    # Best workflows
    if categories["workflows"]:
        tips.append("## BEDSTE WORKFLOWS")
        for p in categories["workflows"][:3]:
            tips.append(f"- {p['pattern']}")
        tips.append("")

    # Useful tools
    if categories["tools"]:
        tips.append("## NYTTIGE VÆRKTØJER")
        for p in categories["tools"][:3]:
            tips.append(f"- {p['pattern']}")
        tips.append("")

    # Technical tips
    if categories["technical"]:
        tips.append("## TEKNISKE TIPS")
        for p in categories["technical"][:3]:
            tips.append(f"- {p['pattern']}")
        tips.append("")

    # Reusable items
    if categories["reusable"]:
        tips.append("## GENBRUGELIGE RESSOURCER")
        for p in categories["reusable"][:3]:
            tips.append(f"- {p['pattern']}")
        tips.append("")

    # Admiral wisdom
    tips.append("## ADMIRAL VISDOM")
    tips.append("")
    tips.append("```")
    tips.append("1. ÉN TING AD GANGEN - Færdiggør før du starter nyt")
    tips.append("2. BEVIS IKKE TOMME ORD - Vis kørende kode, ikke planer")
    tips.append("3. 3-PASS TVINGER FORBEDRING - Score SKAL stige")
    tips.append("4. 7-DNA GENNEMGANG - Check alle lag før arkivering")
    tips.append("5. OVERRASK - Gør mere end forventet")
    tips.append("```")
    tips.append("")

    return "\n".join(tips)


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE OPTIMIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def count_archive_stats() -> Dict:
    """Count statistics from archived sejrs"""
    stats = {
        "total": 0,
        "grand_admirals": 0,
        "avg_score": 0,
        "common_issues": [],
        "best_practices": []
    }

    scores = []

    if ARCHIVE_DIR.exists():
        for folder in ARCHIVE_DIR.iterdir():
            if folder.is_dir():
                stats["total"] += 1

                # Check for diplom
                diplom = folder / "SEJR_DIPLOM.md"
                if diplom.exists():
                    content = diplom.read_text()
                    if "GRAND ADMIRAL" in content:
                        stats["grand_admirals"] += 1

                    # Extract score
                    import re
                    score_match = re.search(r'(\d+)/30', content)
                    if score_match:
                        scores.append(int(score_match.group(1)))

    if scores:
        stats["avg_score"] = sum(scores) / len(scores)

    return stats


def generate_optimized_prompt() -> str:
    """Generate an optimized prompt based on all learnings"""
    patterns = load_patterns()
    stats = count_archive_stats()

    prompt = []
    prompt.append("# OPTIMERET SEJR PROMPT")
    prompt.append("")
    prompt.append(f"*Auto-genereret baseret på {stats['total']} gennemførte sejr*")
    prompt.append(f"*Success rate: {stats['grand_admirals']}/{stats['total']} GRAND ADMIRAL ({int(stats['grand_admirals']/max(1,stats['total'])*100)}%)*")
    prompt.append(f"*Gennemsnitlig score: {stats['avg_score']:.1f}/30*")
    prompt.append("")
    prompt.append("---")
    prompt.append("")
    prompt.append("## NÅR DU STARTER EN NY SEJR:")
    prompt.append("")
    prompt.append("1. **Læs PROJECT_BRIEF.md først** - Forstå målet på <30 sekunder")
    prompt.append("2. **Check LEARNED_TIPS.md** - Undgå kendte faldgruber")
    prompt.append("3. **Planlæg Pass 1 grundigt** - Kvalitet her reducerer arbejde i Pass 2-3")
    prompt.append("4. **Brug eksisterende værktøjer** - Check scripts/ før du bygger nyt")
    prompt.append("5. **Document AS du arbejder** - Ikke bagefter")
    prompt.append("")
    prompt.append("## KVALITETSKRAV (OBLIGATORISK):")
    prompt.append("")
    prompt.append("- [ ] Score stiger mellem passes")
    prompt.append("- [ ] Alle 7 DNA lag gennemgået i Pass 3")
    prompt.append("- [ ] Minimum 5 tests bestået")
    prompt.append("- [ ] Kode KØRER (ikke bare eksisterer)")
    prompt.append("- [ ] Dokumentation opdateret")
    prompt.append("")

    return "\n".join(prompt)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("═══════════════════════════════════════════════════════════════════════════════")
    print("               AUTO_OPTIMIZE - Selvoptimerende Template System")
    print("═══════════════════════════════════════════════════════════════════════════════")
    print()

    # Load patterns
    patterns = load_patterns()
    total_patterns = len(patterns.get("learned_patterns", []))
    print(f"Loaded {total_patterns} patterns from PATTERNS.json")

    # Get archive stats
    stats = count_archive_stats()
    print(f"\n Archive Stats:")
    print(f"   Total sejr: {stats['total']}")
    print(f"   Grand Admirals: {stats['grand_admirals']}")
    print(f"   Success rate: {int(stats['grand_admirals']/max(1,stats['total'])*100)}%")
    print(f"   Avg score: {stats['avg_score']:.1f}/30")

    # Generate tips
    tips = generate_tips_for_sejr(patterns)
    LEARNED_TIPS_FILE.write_text(tips)
    print(f"\n Generated: {LEARNED_TIPS_FILE}")

    # Generate optimized prompt
    prompt = generate_optimized_prompt()
    prompt_file = SYSTEM_PATH / "_CURRENT" / "OPTIMIZED_PROMPT.md"
    prompt_file.write_text(prompt)
    print(f" Generated: {prompt_file}")

    # Update template with learned tips link
    template_path = TEMPLATES_DIR / "SEJR_TEMPLATE.md"
    if template_path.exists():
        content = template_path.read_text()
        if "LEARNED_TIPS" not in content:
            # Add reference to learned tips
            addition = "\n\n> **TIP:** Check `_CURRENT/LEARNED_TIPS.md` for advice baseret på tidligere sejr!\n"
            if "## PASS 1:" in content:
                content = content.replace("## PASS 1:", addition + "\n## PASS 1:")
                template_path.write_text(content)
                print(f" Updated: {template_path}")

    print("\n═══════════════════════════════════════════════════════════════════════════════")
    print("✅ SELF-OPTIMIZATION COMPLETE")
    print("═══════════════════════════════════════════════════════════════════════════════")

    # Preview tips
    print("\n GENERATED TIPS PREVIEW:")
    print("-" * 60)
    for line in tips.split("\n")[:20]:
        print(f"  {line}")
    print("  ...")


if __name__ == "__main__":
    main()
