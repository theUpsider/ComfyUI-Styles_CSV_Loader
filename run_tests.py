#!/usr/bin/env python3
"""
Simple test runner script for ComfyUI-Styles_CSV_Loader
Usage: python run_tests.py [--coverage]
"""
import sys
import subprocess
import os

def main():
    """Run tests with optional coverage reporting."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    base_cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    
    if "--coverage" in sys.argv:
        base_cmd.extend(["--cov=.", "--cov-report=term-missing", "--cov-report=html"])
        print("Running tests with coverage...")
    else:
        print("Running tests...")
    
    try:
        result = subprocess.run(base_cmd, check=True)
        print("\n✅ All tests passed!")
        if "--coverage" in sys.argv:
            print("📊 Coverage report generated in htmlcov/")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    sys.exit(main())