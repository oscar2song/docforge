# !/usr/bin/env python3
"""Simple test runner for DocForge"""

import subprocess
import sys


def main():
    """Run tests using current Python interpreter."""
    print("🧪 Running DocForge Tests...")

    try:
        subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=True)
        print("✅ All tests passed!")
    except subprocess.CalledProcessError:
        print("❌ Some tests failed")


if __name__ == "__main__":
    main()
