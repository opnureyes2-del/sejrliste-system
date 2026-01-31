#!/usr/bin/env python3
"""
ADMIRAL TRACKER - Konkurrence Score System
==========================================

Tracker positive og negative metrics for AI modeller.
Beregner scores og rankings.
Opretholder global leaderboard.

SCORE FORMEL:
  total = positive_points - (negative_points × 2)

RANKINGS:
  STORADMIRAL: 150+
  ADMIRAL: 100-149
  KAPTAJN: 50-99
  LØJTNANT: 20-49
  KADET: 0-19
  SKIBSDRENG: < 0
"""

import argparse
import sys
import yaml
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from yaml_utils import parse_yaml_simple


# Point values
POSITIVE_POINTS = {
    "CHECKBOX_DONE": 1,
    "PASS_COMPLETE": 10,
    "VERIFIED_WORKING": 5,
    "TEST_PASSED": 3,
    "IMPROVEMENT_FOUND": 5,
    "PROACTIVE_ACTION": 3,
    "GOOD_DOCUMENTATION": 2,
    "EFFICIENCY_BONUS": 5,
    "ADMIRAL_MOMENT": 10,
    "SEJR_ARCHIVED": 20,
}

NEGATIVE_POINTS = {
    "TOKEN_WASTE": -3,
    "MEMORY_LOSS": -5,
    "INCOMPLETE_STEP": -3,
    "SKIPPED_STEP": -5,
    "LIE_DETECTED": -10,
    "ERROR_MADE": -3,
    "DUMB_MOMENT": -5,
    "FOCUS_LOST": -3,
    "RULE_BREAK": -10,
    "ARCHIVE_BLOCKED": -5,
}

ACHIEVEMENT_BONUS = {
    "perfekt_pass": 15,
    "flawless_sejr": 50,
    "speed_demon": 10,
    "memory_master": 20,
    "doc_king": 10,
    "bug_hunter": 15,
}

RANKS = [
    ("STORADMIRAL", 150),
    ("ADMIRAL", 100),
    ("KAPTAJN", 50),
    ("LØJTNANT", 20),
    ("KADET", 0),
    ("SKIBSDRENG", -999),
]


def write_yaml_simple(filepath: Path, data: dict):
    """Write YAML using PyYAML (preserves nested structures)."""
    header = f"# ADMIRAL SCORE - Auto-updated\n# Updated: {datetime.now().isoformat()}\n\n"
    yaml_content = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    filepath.write_text(header + yaml_content, encoding="utf-8")


def get_rank(score: int) -> str:
    """Get rank based on score."""
    for rank, threshold in RANKS:
        if score >= threshold:
            return rank
    return "SKIBSDRENG"


def calculate_totals(data: dict) -> dict:
    """Calculate total scores."""
    positive = data.get("positive", {})
    negative = data.get("negative", {})
    achievements = data.get("achievements", {})

    # Calculate positive points
    positive_total = 0
    for key, count in positive.items():
        if isinstance(count, int):
            event_key = key.upper()
            if event_key in POSITIVE_POINTS:
                positive_total += count * POSITIVE_POINTS[event_key]

    # Calculate negative points
    negative_total = 0
    for key, count in negative.items():
        if isinstance(count, int):
            event_key = key.upper()
            if event_key in NEGATIVE_POINTS:
                negative_total += count * abs(NEGATIVE_POINTS[event_key])

    # Calculate achievement bonus
    achievement_total = 0
    for key, achieved in achievements.items():
        if achieved and key in ACHIEVEMENT_BONUS:
            achievement_total += ACHIEVEMENT_BONUS[key]

    # Total score (negative counts double!)
    total_score = positive_total - (negative_total * 2) + achievement_total

    return {
        "positive_points": positive_total,
        "negative_points": negative_total,
        "negative_multiplied": negative_total * 2,
        "achievement_bonus": achievement_total,
        "total_score": total_score,
        "rank": get_rank(total_score),
    }


def log_event(sejr_path: Path, event_type: str, note: str = ""):
    """Log an event to ADMIRAL_SCORE.yaml."""
    score_file = sejr_path / "ADMIRAL_SCORE.yaml"

    if not score_file.exists():
        print(f"[FAIL] ADMIRAL_SCORE.yaml not found in {sejr_path}")
        return

    data = parse_yaml_simple(score_file)

    # Determine if positive or negative
    event_upper = event_type.upper()
    event_lower = event_type.lower()

    if event_upper in POSITIVE_POINTS:
        section = "positive"
        points = POSITIVE_POINTS[event_upper]
    elif event_upper in NEGATIVE_POINTS:
        section = "negative"
        points = NEGATIVE_POINTS[event_upper]
    else:
        print(f"[FAIL] Unknown event type: {event_type}")
        print(f"   Positive: {list(POSITIVE_POINTS.keys())}")
        print(f"   Negative: {list(NEGATIVE_POINTS.keys())}")
        return

    # Update count
    if section not in data:
        data[section] = {}

    if event_lower not in data[section]:
        data[section][event_lower] = 0

    data[section][event_lower] += 1

    # Recalculate totals
    data["totals"] = calculate_totals(data)

    # Save
    write_yaml_simple(score_file, data)

    # Print result
    symbol = "[OK]" if section == "positive" else "[FAIL]"
    multiplier = "" if section == "positive" else " (×2!)"
    print(f"{symbol} {event_upper}: {points:+d} points{multiplier}")
    print(f"   Note: {note}" if note else "")
    print(f"   Total Score: {data['totals']['total_score']} ({data['totals']['rank']})")


def show_score(sejr_path: Path):
    """Show current score for a sejr."""
    score_file = sejr_path / "ADMIRAL_SCORE.yaml"

    if not score_file.exists():
        print(f"[FAIL] No ADMIRAL_SCORE.yaml in {sejr_path}")
        return

    data = parse_yaml_simple(score_file)
    totals = calculate_totals(data)

    print("\n" + "=" * 60)
    print(f"  ADMIRAL SCORE: {sejr_path.name}")
    print("=" * 60)

    print(f"\n MODEL: {data.get('meta', {}).get('model_name', 'Unknown')}")

    print("\n[OK] POSITIVE:")
    positive = data.get("positive", {})
    for key, count in positive.items():
        if count > 0:
            pts = POSITIVE_POINTS.get(key.upper(), 0)
            print(f"   {key}: {count} × {pts} = +{count * pts}")
    print(f"   SUBTOTAL: +{totals['positive_points']}")

    print("\n[FAIL] NEGATIVE (×2!):")
    negative = data.get("negative", {})
    for key, count in negative.items():
        if count > 0:
            pts = abs(NEGATIVE_POINTS.get(key.upper(), 0))
            print(f"   {key}: {count} × {pts} × 2 = -{count * pts * 2}")
    print(f"   SUBTOTAL: -{totals['negative_multiplied']}")

    if totals['achievement_bonus'] > 0:
        print(f"\n ACHIEVEMENTS: +{totals['achievement_bonus']}")

    print("\n" + "-" * 40)
    print(f" TOTAL SCORE: {totals['total_score']}")
    print(f"  RANK: {totals['rank']}")
    print("=" * 60 + "\n")


def _extract_score_from_status(sejr_path: Path) -> dict | None:
    """Extract score from STATUS.yaml (used by auto_verify.py)."""
    status_file = sejr_path / "STATUS.yaml"
    if not status_file.exists():
        return None

    data = parse_yaml_simple(status_file)
    score = data.get("score", 0)
    if isinstance(score, (int, float)):
        return {
            "sejr": sejr_path.name,
            "model": data.get("created_by", "Kv1nt"),
            "score": int(score),
            "rank": get_rank(int(score)),
        }
    return None


def _extract_score_from_diplom(sejr_path: Path) -> dict | None:
    """Extract score from SEJR_DIPLOM.md (fallback)."""
    diplom_file = sejr_path / "SEJR_DIPLOM.md"
    if not diplom_file.exists():
        return None

    try:
        content = diplom_file.read_text(encoding="utf-8")
        import re
        # Look for "SCORE: XX/30" pattern
        match = re.search(r"SCORE:\s*(\d+)/30", content)
        if match:
            score = int(match.group(1))
            # Look for rank
            rank_match = re.search(r"RANG:\s*(\w+)", content)
            rank = rank_match.group(1) if rank_match else get_rank(score)
            return {
                "sejr": sejr_path.name,
                "model": "Kv1nt",
                "score": score,
                "rank": rank,
            }
    except Exception:
        pass
    return None


def show_leaderboard(system_path: Path):
    """Show global leaderboard from all available score sources."""
    scores = []

    # Helper to collect scores from a directory
    def collect_from_dir(directory: Path, status_label: str):
        if not directory.exists():
            return
        for sejr_path in directory.iterdir():
            if not sejr_path.is_dir():
                continue

            # Try ADMIRAL_SCORE.yaml first (original format)
            score_file = sejr_path / "ADMIRAL_SCORE.yaml"
            if score_file.exists():
                data = parse_yaml_simple(score_file)
                totals = calculate_totals(data)
                scores.append({
                    "sejr": sejr_path.name,
                    "model": data.get("meta", {}).get("model_name", "Kv1nt"),
                    "score": totals["total_score"],
                    "rank": totals["rank"],
                    "status": status_label,
                })
                continue

            # Try SEJR_DIPLOM.md (has SCORE: XX/30)
            entry = _extract_score_from_diplom(sejr_path)
            if entry:
                entry["status"] = status_label
                scores.append(entry)
                continue

            # Try STATUS.yaml (auto_verify output)
            entry = _extract_score_from_status(sejr_path)
            if entry:
                entry["status"] = status_label
                scores.append(entry)

    # Collect from both directories
    collect_from_dir(system_path / "10_ACTIVE", "ACTIVE")
    collect_from_dir(system_path / "90_ARCHIVE", "ARCHIVED")

    # Sort by score
    scores.sort(key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 70)
    print(" ADMIRAL LEADERBOARD")
    print("=" * 70)

    if not scores:
        print("\nIngen scores endnu. Start en sejr for at begynde!")
    else:
        print(f"\n{'#':<3} {'Sejr':<40} {'Score':<8} {'Rank':<15} {'Status':<10}")
        print("-" * 80)
        for i, entry in enumerate(scores, 1):
            rank_emoji = {
                "STORADMIRAL": "",
                "ADMIRAL": "",
                "KAPTAJN": "",
                "LØJTNANT": "",
                "KADET": "",
                "SKIBSDRENG": "",
                "GRAND": "",
            }.get(entry["rank"], "")
            name = entry["sejr"][:38]
            print(f"{i:<3} {name:<40} {entry['score']:<8} {rank_emoji} {entry['rank']:<13} {entry['status']}")

    print(f"\nTotal: {len(scores)} sejr registreret")
    print("=" * 70 + "\n")


def finalize_sejr(sejr_path: Path):
    """Finalize scores and check achievements."""
    score_file = sejr_path / "ADMIRAL_SCORE.yaml"

    if not score_file.exists():
        print(f"[FAIL] No ADMIRAL_SCORE.yaml in {sejr_path}")
        return

    data = parse_yaml_simple(score_file)
    negative = data.get("negative", {})
    positive = data.get("positive", {})

    # Check achievements
    achievements = data.get("achievements", {})

    # Memory master: 0 memory_loss
    if negative.get("memory_loss", 0) == 0:
        achievements["memory_master"] = True
        print(" Achievement unlocked: MEMORY MASTER (+20)")

    # Doc king: 10+ good docs
    if positive.get("good_documentation", 0) >= 10:
        achievements["doc_king"] = True
        print(" Achievement unlocked: DOC KING (+10)")

    # Bug hunter: 5+ improvements
    if positive.get("improvement_found", 0) >= 5:
        achievements["bug_hunter"] = True
        print(" Achievement unlocked: BUG HUNTER (+15)")

    # Flawless sejr: 0 total negative
    total_negative = sum(v for v in negative.values() if isinstance(v, int))
    if total_negative == 0:
        achievements["flawless_sejr"] = True
        print(" Achievement unlocked: FLAWLESS SEJR (+50)")

    data["achievements"] = achievements
    data["totals"] = calculate_totals(data)

    write_yaml_simple(score_file, data)

    print(f"\n FINAL SCORE: {data['totals']['total_score']}")
    print(f" FINAL RANK: {data['totals']['rank']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ADMIRAL TRACKER - Konkurrence Score System"
    )
    parser.add_argument("--sejr", help="Sejr folder name")
    parser.add_argument("--event", help="Event type to log")
    parser.add_argument("--note", default="", help="Note for event")
    parser.add_argument("--score", action="store_true", help="Show current score")
    parser.add_argument("--leaderboard", action="store_true", help="Show leaderboard")
    parser.add_argument("--finalize", action="store_true", help="Finalize sejr score")
    args = parser.parse_args()

    system_path = Path(__file__).parent.parent

    if args.leaderboard:
        show_leaderboard(system_path)
    elif args.sejr:
        sejr_path = system_path / "10_ACTIVE" / args.sejr
        if not sejr_path.exists():
            sejr_path = system_path / "90_ARCHIVE" / args.sejr

        if not sejr_path.exists():
            print(f"[FAIL] Sejr not found: {args.sejr}")
        elif args.event:
            log_event(sejr_path, args.event, args.note)
        elif args.score:
            show_score(sejr_path)
        elif args.finalize:
            finalize_sejr(sejr_path)
        else:
            show_score(sejr_path)
    else:
        show_leaderboard(system_path)
