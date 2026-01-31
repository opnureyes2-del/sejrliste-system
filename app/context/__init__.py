"""
SEJR CONTEXT SYSTEM
===================

Obligatoriske regler og constraints for Sejrliste arbejde.

Files:
- SEJR_RULES.md: 7 obligatoriske regler per sejr
- MODEL_CONSTRAINTS.yaml: Token budgets og model routing
"""

from pathlib import Path

CONTEXT_DIR = Path(__file__).parent
RULES_FILE = CONTEXT_DIR / "SEJR_RULES.md"
CONSTRAINTS_FILE = CONTEXT_DIR / "MODEL_CONSTRAINTS.yaml"


def load_rules() -> str:
    """Load obligatoriske sejr regler."""
    if RULES_FILE.exists():
        return RULES_FILE.read_text()
    return ""


def load_constraints() -> dict:
    """Load model constraints og token budgets (no PyYAML dependency)."""
    if not CONSTRAINTS_FILE.exists():
        return {}

    # Simple YAML parser for our specific format
    result = {}
    try:
        content = CONSTRAINTS_FILE.read_text()
        current_section = None

        for line in content.split('\n'):
            line = line.rstrip()
            if not line or line.strip().startswith('#'):
                continue

            # Top-level key (no indent)
            if not line.startswith(' ') and ':' in line:
                key = line.split(':')[0].strip()
                value = line.split(':', 1)[1].strip() if ':' in line else ''
                if not value:
                    result[key] = {}
                    current_section = key
                else:
                    result[key] = value.strip('"').strip("'")
                    current_section = None
            # Nested key (indented)
            elif current_section and ':' in line:
                key = line.split(':')[0].strip()
                value = line.split(':', 1)[1].strip().strip('"').strip("'")
                # Convert types
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                result[current_section][key] = value
    except Exception:
        pass
    return result


def get_model_for_task(task_type: str) -> str:
    """Get the recommended model for a task type."""
    constraints = load_constraints()
    routing = constraints.get("model_routing", {})
    return routing.get(task_type, "claude-sonnet-4-20250514")


def get_token_budget(dna_lag: int) -> int:
    """Get token budget for a DNA lag (1-7)."""
    constraints = load_constraints()
    budgets = constraints.get("token_budgets", {})
    lag_key = f"lag_{dna_lag}_{'aware' if dna_lag == 1 else ['documenting', 'verifying', 'improving', 'archiving', 'predictive', 'optimizing'][dna_lag - 2]}"
    lag_config = budgets.get(lag_key, {})
    return lag_config.get("max_tokens", 1000) if isinstance(lag_config, dict) else lag_config
