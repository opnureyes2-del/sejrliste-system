#!/usr/bin/env python3
"""
Auto-learn patterns from completed sejr
Part of SEJR LISTE SYSTEM - DNA Layer 4 (SELF-IMPROVING)

INGEN EXTERNAL DEPENDENCIES - Kun Python standard library
"""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter


# ============================================================================
# SIMPLE YAML PARSING (No PyYAML dependency)
# ============================================================================

def parse_yaml_simple(filepath: Path) -> dict:
    """Parse simple YAML without PyYAML."""
    if not filepath.exists():
        return {}

    result = {}
    try:
        content = filepath.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if ":" in line and not line.strip().startswith("#"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().strip('"').strip("'")
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    elif value.replace(".", "").isdigit():
                        value = float(value) if "." in value else int(value)
                    result[key] = value
    except:
        pass
    return result


def write_yaml_simple(filepath: Path, data: dict, indent: int = 0):
    """Write simple YAML without PyYAML. Supports nested dicts and lists."""
    def _to_yaml_lines(obj, level=0):
        lines = []
        prefix = "  " * level

        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, dict):
                    lines.append(f"{prefix}{key}:")
                    lines.extend(_to_yaml_lines(value, level + 1))
                elif isinstance(value, list):
                    lines.append(f"{prefix}{key}:")
                    for item in value:
                        if isinstance(item, dict):
                            lines.append(f"{prefix}  -")
                            for k, v in item.items():
                                if isinstance(v, bool):
                                    v_str = "true" if v else "false"
                                elif v is None:
                                    v_str = "null"
                                else:
                                    v_str = f'"{v}"' if isinstance(v, str) else str(v)
                                lines.append(f"{prefix}    {k}: {v_str}")
                        else:
                            lines.append(f"{prefix}  - {item}")
                else:
                    if isinstance(value, bool):
                        value_str = "true" if value else "false"
                    elif value is None:
                        value_str = "null"
                    elif isinstance(value, str):
                        value_str = f'"{value}"'
                    else:
                        value_str = str(value)
                    lines.append(f"{prefix}{key}: {value_str}")
        return lines

    yaml_lines = _to_yaml_lines(data)
    filepath.write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")

def extract_learnings_from_sejr(sejr_path: Path):
    """Extract semantic learnings from completed SEJR_LISTE.md"""
    sejr_file = sejr_path / "SEJR_LISTE.md"

    if not sejr_file.exists():
        return None

    with open(sejr_file, 'r') as f:
        content = f.read()

    # Extract metrics section
    metrics = {}
    in_metrics = False
    for line in content.split('\n'):
        if '### Metrics' in line:
            in_metrics = True
            continue

        if in_metrics:
            if line.strip().startswith('-'):
                # Parse metric lines
                if ':' in line:
                    key, value = line.strip('- ').split(':', 1)
                    metrics[key.strip()] = value.strip()
            elif line.startswith('##'):
                break

    # Extract learnings section
    learnings = []
    in_learnings = False
    for line in content.split('\n'):
        if '### Hvad Lærte Vi' in line:
            in_learnings = True
            continue

        if in_learnings:
            if line.strip() and not line.startswith('#'):
                learnings.append(line.strip())
            elif line.startswith('##'):
                break

    # Parse AUTO_LOG.jsonl for patterns
    log_file = sejr_path / "AUTO_LOG.jsonl"
    actions = []
    if log_file.exists():
        with open(log_file, 'r') as f:
            for line in f:
                actions.append(json.loads(line))

    return {
        'name': sejr_path.name,
        'metrics': metrics,
        'learnings': learnings,
        'actions': actions
    }

def identify_patterns(all_sejr_data: list):
    """Identify patterns across multiple completed sejr"""
    patterns = []

    # Pattern 1: Time estimation accuracy
    time_diffs = []
    for sejr in all_sejr_data:
        if 'Difference' in sejr['metrics']:
            diff_str = sejr['metrics']['Difference']
            # Parse difference (could be "±X min" format)
            # For simplicity, we'll track if there's a pattern
            time_diffs.append(diff_str)

    if time_diffs:
        patterns.append({
            'pattern': 'Time estimation variance observed',
            'prevention': 'Use previous sejr averages for better estimates',
            'optimization': 'Auto-suggest time based on similar sejr patterns',
            'confidence': 0.7,
            'first_seen': datetime.now().strftime("%Y-%m-%d")
        })

    # Pattern 2: Common blockers
    all_actions = []
    for sejr in all_sejr_data:
        all_actions.extend(sejr['actions'])

    # Count action types to find common patterns
    action_types = Counter(a.get('action', 'unknown') for a in all_actions)

    # Pattern 3: Learnings that repeat
    all_learnings = []
    for sejr in all_sejr_data:
        all_learnings.extend(sejr['learnings'])

    # Simple keyword matching for repeated learnings
    learning_keywords = []
    for learning in all_learnings:
        words = learning.lower().split()
        learning_keywords.extend([w for w in words if len(w) > 4])

    common_keywords = Counter(learning_keywords).most_common(3)

    if common_keywords:
        for keyword, count in common_keywords:
            if count > 1:  # Repeated at least twice
                patterns.append({
                    'pattern': f'Repeated learning about: {keyword}',
                    'prevention': f'Create reusable template for {keyword} tasks',
                    'optimization': f'Auto-suggest best practices for {keyword}',
                    'confidence': min(0.9, count * 0.3),
                    'first_seen': datetime.now().strftime("%Y-%m-%d")
                })

    return patterns

def update_patterns_yaml(system_path: Path, new_patterns: list):
    """Update _CURRENT/PATTERNS.yaml with newly learned patterns"""
    patterns_file = system_path / "_CURRENT" / "PATTERNS.yaml"

    # Load existing patterns (use JSON for complex structures)
    patterns_json = patterns_file.with_suffix('.json')
    if patterns_json.exists():
        with open(patterns_json, 'r') as f:
            data = json.load(f)
    elif patterns_file.exists():
        # Try to read existing YAML (simple format)
        data = parse_yaml_simple(patterns_file)
        if 'learned_patterns' not in data:
            data['learned_patterns'] = []
        if 'system' not in data:
            data['system'] = {'version': '1.0.0', 'last_learned': None, 'total_patterns': 0}
    else:
        data = {
            'system': {
                'version': '1.0.0',
                'last_learned': None,
                'total_patterns': 0
            },
            'learned_patterns': []
        }

    # Add new patterns (avoid duplicates)
    existing_patterns = [p['pattern'] for p in data.get('learned_patterns', [])]

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

    # Update metadata
    data['system']['last_learned'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data['system']['total_patterns'] = len(data['learned_patterns'])

    # Write back as JSON (better for complex nested structures)
    patterns_json = patterns_file.with_suffix('.json')
    with open(patterns_json, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Also write simple YAML for human readability
    write_yaml_simple(patterns_file, {
        'system_version': data['system'].get('version', '1.0.0'),
        'last_learned': data['system'].get('last_learned'),
        'total_patterns': data['system'].get('total_patterns', 0)
    })

    print(f"✅ Updated: {patterns_file}")
    print(f"   Added {len([p for p in new_patterns if p['pattern'] not in existing_patterns])} new patterns")

def learn_from_completed(system_path: Path):
    """Learn from all completed sejr in archive"""
    archive_dir = system_path / "90_ARCHIVE"

    if not archive_dir.exists():
        print("ℹ️  No archive directory yet - no completed sejr to learn from")
        return

    completed_sejr = [f for f in archive_dir.iterdir() if f.is_dir()]

    if not completed_sejr:
        print("ℹ️  No completed sejr found in archive")
        return

    print(f"🧠 Learning from {len(completed_sejr)} completed sejr...\n")

    # Extract data from all completed sejr
    all_sejr_data = []
    for sejr_path in completed_sejr:
        data = extract_learnings_from_sejr(sejr_path)
        if data:
            all_sejr_data.append(data)

    if not all_sejr_data:
        print("⚠️  No learnings could be extracted")
        return

    # Identify patterns
    patterns = identify_patterns(all_sejr_data)

    if patterns:
        print(f"📊 Identified {len(patterns)} new patterns:")
        for p in patterns:
            print(f"   • {p['pattern']}")
        print()

        # Update PATTERNS.yaml
        update_patterns_yaml(system_path, patterns)
    else:
        print("ℹ️  No new patterns identified")

if __name__ == "__main__":
    system_path = Path(__file__).parent.parent
    learn_from_completed(system_path)
