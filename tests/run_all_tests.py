#!/usr/bin/env python
"""
Comprehensive test runner for Amortization Calculator
Runs all unit tests with detailed reporting
"""

import unittest
import sys
import os

# Add tests directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
import test_calculator
import test_gestures


def run_all_tests():
    """Run all test suites and provide summary"""

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test modules
    suite.addTests(loader.loadTestsFromModule(test_calculator))
    suite.addTests(loader.loadTestsFromModule(test_gestures))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
