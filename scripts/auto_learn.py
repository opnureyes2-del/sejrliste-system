#!/usr/bin/env python3
"""
Auto-learn patterns from completed sejr
Part of SEJR LISTE SYSTEM - DNA Layer 4 (SELF-IMPROVING)

INGEN EXTERNAL DEPENDENCIES - Kun Python standard library
"""

import json
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))
from yaml_utils import parse_yaml_simple


# ============================================================================
# BLACKLISTS - Filter ud værdiløs data (ADMIRAL STANDARD)
# ============================================================================

# Placeholder tekst der ALDRIG skal detekteres som patterns
PLACEHOLDER_BLACKLIST = {
    '_learnings_', '_ikke', '_beskriv', '_tid_', '_dato_',
    'dokumenteret', 'ikke dokumenteret', '_ikke dokumenteret_',
    'beskriv konkret', 'n/a', 'none', 'null', 'undefined',
    '_patterns_', '_reusable_', '_improvements_'
}

# Danske stop-words der er for generelle til at være patterns
DANISH_STOPWORDS = {
    # Almindelige ord
    'systemet', 'system', 'faktisk', 'tvinger', 'gennemføre', 'arbejde',
    'gennem', 'bruges', 'bruger', 'blevet', 'bliver', 'derfor', 'derefter',
    'selvom', 'stadig', 'altid', 'aldrig', 'nemlig', 'fordi', 'hvordan',
    'sådan', 'mellem', 'efter', 'under', 'inden', 'omkring', 'overfor',
    # Projekt-generiske
    'projekt', 'projektet', 'filen', 'filer', 'koden', 'scriptet',
    'funktionen', 'metoden', 'klassen', 'modulet', 'komponenten'
}

# Actions der er for generiske til at være interessante
GENERIC_ACTIONS = {
    'unknown', 'model_request', 'log', 'info', 'debug', 'trace'
}


def write_yaml_simple(filepath: Path, data: dict, indent: int = 0):
    """Write YAML using PyYAML (preserves nested structures)."""
    yaml_content = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    filepath.write_text(yaml_content, encoding="utf-8")

def extract_learnings_from_sejr(sejr_path: Path):
    """Extract semantic learnings from archived sejr (reads CONCLUSION.md)"""
    # Archived sejr have CONCLUSION.md, not SEJR_LISTE.md
    conclusion_file = sejr_path / "CONCLUSION.md"
    status_file = sejr_path / "STATUS.yaml"

    if not conclusion_file.exists():
        return None

    content = conclusion_file.read_text(encoding="utf-8")

    # Extract metrics from STATUS.yaml
    metrics = {}
    if status_file.exists():
        status = parse_yaml_simple(status_file)
        metrics = {
            'pass_1_score': status.get('pass_1_score', 0),
            'pass_2_score': status.get('pass_2_score', 0),
            'pass_3_score': status.get('pass_3_score', 0),
            'total_score': status.get('total_score', 0),
        }

    # Extract learnings from CONCLUSION.md
    # Look for "## Hvad Lærte Vi" section
    learnings = []
    in_learnings = False
    for line in content.split('\n'):
        if '## Hvad Lærte Vi' in line:
            in_learnings = True
            continue
        if in_learnings:
            if line.startswith('##'):
                break
            if line.strip() and not line.strip().startswith('-'):
                learnings.append(line.strip())

    # Extract reusable items from "## Hvad Kan Genbruges"
    reusable = []
    in_reusable = False
    for line in content.split('\n'):
        if '## Hvad Kan Genbruges' in line:
            in_reusable = True
            continue
        if in_reusable:
            if line.startswith('##'):
                break
            if line.strip().startswith('-'):
                reusable.append(line.strip().lstrip('- '))

    # Extract improvement proofs from "### Pass X → Pass Y Forbedring"
    improvements = []
    in_improvement = False
    for line in content.split('\n'):
        if '→' in line and 'Forbedring' in line:
            in_improvement = True
            continue
        if in_improvement:
            if line.startswith('#'):
                in_improvement = False
                continue
            if line.strip():
                improvements.append(line.strip())

    # Parse AUTO_LOG.jsonl for action patterns
    log_file = sejr_path / "AUTO_LOG.jsonl"
    actions = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        actions.append(json.loads(line))
        except:
            pass

    return {
        'name': sejr_path.name,
        'metrics': metrics,
        'learnings': learnings,
        'reusable': reusable,
        'improvements': improvements,
        'actions': actions
    }

def is_blacklisted(text: str) -> bool:
    """Check if text is blacklisted placeholder or stop-word"""
    text_lower = text.lower().strip()
    # Check exact match
    if text_lower in PLACEHOLDER_BLACKLIST or text_lower in DANISH_STOPWORDS:
        return True
    # Check if starts with underscore (template placeholder)
    if text_lower.startswith('_') and text_lower.endswith('_'):
        return True
    return False


def extract_semantic_patterns(learnings: list[str]) -> list[dict]:
    """Extract MEANINGFUL semantic patterns from learnings, not word counts."""
    patterns = []
    seen_texts = set()  # Track to avoid duplicates

    # Categories of actionable patterns - MUTUALLY EXCLUSIVE
    categorized = {}  # learning -> best category

    for learning in learnings:
        if not learning or is_blacklisted(learning):
            continue

        learning_lower = learning.lower()
        learning_key = learning[:50].lower()  # Use first 50 chars as dedup key

        if learning_key in seen_texts:
            continue
        seen_texts.add(learning_key)

        # Determine BEST category (priority order: BUG > WORKFLOW > TOOL > TECHNICAL)
        category = None

        # Pattern: Bug fixes - highest priority (specific learnings from errors)
        if any(kw in learning_lower for kw in ['fejl', 'bug', 'løsning', 'fikse', 'rettet']):
            if 'fordi' in learning_lower or 'løsning' in learning_lower:
                category = 'BUG_FIX'

        # Pattern: Workflow rules - "altid", "aldrig", "skal"
        elif any(kw in learning_lower for kw in ['altid', 'aldrig', 'skal', 'must', 'never', 'always']):
            if len(learning) > 20:
                category = 'WORKFLOW'

        # Pattern: Script/tool learnings
        elif any(kw in learning_lower for kw in ['.py', 'script', 'auto_', 'generate_', 'executor']):
            category = 'TOOL'

        # Pattern: Technical (API/regex/path issues)
        elif any(kw in learning_lower for kw in ['regex', 'api', 'path', 'mock', 'test']):
            category = 'TECHNICAL'

        if category:
            categorized[learning] = category

    # Create patterns from categorized learnings (no duplicates)
    today = datetime.now().strftime("%Y-%m-%d")

    # Group by category
    by_category = {'BUG_FIX': [], 'WORKFLOW': [], 'TOOL': [], 'TECHNICAL': []}
    for learning, cat in categorized.items():
        by_category[cat].append(learning)

    # BUG patterns (top 3)
    for bug in by_category['BUG_FIX'][:3]:
        patterns.append({
            'pattern': f'BUG LÆRT: {bug[:100]}',
            'prevention': 'Check for this issue in similar contexts',
            'optimization': 'Add to pre-flight checklist',
            'category': 'BUG_FIX',
            'confidence': 0.95,
            'first_seen': today
        })

    # WORKFLOW patterns (top 3)
    for wf in by_category['WORKFLOW'][:3]:
        patterns.append({
            'pattern': f'WORKFLOW: {wf[:100]}',
            'prevention': 'Follow this rule in similar situations',
            'optimization': 'Automate enforcement if possible',
            'category': 'WORKFLOW',
            'confidence': 0.9,
            'first_seen': today
        })

    # TOOL patterns (top 2)
    for tool in by_category['TOOL'][:2]:
        patterns.append({
            'pattern': f'TOOL: {tool[:100]}',
            'prevention': 'Use existing tool before creating new',
            'optimization': 'Document tool usage and edge cases',
            'category': 'TOOL',
            'confidence': 0.85,
            'first_seen': today
        })

    # TECHNICAL patterns (top 2)
    for tech in by_category['TECHNICAL'][:2]:
        patterns.append({
            'pattern': f'TECHNICAL: {tech[:100]}',
            'prevention': 'Remember this technical constraint',
            'optimization': 'Add to technical documentation',
            'category': 'TECHNICAL',
            'confidence': 0.9,
            'first_seen': today
        })

    return patterns


def identify_patterns(all_sejr_data: list):
    """Identify MEANINGFUL patterns across completed sejr (ADMIRAL STANDARD)"""
    patterns = []
    today = datetime.now().strftime("%Y-%m-%d")

    # ========================================================================
    # META PATTERN 1: Overall success rate (keep this, it's useful)
    # ========================================================================
    grand_admirals = sum(1 for s in all_sejr_data if s['metrics'].get('total_score', 0) >= 27)
    total = len(all_sejr_data)

    if total > 0:
        success_rate = grand_admirals / total
        if success_rate >= 0.5:
            patterns.append({
                'pattern': f'SUCCESS RATE: {grand_admirals}/{total} sejr opnår GRAND ADMIRAL ({int(success_rate*100)}%)',
                'prevention': 'Bevar 3-pass system med obligatorisk review',
                'optimization': 'Fokusér på Pass 1 kvalitet for at reducere Pass 2-3 arbejde',
                'category': 'META',
                'confidence': 0.98,
                'first_seen': today
            })

    # ========================================================================
    # SEMANTIC PATTERNS: Extract from actual learnings (REAL VALUE)
    # ========================================================================
    all_learnings = []
    for sejr in all_sejr_data:
        all_learnings.extend(sejr.get('learnings', []))

    # Filter out blacklisted and short learnings
    quality_learnings = [l for l in all_learnings
                        if l and len(l) > 20 and not is_blacklisted(l)]

    if quality_learnings:
        semantic_patterns = extract_semantic_patterns(quality_learnings)
        patterns.extend(semantic_patterns)

    # ========================================================================
    # REUSABLE ITEMS: Konkrete genbrugelige ting (scripts, templates, patterns)
    # ========================================================================
    all_reusable = []
    for sejr in all_sejr_data:
        all_reusable.extend(sejr.get('reusable', []))

    # Filter quality reusable items
    quality_reusable = [r for r in all_reusable
                       if r and len(r) > 10 and not is_blacklisted(r)]

    # Group by type (Script:, Template:, Pattern:, etc.)
    reusable_by_type = {}
    for item in quality_reusable:
        if ':' in item:
            item_type = item.split(':')[0].strip()
            content = item.split(':', 1)[1].strip()
            if item_type not in reusable_by_type:
                reusable_by_type[item_type] = []
            reusable_by_type[item_type].append(content)

    for item_type, items in reusable_by_type.items():
        if len(items) >= 2:
            patterns.append({
                'pattern': f'REUSABLE {item_type.upper()}: {len(items)} identificeret',
                'prevention': f'Check eksisterende {item_type} før oprettelse af ny',
                'optimization': f'Katalogisér {item_type} i 00_TEMPLATES/',
                'category': 'REUSABLE',
                'confidence': 0.85,
                'first_seen': today,
                'details': items[:5]  # Keep top 5 examples
            })

    # ========================================================================
    # IMPROVEMENT PATTERNS: Hvad forbedres typisk mellem passes?
    # ========================================================================
    all_improvements = []
    for sejr in all_sejr_data:
        all_improvements.extend(sejr.get('improvements', []))

    quality_improvements = [i for i in all_improvements
                           if i and len(i) > 15 and not is_blacklisted(i)]

    if quality_improvements:
        # Find common improvement themes
        improvement_keywords = []
        for imp in quality_improvements:
            imp_lower = imp.lower()
            if 'test' in imp_lower:
                improvement_keywords.append('tests')
            if 'dokumentation' in imp_lower or 'docs' in imp_lower:
                improvement_keywords.append('documentation')
            if 'refactor' in imp_lower or 'cleanup' in imp_lower:
                improvement_keywords.append('refactoring')
            if 'error' in imp_lower or 'fejl' in imp_lower:
                improvement_keywords.append('error_handling')

        for keyword, count in Counter(improvement_keywords).most_common(3):
            if count >= 2:
                patterns.append({
                    'pattern': f'IMPROVEMENT FOCUS: {keyword} forbedres i {count} sejr',
                    'prevention': f'Inkludér {keyword} fra Pass 1',
                    'optimization': f'Brug {keyword} checklist i template',
                    'category': 'IMPROVEMENT',
                    'confidence': 0.8,
                    'first_seen': today
                })

    # ========================================================================
    # ACTION PATTERNS: Normaliser og filtrer (kun VALUABLE actions)
    # ========================================================================
    all_actions = []
    for sejr in all_sejr_data:
        all_actions.extend(sejr.get('actions', []))

    if all_actions:
        # Normalize action names (lowercase, strip)
        action_types = Counter(
            a.get('action', 'unknown').lower().strip()
            for a in all_actions
        )

        # Filter out generic/blacklisted actions
        valuable_actions = {
            action: count for action, count in action_types.items()
            if action not in GENERIC_ACTIONS
            and count >= 5
            and not is_blacklisted(action)
        }

        for action, count in sorted(valuable_actions.items(), key=lambda x: -x[1])[:3]:
            patterns.append({
                'pattern': f'FREQUENT ACTION: {action} ({count}x across sejr)',
                'prevention': f'Consider automating {action}',
                'optimization': f'Create script/hotkey for {action}',
                'category': 'AUTOMATION',
                'confidence': min(0.9, count * 0.05),
                'first_seen': today
            })

    return patterns

def update_patterns_yaml(system_path: Path, new_patterns: list):
    """Update _CURRENT/PATTERNS.yaml with newly learned patterns"""
    patterns_file = system_path / "_CURRENT" / "PATTERNS.yaml"
    patterns_json = patterns_file.with_suffix('.json')

    # Initialize fresh data structure
    data = {
        'system': {
            'version': '1.0.0',
            'last_learned': None,
            'total_patterns': 0
        },
        'learned_patterns': []
    }

    # Load existing patterns from JSON if exists
    if patterns_json.exists():
        try:
            with open(patterns_json, 'r') as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    if 'system' in loaded and isinstance(loaded['system'], dict):
                        data['system'] = loaded['system']
                    if 'learned_patterns' in loaded and isinstance(loaded['learned_patterns'], list):
                        data['learned_patterns'] = loaded['learned_patterns']
        except:
            pass  # Use fresh data if JSON is corrupt

    # Add new patterns (avoid duplicates)
    existing_patterns = [p.get('pattern', '') for p in data['learned_patterns'] if isinstance(p, dict)]
    added_count = 0

    for pattern in new_patterns:
        if pattern['pattern'] not in existing_patterns:
            data['learned_patterns'].append({
                'pattern': pattern['pattern'],
                'prevention': pattern['prevention'],
                'optimization': pattern['optimization'],
                'applied_count': 0,
                'time_saved_total': '0 min',
                'confidence': pattern['confidence'],
                'first_seen': pattern['first_seen'],
                'last_applied': None
            })
            added_count += 1

    # Update metadata
    data['system']['last_learned'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data['system']['total_patterns'] = len(data['learned_patterns'])

    # Write as JSON (better for complex nested structures)
    with open(patterns_json, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Also write simple YAML summary for human readability
    yaml_summary = f"""# PATTERNS - Auto-learned from {data['system']['total_patterns']} patterns
# Last updated: {data['system']['last_learned']}
# Full data in: PATTERNS.json

system_version: "1.0.0"
last_learned: "{data['system']['last_learned']}"
total_patterns: {data['system']['total_patterns']}

# Top patterns (see PATTERNS.json for full list):
"""
    for p in data['learned_patterns'][:5]:
        yaml_summary += f"\n# - {p['pattern'][:60]}..."

    patterns_file.write_text(yaml_summary, encoding="utf-8")

    print(f"[OK] Updated: {patterns_json}")
    print(f"   Total patterns: {data['system']['total_patterns']}")
    print(f"   Added {added_count} new patterns")

def learn_from_completed(system_path: Path):
    """Learn from all completed sejr in archive"""
    archive_dir = system_path / "90_ARCHIVE"

    if not archive_dir.exists():
        print("[INFO]  No archive directory yet - no completed sejr to learn from")
        return

    completed_sejr = [f for f in archive_dir.iterdir() if f.is_dir()]

    if not completed_sejr:
        print("[INFO]  No completed sejr found in archive")
        return

    print(f" Learning from {len(completed_sejr)} completed sejr...\n")

    # Extract data from all completed sejr
    all_sejr_data = []
    for sejr_path in completed_sejr:
        data = extract_learnings_from_sejr(sejr_path)
        if data:
            all_sejr_data.append(data)

    if not all_sejr_data:
        print("[WARN]  No learnings could be extracted")
        return

    # Show what was extracted
    total_learnings = sum(len(s.get('learnings', [])) for s in all_sejr_data)
    total_reusable = sum(len(s.get('reusable', [])) for s in all_sejr_data)
    total_improvements = sum(len(s.get('improvements', [])) for s in all_sejr_data)
    print(f" Extracted from {len(all_sejr_data)} sejr:")
    print(f"   • {total_learnings} learnings")
    print(f"   • {total_reusable} reusable items")
    print(f"   • {total_improvements} improvement descriptions")
    print()

    # Identify patterns
    patterns = identify_patterns(all_sejr_data)

    if patterns:
        print(f" Identified {len(patterns)} new patterns:")
        for p in patterns:
            print(f"   • {p['pattern']}")
        print()

        # Update PATTERNS.yaml
        update_patterns_yaml(system_path, patterns)
    else:
        print("[INFO]  No new patterns identified")

if __name__ == "__main__":
    system_path = Path(__file__).parent.parent
    learn_from_completed(system_path)
