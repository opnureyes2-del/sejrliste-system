#!/usr/bin/env python3
"""
Unified Model Handler for Sejrliste Visual System.

Provides a single interface for interacting with all Claude models.
Integrates with model_router.py for automatic model selection.

Features:
- Automatic model selection via ModelRouter (DNA lag based)
- Sync and async request methods
- Request/response logging to AUTO_LOG.jsonl
- Mock implementation for testing (production: use AnthropicClient)
- Edge case handling (empty prompts, invalid lags)
"""

import os
import json
import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

# Import from parent package
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.model_router import ModelType, ModelRouter, get_model_for_script


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# API Client Skeleton (for future production use)
# ============================================================================

class AnthropicClient:
    """
    Skeleton for Anthropic API client.

    In production, replace mock methods with actual anthropic SDK calls:
        from anthropic import Anthropic, AsyncAnthropic

    This skeleton provides the interface for:
    - Sync message creation
    - Async message creation
    - Streaming responses (placeholder)
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the client.

        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._is_mock = True  # Set to False when using real API

    def create_message(self,
                       model: str,
                       messages: List[Dict[str, str]],
                       max_tokens: int = 4096,
                       system: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a message (sync).

        In production:
            client = Anthropic(api_key=self.api_key)
            return client.messages.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                system=system
            )
        """
        # Mock response
        return {
            "content": [{"text": f"[MOCK] Response from {model}"}],
            "usage": {"input_tokens": 100, "output_tokens": 50},
            "model": model,
        }

    async def create_message_async(self,
                                   model: str,
                                   messages: List[Dict[str, str]],
                                   max_tokens: int = 4096,
                                   system: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a message (async).

        In production:
            client = AsyncAnthropic(api_key=self.api_key)
            return await client.messages.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                system=system
            )
        """
        # Simulate async delay
        await asyncio.sleep(0.01)

        # Mock response
        return {
            "content": [{"text": f"[MOCK ASYNC] Response from {model}"}],
            "usage": {"input_tokens": 100, "output_tokens": 50},
            "model": model,
        }


@dataclass
class ModelConfig:
    """Configuration for model requests."""
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60
    system_prompt: Optional[str] = None


@dataclass
class ModelResponse:
    """Response from a model request."""
    content: str
    model: str
    tokens_used: int
    duration_ms: int
    success: bool
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "content": self.content[:500] + "..." if len(self.content) > 500 else self.content,
            "model": self.model,
            "tokens_used": self.tokens_used,
            "duration_ms": self.duration_ms,
            "success": self.success,
            "error": self.error,
            "timestamp": self.timestamp,
        }


class ModelHandler:
    """
    Unified handler for AI model interactions.

    Provides:
    - Automatic model selection via ModelRouter
    - Request/response logging
    - Token tracking
    - Error handling
    """

    # Base path for sejrliste system
    BASE_PATH = Path(__file__).parent.parent.parent

    def __init__(self, config: Optional[ModelConfig] = None):
        """
        Initialize the model handler.

        Args:
            config: Optional ModelConfig for default settings
        """
        self.config = config or ModelConfig()
        self.router = ModelRouter()
        self._request_log: List[Dict[str, Any]] = []

    def get_available_models(self) -> List[str]:
        """Get list of available model names."""
        return [m.name.lower() for m in ModelType]

    def get_model_for_dna_lag(self, lag_number: int) -> str:
        """
        Get the recommended model name for a DNA lag.

        Args:
            lag_number: DNA lag number (1-7)

        Returns:
            Model name (opus, sonnet, or haiku). Defaults to haiku for unknown/None lags.
        """
        model = self.router.get_model_for_dna_lag(lag_number)
        if model is None:
            return "haiku"
        return model.name.lower()

    def get_model_for_script(self, script_name: str) -> str:
        """
        Get the recommended model name for a script.

        Args:
            script_name: Name of the script (e.g., "auto_verify")

        Returns:
            Model name (opus, sonnet, or haiku)
        """
        model = get_model_for_script(script_name)
        return model.name.lower()

    def create_prompt(self,
                      task_description: str,
                      context: Optional[Dict[str, Any]] = None,
                      dna_lag: Optional[int] = None) -> str:
        """
        Create a structured prompt for the model.

        Args:
            task_description: What the model should do
            context: Optional context dictionary
            dna_lag: Optional DNA lag number for context

        Returns:
            Formatted prompt string
        """
        parts = []

        # Add DNA lag context if provided
        if dna_lag:
            lag_names = {
                1: "SELF-AWARE",
                2: "SELF-DOCUMENTING",
                3: "SELF-VERIFYING",
                4: "SELF-IMPROVING",
                5: "SELF-ARCHIVING",
                6: "PREDICTIVE",
                7: "SELF-OPTIMIZING",
            }
            parts.append(f"[DNA Lag {dna_lag}: {lag_names.get(dna_lag, 'UNKNOWN')}]")

        # Add context if provided
        if context:
            parts.append("Context:")
            for key, value in context.items():
                parts.append(f"  {key}: {value}")

        # Add task description
        parts.append(f"\nTask: {task_description}")

        return "\n".join(parts)

    def send_request(self,
                     prompt: str,
                     model: Optional[ModelType] = None,
                     dna_lag: Optional[int] = None,
                     config: Optional[ModelConfig] = None) -> ModelResponse:
        """
        Send a request to an AI model.

        Note: This is a mock implementation. In production, this would
        call the actual Anthropic API via AnthropicClient.

        Args:
            prompt: The prompt to send (empty prompts handled gracefully)
            model: Optional specific model to use
            dna_lag: Optional DNA lag for automatic model selection
            config: Optional config override

        Returns:
            ModelResponse with results
        """
        import time
        start_time = time.time()

        # Handle empty prompt edge case
        if not prompt or not prompt.strip():
            prompt = "[EMPTY PROMPT]"
            logger.warning("Empty prompt received, using placeholder")

        # Determine which model to use
        if model:
            selected_model = model
        elif dna_lag:
            selected_model = self.router.get_model_for_dna_lag(dna_lag)
        else:
            selected_model = None

        # Fallback to SONNET if no model selected (e.g. DNA lag 1 = None)
        if selected_model is None:
            selected_model = ModelType.SONNET

        # Track usage
        self.router.track_usage(selected_model)

        # Use provided config or default
        cfg = config or self.config

        try:
            # MOCK IMPLEMENTATION
            # In production, this would call anthropic.messages.create()
            response_content = self._mock_response(prompt, selected_model)

            duration_ms = int((time.time() - start_time) * 1000)

            response = ModelResponse(
                content=response_content,
                model=selected_model.value,
                tokens_used=len(prompt.split()) + len(response_content.split()),  # Rough estimate
                duration_ms=duration_ms,
                success=True,
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            response = ModelResponse(
                content="",
                model=selected_model.value,
                tokens_used=0,
                duration_ms=duration_ms,
                success=False,
                error=str(e),
            )
            logger.error(f"Model request failed: {e}")

        # Log the request
        self._log_request(prompt, response)

        return response

    def _mock_response(self, prompt: str, model: ModelType) -> str:
        """
        Generate a mock response for testing.

        In production, replace with actual API call.
        """
        model_name = model.name

        if "verify" in prompt.lower():
            return f"[{model_name}] Verification complete. All checks passed."
        elif "predict" in prompt.lower():
            return f"[{model_name}] Based on patterns, next steps: Continue current task."
        elif "archive" in prompt.lower():
            return f"[{model_name}] Semantic extraction complete. Key learnings captured."
        elif "learn" in prompt.lower():
            return f"[{model_name}] Pattern analysis complete. 2 new patterns identified."
        else:
            return f"[{model_name}] Task processed successfully."

    def _log_request(self, prompt: str, response: ModelResponse):
        """Log a request/response pair."""
        log_entry = {
            "timestamp": response.timestamp,
            "model": response.model,
            "prompt_length": len(prompt),
            "response_length": len(response.content),
            "tokens_used": response.tokens_used,
            "duration_ms": response.duration_ms,
            "success": response.success,
        }
        self._request_log.append(log_entry)

        # Also log to AUTO_LOG if active sejr exists
        self._log_to_auto_log(log_entry)

    def _log_to_auto_log(self, entry: Dict[str, Any]):
        """Log model activity to AUTO_LOG.jsonl if active sejr exists."""
        active_dir = self.BASE_PATH / "10_ACTIVE"
        if not active_dir.exists():
            return

        # Find active sejr folders
        for sejr_folder in active_dir.iterdir():
            if sejr_folder.is_dir():
                auto_log = sejr_folder / "AUTO_LOG.jsonl"
                if auto_log.exists():
                    try:
                        log_entry = {
                            "timestamp": entry["timestamp"],
                            "action": "model_request",
                            "model": entry["model"],
                            "tokens": entry["tokens_used"],
                            "duration_ms": entry["duration_ms"],
                            "success": entry["success"],
                        }
                        with open(auto_log, "a") as f:
                            f.write(json.dumps(log_entry) + "\n")
                    except Exception as e:
                        logger.warning(f"Could not log to AUTO_LOG: {e}")

    def get_request_log(self) -> List[Dict[str, Any]]:
        """Get the request log."""
        return self._request_log.copy()

    def get_usage_stats(self) -> Dict[str, int]:
        """Get model usage statistics."""
        return self.router.get_usage_stats()

    async def send_request_async(self,
                                  prompt: str,
                                  model: Optional[ModelType] = None,
                                  dna_lag: Optional[int] = None,
                                  config: Optional[ModelConfig] = None) -> ModelResponse:
        """
        Send a request to an AI model asynchronously.

        Args:
            prompt: The prompt to send
            model: Optional specific model to use
            dna_lag: Optional DNA lag for automatic model selection
            config: Optional config override

        Returns:
            ModelResponse with results
        """
        import time
        start_time = time.time()

        # Handle empty prompt edge case
        if not prompt or not prompt.strip():
            prompt = "[EMPTY PROMPT]"
            logger.warning("Empty prompt received, using placeholder")

        # Determine which model to use
        if model:
            selected_model = model
        elif dna_lag:
            selected_model = self.router.get_model_for_dna_lag(dna_lag)
        else:
            selected_model = None

        # Fallback to SONNET if no model selected (e.g. DNA lag 1 = None)
        if selected_model is None:
            selected_model = ModelType.SONNET

        # Track usage
        self.router.track_usage(selected_model)

        # Use provided config or default
        cfg = config or self.config

        try:
            # Simulate async operation
            await asyncio.sleep(0.01)

            # MOCK ASYNC IMPLEMENTATION
            response_content = f"[ASYNC {selected_model.name}] {self._mock_response(prompt, selected_model)}"

            duration_ms = int((time.time() - start_time) * 1000)

            response = ModelResponse(
                content=response_content,
                model=selected_model.value,
                tokens_used=len(prompt.split()) + len(response_content.split()),
                duration_ms=duration_ms,
                success=True,
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            response = ModelResponse(
                content="",
                model=selected_model.value,
                tokens_used=0,
                duration_ms=duration_ms,
                success=False,
                error=f"Async request failed: {str(e)}",
            )
            logger.error(f"Async model request failed: {e}")

        # Log the request
        self._log_request(prompt, response)

        return response

    def render_status(self, width: int = 50) -> str:
        """
        Render model status for terminal display.

        Args:
            width: Display width

        Returns:
            Formatted status string
        """
        lines = []
        lines.append("=" * width)
        lines.append("MODEL HANDLER STATUS".center(width))
        lines.append("=" * width)

        # Available models
        lines.append("\nAvailable Models:")
        for model in ModelType:
            info = self.router.get_model_info(model)
            lines.append(f"  {model.name}: {info.get('name', 'Unknown')} ({info.get('tier', 'unknown')})")

        # Usage stats
        stats = self.get_usage_stats()
        lines.append("\nUsage Statistics:")
        for model_id, count in stats.items():
            lines.append(f"  {model_id}: {count} requests")

        # Recent requests
        if self._request_log:
            lines.append(f"\nRecent Requests: {len(self._request_log)}")
            for entry in self._request_log[-3:]:
                lines.append(f"  [{entry['model']}] {entry['duration_ms']}ms, {entry['tokens_used']} tokens")

        lines.append("=" * width)
        return "\n".join(lines)


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Testing ModelHandler...")

    handler = ModelHandler()

    # Test available models
    print(f"\nAvailable models: {handler.get_available_models()}")

    # Test model selection for DNA lags
    print("\nDNA Lag → Model:")
    for lag in range(1, 8):
        model = handler.get_model_for_dna_lag(lag)
        print(f"  Lag {lag}: {model}")

    # Test prompt creation
    prompt = handler.create_prompt(
        "Verify all checkboxes are complete",
        context={"sejr": "TEST_SEJR", "pass": 1},
        dna_lag=3
    )
    print(f"\nSample prompt:\n{prompt}")

    # Test request (mock)
    response = handler.send_request(prompt, dna_lag=3)
    print(f"\nResponse: {response.content}")
    print(f"Model used: {response.model}")
    print(f"Tokens: {response.tokens_used}")

    # Test status rendering
    print("\n" + handler.render_status())

    print("\nModelHandler test complete!")
