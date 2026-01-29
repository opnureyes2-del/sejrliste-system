#!/usr/bin/env python3
"""
Unit tests for ScriptExecutor.

Run with: python3 -m pytest app/tests/test_executor.py -v
Or simply: python3 app/tests/test_executor.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.executor import ScriptExecutor, get_executor


def test_script_executor_init():
    """Test 1: ScriptExecutor initializes correctly."""
    executor = ScriptExecutor()

    assert executor is not None
    assert executor.system_path.exists()
    assert not executor.is_running
    assert executor.current_script is None
    assert len(executor.SCRIPTS) == 6

    print("[OK] Test 1 PASSED: ScriptExecutor initializes correctly")
    return True


def test_script_paths_exist():
    """Test 2: All script paths exist."""
    executor = ScriptExecutor()
    all_scripts = executor.get_all_scripts()

    missing = []
    for name, info in all_scripts.items():
        if not info["exists"]:
            missing.append(name)

    if missing:
        print(f"[FAIL] Test 2 FAILED: Missing scripts: {missing}")
        return False

    print(f"[OK] Test 2 PASSED: All {len(all_scripts)} scripts exist")
    return True


def test_run_script_with_help():
    """Test 3: run_script works with --help flag."""
    executor = ScriptExecutor()

    success, output = executor.run_script("auto_verify", ["--help"])

    # --help should always succeed
    assert success is True or "usage" in output.lower() or "help" in output.lower()
    assert len(output) > 0

    print(f"[OK] Test 3 PASSED: run_script returns output (got {len(output)} chars)")
    return True


def test_unknown_script_fails():
    """Test 4 (bonus): Unknown script returns error."""
    executor = ScriptExecutor()

    success, output = executor.run_script("nonexistent_script")

    assert success is False
    assert "unknown" in output.lower() or "not found" in output.lower()

    print("[OK] Test 4 PASSED: Unknown script fails gracefully")
    return True


def test_dna_lag_mapping():
    """Test 5 (bonus): DNA lag mapping is correct."""
    executor = ScriptExecutor()

    expected_lags = {
        "auto_track": 2,
        "auto_verify": 3,
        "auto_learn": 4,
        "auto_archive": 5,
        "auto_predict": 6,
        "generate_sejr": 7,
    }

    for script_name, expected_lag in expected_lags.items():
        actual_lag = executor.get_dna_lag(script_name)
        assert actual_lag == expected_lag, f"{script_name}: expected {expected_lag}, got {actual_lag}"

    print("[OK] Test 5 PASSED: DNA lag mapping is correct")
    return True


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("EXECUTOR UNIT TESTS")
    print("=" * 60)

    tests = [
        test_script_executor_init,
        test_script_paths_exist,
        test_run_script_with_help,
        test_unknown_script_fails,
        test_dna_lag_mapping,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__} FAILED with exception: {e}")
            failed += 1

    print("=" * 60)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
