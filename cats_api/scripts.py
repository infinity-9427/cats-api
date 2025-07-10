"""Custom test scripts for the Cats API project."""

import subprocess
import sys
import os


def run_tests():
    """Run full test suite with coverage."""
    print("🧪 Running Cats API Tests (Full Suite)...")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/", 
        "--cov=app", 
        "--cov-report=term-missing"
    ]
    
    result = subprocess.run(cmd, cwd=os.getcwd())
    
    if result.returncode == 0:
        print("✅ Tests complete - workspace clean!")
    else:
        print("❌ Tests failed!")
        sys.exit(1)


def run_quick_tests():
    """Run tests without coverage for speed."""
    print("⚡ Running Quick Tests...")
    
    cmd = [sys.executable, "-m", "pytest", "tests/", "-q"]
    
    result = subprocess.run(cmd, cwd=os.getcwd())
    
    if result.returncode == 0:
        print("✅ Quick tests complete!")
    else:
        print("❌ Tests failed!")
        sys.exit(1)


def run_coverage_tests():
    """Run tests with detailed coverage report."""
    print("📊 Running Tests with Detailed Coverage...")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/", 
        "--cov=app", 
        "--cov-report=term-missing",
        "--cov-report=term:skip-covered",
        "-v"
    ]
    
    result = subprocess.run(cmd, cwd=os.getcwd())
    
    if result.returncode == 0:
        print("✅ Coverage tests complete!")
    else:
        print("❌ Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
