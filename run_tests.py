"""Test runner script for the CMS application."""

import pytest
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def run_tests():
    """Run all tests with coverage reporting."""
    args = [
        "-v",                           # Verbose output
        "--tb=short",                   # Short traceback format
        "--disable-warnings",           # Disable pytest warnings
        "-x",                          # Stop on first failure
        "cms/tests/",                  # Test directory
    ]
    
    # Add coverage if pytest-cov is available
    try:
        import pytest_cov
        args.extend([
            "--cov=cms",               # Coverage for cms package
            "--cov-report=term-missing", # Show missing lines
            "--cov-report=html:htmlcov", # HTML report
        ])
    except ImportError:
        print("Note: Install pytest-cov for coverage reporting")
    
    exit_code = pytest.main(args)
    return exit_code


def run_unit_tests():
    """Run only unit tests."""
    args = [
        "-v",
        "--tb=short",
        "--disable-warnings",
        "cms/tests/unit/",
    ]
    
    exit_code = pytest.main(args)
    return exit_code


def run_integration_tests():
    """Run only integration tests."""
    args = [
        "-v",
        "--tb=short", 
        "--disable-warnings",
        "cms/tests/integration/",
    ]
    
    exit_code = pytest.main(args)
    return exit_code


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run CMS tests")
    parser.add_argument(
        "--type",
        choices=["all", "unit", "integration"],
        default="all",
        help="Type of tests to run"
    )
    
    args = parser.parse_args()
    
    if args.type == "unit":
        exit_code = run_unit_tests()
    elif args.type == "integration":
        exit_code = run_integration_tests()
    else:
        exit_code = run_tests()
    
    sys.exit(exit_code)