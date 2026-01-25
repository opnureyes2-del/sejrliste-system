#!/usr/bin/env python3
"""
Script Executor for Sejrliste Visual System.

Centralizes execution of DNA lag scripts with:
- Sync mode (terminal fallback)
- Async mode (Textual TUI)
- Output capture
- Timeout handling
- Error formatting
"""

import subprocess
import threading
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from datetime import datetime
import queue


class ScriptExecutor:
    """Execute DNA lag scripts with output capture."""

    # Script mapping: name -> (relative_path, dna_lag)
    SCRIPTS: Dict[str, Tuple[str, int]] = {
        "auto_track": ("scripts/auto_track.py", 2),
        "auto_verify": ("scripts/auto_verify.py", 3),
        "auto_learn": ("scripts/auto_learn.py", 4),
        "auto_archive": ("scripts/auto_archive.py", 5),
        "auto_predict": ("scripts/auto_predict.py", 6),
        "generate_sejr": ("scripts/generate_sejr.py", 7),
    }

    def __init__(self, system_path: Optional[Path] = None):
        """Initialize executor with system path."""
        self.system_path = system_path or Path("/home/rasmus/Desktop/sejrliste systemet")
        self._running = False
        self._current_script: Optional[str] = None
        self._output: str = ""
        self._error: str = ""
        self._return_code: Optional[int] = None
        self._last_run: Dict[str, datetime] = {}
        self._output_queue: queue.Queue = queue.Queue()

    @property
    def is_running(self) -> bool:
        """Check if a script is currently running."""
        return self._running

    @property
    def current_script(self) -> Optional[str]:
        """Get name of currently running script."""
        return self._current_script

    def get_output(self) -> str:
        """Get captured stdout from last run."""
        return self._output

    def get_error(self) -> str:
        """Get captured stderr from last run."""
        return self._error

    def get_return_code(self) -> Optional[int]:
        """Get return code from last run."""
        return self._return_code

    def get_last_run(self, script_name: str) -> Optional[datetime]:
        """Get last run timestamp for a script."""
        return self._last_run.get(script_name)

    def get_script_path(self, script_name: str) -> Optional[Path]:
        """Get full path to a script."""
        if script_name not in self.SCRIPTS:
            return None
        relative_path, _ = self.SCRIPTS[script_name]
        return self.system_path / relative_path

    def get_dna_lag(self, script_name: str) -> Optional[int]:
        """Get DNA lag number for a script."""
        if script_name not in self.SCRIPTS:
            return None
        _, dna_lag = self.SCRIPTS[script_name]
        return dna_lag

    def run_script(
        self,
        script_name: str,
        args: Optional[list] = None,
        timeout: int = 30
    ) -> Tuple[bool, str]:
        """
        Run a script synchronously (blocking).

        Args:
            script_name: Name of script (without .py)
            args: Optional list of arguments
            timeout: Timeout in seconds (default 30)

        Returns:
            Tuple of (success: bool, output: str)
        """
        script_path = self.get_script_path(script_name)
        if not script_path:
            return False, f"Unknown script: {script_name}"

        if not script_path.exists():
            return False, f"Script not found: {script_path}"

        # Build command
        cmd = ["python3", str(script_path)]
        if args:
            cmd.extend(args)

        self._running = True
        self._current_script = script_name
        self._output = ""
        self._error = ""
        self._return_code = None

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.system_path)
            )

            self._output = result.stdout
            self._error = result.stderr
            self._return_code = result.returncode
            self._last_run[script_name] = datetime.now()

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, f"Exit code {result.returncode}: {result.stderr}"

        except subprocess.TimeoutExpired:
            self._error = f"Timeout after {timeout} seconds"
            return False, f"Script timed out after {timeout}s"

        except PermissionError as e:
            self._error = f"Permission denied: {e}"
            return False, f"Permission denied: Cannot execute {script_path}"

        except FileNotFoundError as e:
            self._error = f"File not found: {e}"
            return False, f"Python interpreter not found or script missing"

        except Exception as e:
            self._error = str(e)
            return False, f"Error: {e}"

        finally:
            self._running = False
            self._current_script = None

    def run_script_async(
        self,
        script_name: str,
        args: Optional[list] = None,
        timeout: int = 30,
        callback: Optional[callable] = None
    ) -> threading.Thread:
        """
        Run a script asynchronously (non-blocking).

        Args:
            script_name: Name of script (without .py)
            args: Optional list of arguments
            timeout: Timeout in seconds
            callback: Optional callback(success, output) when done

        Returns:
            Thread object (already started)
        """
        def _run():
            success, output = self.run_script(script_name, args, timeout)
            if callback:
                callback(success, output)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        return thread

    def format_output(self, include_error: bool = True) -> str:
        """Format last run output for display."""
        lines = []

        if self._output:
            lines.append("=== OUTPUT ===")
            lines.append(self._output.strip())

        if include_error and self._error:
            lines.append("=== ERROR ===")
            lines.append(self._error.strip())

        if self._return_code is not None:
            lines.append(f"=== EXIT CODE: {self._return_code} ===")

        return "\n".join(lines) if lines else "(no output)"

    def get_all_scripts(self) -> Dict[str, Dict[str, Any]]:
        """Get info about all available scripts."""
        result = {}
        for name, (path, dna_lag) in self.SCRIPTS.items():
            full_path = self.system_path / path
            result[name] = {
                "path": str(full_path),
                "exists": full_path.exists(),
                "dna_lag": dna_lag,
                "last_run": self._last_run.get(name),
            }
        return result


# ============================================================================
# Convenience functions for direct use
# ============================================================================

_default_executor: Optional[ScriptExecutor] = None

def get_executor(system_path: Optional[Path] = None) -> ScriptExecutor:
    """Get or create the default executor instance."""
    global _default_executor
    if _default_executor is None or system_path:
        _default_executor = ScriptExecutor(system_path)
    return _default_executor


def run_verify(args: Optional[list] = None) -> Tuple[bool, str]:
    """Run auto_verify.py."""
    return get_executor().run_script("auto_verify", args or ["--all"])


def run_archive(sejr_name: str) -> Tuple[bool, str]:
    """Run auto_archive.py for a specific sejr."""
    return get_executor().run_script("auto_archive", ["--sejr", sejr_name])


def run_predict() -> Tuple[bool, str]:
    """Run auto_predict.py."""
    return get_executor().run_script("auto_predict")


def run_learn() -> Tuple[bool, str]:
    """Run auto_learn.py."""
    return get_executor().run_script("auto_learn")


def run_track() -> Tuple[bool, str]:
    """Run auto_track.py."""
    return get_executor().run_script("auto_track")


def run_generate(name: str) -> Tuple[bool, str]:
    """Run generate_sejr.py with name."""
    return get_executor().run_script("generate_sejr", ["--name", name])


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Testing ScriptExecutor...")

    executor = ScriptExecutor()

    # List all scripts
    print("\nAvailable scripts:")
    for name, info in executor.get_all_scripts().items():
        status = "OK" if info["exists"] else "MISSING"
        print(f"  [{status}] {name} (DNA Lag {info['dna_lag']})")

    # Test run
    print("\nRunning auto_verify --help...")
    success, output = executor.run_script("auto_verify", ["--help"])
    print(f"Success: {success}")
    print(f"Output preview: {output[:200]}..." if len(output) > 200 else f"Output: {output}")

    print("\nScriptExecutor test complete!")
