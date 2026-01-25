#!/usr/bin/env python3
"""
Unit tests for Visual Polish Widgets.

Tests:
1. Colors class
2. StatusIndicator
3. SessionTimer
4. StatisticsView
5. ProgressAnimation
6. VisualPolishWidget
"""

import sys
import time
from pathlib import Path
import unittest

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.widgets.visual_polish import (
    Colors,
    StatusIndicator,
    SessionTimer,
    StatisticsView,
    ProgressAnimation,
    VisualPolishWidget,
)


class TestColors(unittest.TestCase):
    """Test cases for Colors class."""

    def test_colors_exist(self):
        """Test that color constants exist."""
        self.assertIsNotNone(Colors.GREEN)
        self.assertIsNotNone(Colors.YELLOW)
        self.assertIsNotNone(Colors.RED)
        self.assertIsNotNone(Colors.BLUE)
        self.assertIsNotNone(Colors.RESET)

    def test_colors_are_ansi(self):
        """Test that colors are ANSI escape codes."""
        self.assertIn("\033[", Colors.GREEN)
        self.assertIn("\033[", Colors.RESET)


class TestStatusIndicator(unittest.TestCase):
    """Test cases for StatusIndicator."""

    def test_get_icon_done(self):
        """Test done status icon."""
        icon = StatusIndicator.get_icon("done")
        self.assertIn("✅", icon)

    def test_get_icon_in_progress(self):
        """Test in_progress status icon."""
        icon = StatusIndicator.get_icon("in_progress")
        self.assertIn("🔵", icon)

    def test_get_icon_blocked(self):
        """Test blocked status icon."""
        icon = StatusIndicator.get_icon("blocked")
        self.assertIn("🔴", icon)

    def test_get_icon_unknown(self):
        """Test unknown status returns default."""
        icon = StatusIndicator.get_icon("unknown_status")
        self.assertEqual(icon, "•")

    def test_get_progress_color_high(self):
        """Test high progress returns green."""
        color = StatusIndicator.get_progress_color(85)
        self.assertEqual(color, Colors.GREEN)

    def test_get_progress_color_medium(self):
        """Test medium progress returns yellow."""
        color = StatusIndicator.get_progress_color(65)
        self.assertEqual(color, Colors.YELLOW)

    def test_get_progress_color_low(self):
        """Test low progress returns red."""
        color = StatusIndicator.get_progress_color(25)
        self.assertEqual(color, Colors.RED)

    def test_colorize(self):
        """Test text colorization."""
        result = StatusIndicator.colorize("test", Colors.GREEN)
        self.assertIn(Colors.GREEN, result)
        self.assertIn(Colors.RESET, result)
        self.assertIn("test", result)


class TestSessionTimer(unittest.TestCase):
    """Test cases for SessionTimer."""

    def test_init(self):
        """Test timer initialization."""
        timer = SessionTimer()
        self.assertIsNone(timer.start_time)
        self.assertFalse(timer.is_paused)

    def test_start(self):
        """Test timer start."""
        timer = SessionTimer()
        timer.start()
        self.assertIsNotNone(timer.start_time)

    def test_elapsed_without_start(self):
        """Test elapsed time without starting."""
        timer = SessionTimer()
        elapsed = timer.get_elapsed()
        self.assertEqual(elapsed.total_seconds(), 0)

    def test_elapsed_after_start(self):
        """Test elapsed time after starting."""
        timer = SessionTimer()
        timer.start()
        time.sleep(0.1)
        elapsed = timer.get_elapsed()
        self.assertGreater(elapsed.total_seconds(), 0)

    def test_pause_resume(self):
        """Test pause and resume."""
        timer = SessionTimer()
        timer.start()
        time.sleep(0.1)
        timer.pause()
        self.assertTrue(timer.is_paused)
        timer.resume()
        self.assertFalse(timer.is_paused)

    def test_format_elapsed(self):
        """Test elapsed time formatting."""
        timer = SessionTimer()
        timer.start()
        formatted = timer.format_elapsed()
        self.assertRegex(formatted, r'\d{2}:\d{2}:\d{2}')

    def test_render(self):
        """Test timer rendering."""
        timer = SessionTimer()
        timer.start()
        rendered = timer.render()
        self.assertIn("Session:", rendered)
        self.assertIn("RUNNING", rendered)


class TestProgressAnimation(unittest.TestCase):
    """Test cases for ProgressAnimation."""

    def test_spinner(self):
        """Test spinner animation."""
        anim = ProgressAnimation()
        frame1 = anim.get_spinner()
        frame2 = anim.get_spinner()
        # Frames should cycle
        self.assertIsNotNone(frame1)
        self.assertIsNotNone(frame2)

    def test_progress_bar(self):
        """Test progress bar generation."""
        bar = ProgressAnimation.get_progress_bar(50)
        self.assertIn("50%", bar)
        self.assertIn("█", bar)
        self.assertIn("░", bar)

    def test_progress_bar_0_percent(self):
        """Test progress bar at 0%."""
        bar = ProgressAnimation.get_progress_bar(0)
        self.assertIn("0%", bar)

    def test_progress_bar_100_percent(self):
        """Test progress bar at 100%."""
        bar = ProgressAnimation.get_progress_bar(100)
        self.assertIn("100%", bar)

    def test_completion_message(self):
        """Test completion message."""
        msg = ProgressAnimation.get_completion_message()
        self.assertIsNotNone(msg)
        self.assertTrue(len(msg) > 0)


class TestStatisticsView(unittest.TestCase):
    """Test cases for StatisticsView."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_path = Path("/home/rasmus/Desktop/sejrliste systemet")

    def test_init(self):
        """Test StatisticsView initialization."""
        stats = StatisticsView(self.test_path)
        self.assertEqual(stats.system_path, self.test_path)

    def test_get_stats(self):
        """Test get_stats returns dict."""
        stats = StatisticsView(self.test_path)
        result = stats.get_stats()
        self.assertIsInstance(result, dict)
        self.assertIn("sejr_completed", result)
        self.assertIn("tests_passed", result)
        self.assertIn("patterns_learned", result)

    def test_render(self):
        """Test render output."""
        stats = StatisticsView(self.test_path)
        rendered = stats.render()
        self.assertIn("STATISTICS", rendered)
        self.assertIn("Sejr Completed", rendered)


class TestVisualPolishWidget(unittest.TestCase):
    """Test cases for VisualPolishWidget."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_path = Path("/home/rasmus/Desktop/sejrliste systemet")
        self.widget = VisualPolishWidget(self.test_path)

    def test_init(self):
        """Test widget initialization."""
        self.assertIsNotNone(self.widget.timer)
        self.assertIsNotNone(self.widget.stats)
        self.assertIsNotNone(self.widget.animation)

    def test_start_session(self):
        """Test session start."""
        self.widget.start_session()
        self.assertIsNotNone(self.widget.timer.start_time)

    def test_get_status_icon(self):
        """Test status icon getter."""
        icon = self.widget.get_status_icon("done")
        self.assertIn("✅", icon)

    def test_get_progress_bar(self):
        """Test progress bar getter."""
        bar = self.widget.get_progress_bar(75)
        self.assertIn("75%", bar)

    def test_render_dashboard(self):
        """Test dashboard rendering."""
        self.widget.start_session()
        dashboard = self.widget.render_dashboard()
        self.assertIn("DASHBOARD", dashboard)
        self.assertIn("Stats", dashboard)


if __name__ == "__main__":
    unittest.main(verbosity=2)
