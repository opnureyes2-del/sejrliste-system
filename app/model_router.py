#!/usr/bin/env python3
"""
MODEL ROUTER - Automatic AI model selection per task type
Matches the plan: Opus for complex, Sonnet for code, Haiku for quick
"""
from enum import Enum
from typing import Optional
import os

class ModelType(Enum):
    OPUS = "claude-opus-4-5-20251101"
    SONNET = "claude-sonnet-4-20250514"
    HAIKU = "claude-haiku-3-5-20241022"

# Task type to model mapping (from plan)
MODEL_ROUTING = {
    # Complex tasks -> Opus
    "architecture": ModelType.OPUS,
    "planning": ModelType.OPUS,
    "complex_decisions": ModelType.OPUS,
    "pattern_analysis": ModelType.OPUS,
    "predictions": ModelType.OPUS,
    "optimization": ModelType.OPUS,

    # Implementation -> Sonnet
    "code_writing": ModelType.SONNET,
    "file_editing": ModelType.SONNET,
    "refactoring": ModelType.SONNET,
    "archiving": ModelType.SONNET,

    # Quick tasks -> Haiku
    "verification": ModelType.HAIKU,
    "simple_checks": ModelType.HAIKU,
    "formatting": ModelType.HAIKU,
    "logging": ModelType.HAIKU,
}

# DNA Lag to model mapping (from plan)
DNA_LAG_MODELS = {
    1: None,
    2: ModelType.HAIKU,
    3: ModelType.HAIKU,
    4: ModelType.OPUS,
    5: ModelType.SONNET,
    6: ModelType.OPUS,
    7: ModelType.OPUS,
}

# Token budgets per DNA lag (from plan)
TOKEN_BUDGETS = {
    2: 500,
    3: 1000,
    4: 3000,
    5: 1500,
    6: 2000,
    7: 4000,
}

class ModelRouter:
    """Routes tasks to appropriate AI model"""

    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.current_model: Optional[ModelType] = None
        self.tokens_used = 0
        self._usage_stats: dict = {}

    def get_model_for_task(self, task_type: str) -> ModelType:
        return MODEL_ROUTING.get(task_type, ModelType.HAIKU)

    def get_model_for_dna_lag(self, lag_number: int) -> Optional[ModelType]:
        return DNA_LAG_MODELS.get(lag_number)

    def get_token_budget(self, lag_number: int) -> int:
        return TOKEN_BUDGETS.get(lag_number, 1000)

    def select_model(self, task_type: str = None, dna_lag: int = None) -> Optional[ModelType]:
        if dna_lag:
            self.current_model = self.get_model_for_dna_lag(dna_lag)
        elif task_type:
            self.current_model = self.get_model_for_task(task_type)
        return self.current_model

    def track_usage(self, model: Optional[ModelType]):
        """Track model usage for statistics."""
        if model is None:
            return
        key = model.value
        self._usage_stats[key] = self._usage_stats.get(key, 0) + 1
        self.tokens_used += 1

    def get_usage_stats(self) -> dict:
        """Get model usage statistics."""
        return self._usage_stats.copy()

    def get_model_info(self, model: ModelType) -> dict:
        """Get information about a model."""
        info = {
            ModelType.OPUS: {"name": "Claude Opus 4.5", "tier": "premium"},
            ModelType.SONNET: {"name": "Claude Sonnet 4", "tier": "standard"},
            ModelType.HAIKU: {"name": "Claude Haiku 3.5", "tier": "fast"},
        }
        return info.get(model, {"name": "Unknown", "tier": "unknown"})

    def get_model_short_name(self) -> str:
        if self.current_model == ModelType.OPUS:
            return "Opus"
        elif self.current_model == ModelType.SONNET:
            return "Sonnet"
        elif self.current_model == ModelType.HAIKU:
            return "Haiku"
        return "None"

# Script to model mapping
SCRIPT_MODELS = {
    "auto_verify": ModelType.HAIKU,
    "auto_learn": ModelType.OPUS,
    "auto_archive": ModelType.SONNET,
    "auto_predict": ModelType.OPUS,
    "auto_health_check": ModelType.HAIKU,
    "generate_sejr": ModelType.SONNET,
}

def get_model_for_script(script_name: str) -> ModelType:
    """Get the recommended model for a script."""
    return SCRIPT_MODELS.get(script_name, ModelType.HAIKU)

router = ModelRouter()
