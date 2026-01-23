#!/usr/bin/env python3
"""
Auto-predict next steps based on patterns
Part of SEJR LISTE SYSTEM - DNA Layer 6 (PREDICTIVE)
"""

import yaml
from pathlib import Path
from datetime import datetime

def load_patterns(system_path: Path):
    """Load learned patterns from PATTERNS.yaml"""
    patterns_file = system_path / "_CURRENT" / "PATTERNS.yaml"

    if patterns_file.exists():
        with open(patterns_file, 'r') as f:
            return yaml.safe_load(f)

    return {'learned_patterns': [], 'statistics': {}}

def scan_current_state(system_path: Path):
    """Scan current state to inform predictions"""
    active_dir = system_path / "10_ACTIVE"

    if not active_dir.exists():
        return {
            'active_sejr_count': 0,
            'status_distribution': {},
            'needs_attention': []
        }

    sejr_folders = [f for f in active_dir.iterdir() if f.is_dir()]

    status_counts = {}
    needs_attention = []

    for sejr_folder in sejr_folders:
        status_file = sejr_folder / "VERIFY_STATUS.yaml"

        if status_file.exists():
            with open(status_file, 'r') as f:
                status = yaml.safe_load(f)

            status_name = status.get('status', 'unknown')
            status_counts[status_name] = status_counts.get(status_name, 0) + 1

            # Identify sejr that need attention
            completion = status.get('completion_percentage', 0)
            if completion >= 75 and completion < 100:
                needs_attention.append({
                    'name': sejr_folder.name,
                    'completion': completion,
                    'reason': 'Nearly complete - needs final push'
                })

    return {
        'active_sejr_count': len(sejr_folders),
        'status_distribution': status_counts,
        'needs_attention': needs_attention
    }

def generate_predictions(patterns_data: dict, current_state: dict):
    """Generate AI-driven predictions for next steps"""
    predictions = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'next_steps': [],
        'insights': [],
        'suggested_focus': None
    }

    # Prediction 1: Based on active sejr count
    if current_state['active_sejr_count'] == 0:
        predictions['next_steps'].append({
            'priority': 'high',
            'action': 'Generate new sejr liste',
            'reasoning': 'No active projects - start something new',
            'command': 'python scripts/generate_sejr.py --name "Project Name"'
        })
        predictions['suggested_focus'] = 'Start new project'

    elif current_state['needs_attention']:
        # Focus on nearly complete work
        for sejr in current_state['needs_attention']:
            predictions['next_steps'].append({
                'priority': 'high',
                'action': f'Complete {sejr["name"]}',
                'reasoning': f'{sejr["completion"]:.0f}% done - finish it!',
                'command': f'# Work on remaining tasks in SEJR_LISTE.md'
            })
        predictions['suggested_focus'] = f'Complete {current_state["needs_attention"][0]["name"]}'

    else:
        predictions['next_steps'].append({
            'priority': 'medium',
            'action': 'Continue with active sejr',
            'reasoning': f'{current_state["active_sejr_count"]} active project(s) in progress',
            'command': 'cat _CURRENT/STATE.md  # Check current state'
        })
        predictions['suggested_focus'] = 'Continue current work'

    # Prediction 2: Based on learned patterns
    if patterns_data.get('learned_patterns'):
        high_confidence_patterns = [
            p for p in patterns_data['learned_patterns']
            if p.get('confidence', 0) > 0.7
        ]

        if high_confidence_patterns:
            predictions['insights'].append({
                'type': 'pattern_based',
                'insight': f'{len(high_confidence_patterns)} high-confidence patterns learned',
                'suggestion': 'Apply learned optimizations to avoid repeated mistakes'
            })

    # Prediction 3: Maintenance suggestions
    if current_state['active_sejr_count'] > 3:
        predictions['insights'].append({
            'type': 'maintenance',
            'insight': 'Many active sejr - risk of context switching',
            'suggestion': 'Focus on completing before starting new ones'
        })

    return predictions

def update_next_md(system_path: Path, predictions: dict):
    """Update _CURRENT/NEXT.md with predictions"""
    next_file = system_path / "_CURRENT" / "NEXT.md"

    content = f"""# NEXT - Hvad Skal Ske Nu?

**AI-Genereret:** {predictions['timestamp']}
**Baseret på:** Current state + Learned patterns

---

## NÆSTE SKRIDT (Prioriteret)

"""

    for i, step in enumerate(predictions['next_steps'], 1):
        priority_emoji = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }.get(step['priority'], '⚪')

        content += f"""### {i}. {step['action']} ({priority_emoji} {step['priority'].title()} Prioritet)
**Hvorfor:** {step['reasoning']}

**Action:**
```bash
{step['command']}
```

"""

    if predictions['insights']:
        content += """---

## PREDICTIVE INSIGHTS (AI-Drevet)

"""

        for insight in predictions['insights']:
            content += f"""### {insight['type'].replace('_', ' ').title()}
**Observation:** {insight['insight']}
**Forslag:** {insight['suggestion']}

"""

    content += f"""---

## FORSLAG FRA SYSTEM

**Fokus lige nu:** {predictions['suggested_focus']}
**Reasoning:** Based on current progress and learned patterns

---

**Auto-opdateret af:** scripts/auto_predict.py
**Baseret på:** Previous sejr patterns + AI analysis + Current state
**Refreshed:** On-demand or after state changes
"""

    with open(next_file, 'w') as f:
        f.write(content)

    print(f"✅ Updated: {next_file}")
    print(f"   Generated {len(predictions['next_steps'])} next steps")
    print(f"   Suggested focus: {predictions['suggested_focus']}")

def run_prediction(system_path: Path):
    """Run full prediction cycle"""
    print("🔮 Generating predictions...\n")

    # Load patterns
    patterns_data = load_patterns(system_path)

    # Scan current state
    current_state = scan_current_state(system_path)

    print(f"📊 Current state:")
    print(f"   Active sejr: {current_state['active_sejr_count']}")
    print(f"   Needs attention: {len(current_state['needs_attention'])}")
    print(f"   Learned patterns: {len(patterns_data.get('learned_patterns', []))}\n")

    # Generate predictions
    predictions = generate_predictions(patterns_data, current_state)

    # Update NEXT.md
    update_next_md(system_path, predictions)

    print(f"\n✅ Predictions generated and saved to _CURRENT/NEXT.md")

if __name__ == "__main__":
    system_path = Path(__file__).parent.parent
    run_prediction(system_path)
