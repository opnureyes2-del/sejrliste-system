#!/usr/bin/env python3
"""
Model Router for Sejrliste Visual System.

Routes tasks to appropriate AI models based on DNA lag and task complexity.

Model Selection:
- Opus: Complex analysis, architecture, predictions (Lag 4, 6, 7)
- Sonnet: Code writing, implementation (Lag 5 archive extraction)
- Haiku: Quick checks, verification, logging (Lag 2, 3)
"""

from typing import Optional, Dict, Any
from enum import Enum


class Model(Enum):
    """Available AI models."""
    OPUS = "claude-opus-4-5-20251101"
    SONNET = "claude-sonnet-4-20250514"
    HAIKU = "claude-haiku"


# DNA Lag to Model mapping
DNA_LAG_MODELS: Dict[int, Model] = {
    1: Model.HAIKU,    # SELF-AWARE - metadata only, minimal model needed
    2: Model.HAIKU,    # SELF-DOCUMENTING - quick logging
    3: Model.HAIKU,    # SELF-VERIFYING - run verification commands
    4: Model.OPUS,     # SELF-IMPROVING - pattern analysis
    5: Model.SONNET,   # SELF-ARCHIVING - extract conclusions
    6: Model.OPUS,     # PREDICTIVE - generate predictions
    7: Model.OPUS,     # SELF-OPTIMIZING - research alternatives
}

# Task type to Model mapping
TASK_MODELS: Dict[str, Model] = {
    # Complex tasks → Opus
    "architecture": Model.OPUS,
    "planning": Model.OPUS,
    "complex_decisions": Model.OPUS,
    "pattern_analysis": Model.OPUS,
    "predictions": Model.OPUS,
    "research": Model.OPUS,

    # Implementation → Sonnet
    "code_writing": Model.SONNET,
    "file_editing": Model.SONNET,
    "refactoring": Model.SONNET,
    "extraction": Model.SONNET,

    # Quick tasks → Haiku
    "verification": Model.HAIKU,
    "simple_checks": Model.HAIKU,
    "formatting": Model.HAIKU,
    "logging": Model.HAIKU,
}


class ModelRouter:
    """
    Routes tasks to appropriate AI models.

    Uses DNA lag or task type to determine optimal model.
    """

    def __init__(self):
        """Initialize the router."""
        self._usage_stats: Dict[str, int] = {
            Model.OPUS.value: 0,
            Model.SONNET.value: 0,
            Model.HAIKU.value: 0,
        }

    def get_model_for_dna_lag(self, lag_number: int) -> Model:
        """
        Get the recommended model for a DNA lag.

        Args:
            lag_number: DNA lag number (1-7)

        Returns:
            Model enum value
        """
        return DNA_LAG_MODELS.get(lag_number, Model.HAIKU)

    def get_model_for_task(self, task_type: str) -> Model:
        """
        Get the recommended model for a task type.

        Args:
            task_type: Type of task (e.g., "verification", "planning")

        Returns:
            Model enum value
        """
        return TASK_MODELS.get(task_type.lower(), Model.SONNET)

    def get_model_id(self, model: Model) -> str:
        """Get the model ID string for API calls."""
        return model.value

    def track_usage(self, model: Model):
        """Track model usage for statistics."""
        self._usage_stats[model.value] = self._usage_stats.get(model.value, 0) + 1

    def get_usage_stats(self) -> Dict[str, int]:
        """Get usage statistics for all models."""
        return self._usage_stats.copy()

    def get_model_info(self, model: Model) -> Dict[str, Any]:
        """Get information about a model."""
        info = {
            Model.OPUS: {
                "name": "Claude Opus 4.5",
                "tier": "flagship",
                "best_for": ["complex analysis", "architecture", "predictions"],
                "token_cost": "high",
            },
            Model.SONNET: {
                "name": "Claude Sonnet 4",
                "tier": "balanced",
                "best_for": ["code writing", "implementation", "refactoring"],
                "token_cost": "medium",
            },
            Model.HAIKU: {
                "name": "Claude Haiku",
                "tier": "fast",
                "best_for": ["quick checks", "verification", "logging"],
                "token_cost": "low",
            },
        }
        return info.get(model, {})


def get_model_for_script(script_name: str) -> Model:
    """
    Get the recommended model for a script.

    Args:
        script_name: Name of the script (e.g., "auto_verify")

    Returns:
        Model enum value
    """
    script_to_lag = {
        "auto_track": 2,
        "auto_verify": 3,
        "auto_learn": 4,
        "auto_archive": 5,
        "auto_predict": 6,
        "generate_sejr": 7,
    }

    lag = script_to_lag.get(script_name)
    if lag:
        return DNA_LAG_MODELS.get(lag, Model.HAIKU)
    return Model.SONNET


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Testing ModelRouter...")

    router = ModelRouter()

    # Test DNA lag routing
    print("\nDNA Lag → Model mapping:")
    for lag in range(1, 8):
        model = router.get_model_for_dna_lag(lag)
        print(f"  Lag {lag}: {model.name} ({model.value})")

    # Test task routing
    print("\nTask Type → Model mapping:")
    for task in ["verification", "planning", "code_writing"]:
        model = router.get_model_for_task(task)
        print(f"  {task}: {model.name}")

    # Test script routing
    print("\nScript → Model mapping:")
    for script in ["auto_verify", "auto_learn", "auto_predict"]:
        model = get_model_for_script(script)
        print(f"  {script}: {model.name}")

    print("\nModelRouter test complete!")
