#!/usr/bin/env python3
"""
Unit tests for ModelHandler.

Tests:
1. ModelHandler initialization
2. Available models list
3. DNA lag model selection
4. Script model selection
5. Prompt creation
6. Request/response handling
7. Usage statistics
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import unittest
from app.models.model_handler import ModelHandler, ModelConfig, ModelResponse
from app.model_router import Model


class TestModelHandler(unittest.TestCase):
    """Test cases for ModelHandler."""

    def setUp(self):
        """Set up test fixtures."""
        self.handler = ModelHandler()

    def test_init(self):
        """Test ModelHandler initialization."""
        self.assertIsNotNone(self.handler)
        self.assertIsNotNone(self.handler.router)
        self.assertIsNotNone(self.handler.config)

    def test_available_models(self):
        """Test get_available_models returns correct list."""
        models = self.handler.get_available_models()
        self.assertEqual(len(models), 3)
        self.assertIn("opus", models)
        self.assertIn("sonnet", models)
        self.assertIn("haiku", models)

    def test_dna_lag_model_selection(self):
        """Test model selection for DNA lags."""
        # Lag 1-3 should use Haiku
        self.assertEqual(self.handler.get_model_for_dna_lag(1), "haiku")
        self.assertEqual(self.handler.get_model_for_dna_lag(2), "haiku")
        self.assertEqual(self.handler.get_model_for_dna_lag(3), "haiku")

        # Lag 4 should use Opus
        self.assertEqual(self.handler.get_model_for_dna_lag(4), "opus")

        # Lag 5 should use Sonnet
        self.assertEqual(self.handler.get_model_for_dna_lag(5), "sonnet")

        # Lag 6-7 should use Opus
        self.assertEqual(self.handler.get_model_for_dna_lag(6), "opus")
        self.assertEqual(self.handler.get_model_for_dna_lag(7), "opus")

    def test_script_model_selection(self):
        """Test model selection for scripts."""
        self.assertEqual(self.handler.get_model_for_script("auto_verify"), "haiku")
        self.assertEqual(self.handler.get_model_for_script("auto_learn"), "opus")
        self.assertEqual(self.handler.get_model_for_script("auto_archive"), "sonnet")
        self.assertEqual(self.handler.get_model_for_script("auto_predict"), "opus")

    def test_prompt_creation(self):
        """Test prompt creation with context."""
        prompt = self.handler.create_prompt(
            "Test task",
            context={"key": "value"},
            dna_lag=3
        )
        self.assertIn("DNA Lag 3", prompt)
        self.assertIn("SELF-VERIFYING", prompt)
        self.assertIn("Test task", prompt)
        self.assertIn("key: value", prompt)

    def test_send_request_mock(self):
        """Test sending a mock request."""
        response = self.handler.send_request(
            "Test prompt for verification",
            dna_lag=3
        )
        self.assertIsInstance(response, ModelResponse)
        self.assertTrue(response.success)
        self.assertIn("HAIKU", response.content)  # Lag 3 uses Haiku

    def test_request_logging(self):
        """Test that requests are logged."""
        initial_count = len(self.handler.get_request_log())

        self.handler.send_request("Test prompt", dna_lag=2)

        log = self.handler.get_request_log()
        self.assertEqual(len(log), initial_count + 1)
        self.assertIn("model", log[-1])
        self.assertIn("success", log[-1])

    def test_usage_stats(self):
        """Test usage statistics tracking."""
        # Make some requests
        self.handler.send_request("Test", dna_lag=3)  # Haiku
        self.handler.send_request("Test", dna_lag=4)  # Opus

        stats = self.handler.get_usage_stats()
        self.assertIsInstance(stats, dict)
        # Stats should have entries for models used
        self.assertGreaterEqual(stats.get(Model.HAIKU.value, 0), 1)
        self.assertGreaterEqual(stats.get(Model.OPUS.value, 0), 1)

    def test_render_status(self):
        """Test status rendering."""
        status = self.handler.render_status()
        self.assertIn("MODEL HANDLER STATUS", status)
        self.assertIn("Available Models", status)
        self.assertIn("Usage Statistics", status)

    def test_model_config(self):
        """Test custom ModelConfig."""
        config = ModelConfig(
            max_tokens=2048,
            temperature=0.5,
            timeout=30
        )
        handler = ModelHandler(config=config)
        self.assertEqual(handler.config.max_tokens, 2048)
        self.assertEqual(handler.config.temperature, 0.5)
        self.assertEqual(handler.config.timeout, 30)


class TestModelResponse(unittest.TestCase):
    """Test cases for ModelResponse dataclass."""

    def test_response_creation(self):
        """Test creating a ModelResponse."""
        response = ModelResponse(
            content="Test content",
            model="test-model",
            tokens_used=100,
            duration_ms=50,
            success=True
        )
        self.assertEqual(response.content, "Test content")
        self.assertTrue(response.success)

    def test_response_to_dict(self):
        """Test converting response to dict."""
        response = ModelResponse(
            content="Short content",
            model="test-model",
            tokens_used=50,
            duration_ms=25,
            success=True
        )
        d = response.to_dict()
        self.assertIn("content", d)
        self.assertIn("model", d)
        self.assertIn("success", d)

    def test_long_content_truncation(self):
        """Test that long content is truncated in to_dict."""
        long_content = "x" * 1000
        response = ModelResponse(
            content=long_content,
            model="test-model",
            tokens_used=1000,
            duration_ms=100,
            success=True
        )
        d = response.to_dict()
        self.assertLess(len(d["content"]), len(long_content))
        self.assertIn("...", d["content"])


if __name__ == "__main__":
    # Run with verbosity
    unittest.main(verbosity=2)
