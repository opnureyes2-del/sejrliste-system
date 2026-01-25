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
    """Load model constraints og token budgets."""
    import yaml
    if CONSTRAINTS_FILE.exists():
        with open(CONSTRAINTS_FILE) as f:
            return yaml.safe_load(f)
    return {}


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
