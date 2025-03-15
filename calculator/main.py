#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__" and __package__ is None:
    # Insert repository root (parent directory of "calculator") into sys.path.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Re-run this module as a package.
    os.execvp(sys.executable, [sys.executable, "-m", "calculator.main"])

# pylint: disable=wrong-import-position
from calculator.repl import REPL

def main():
    repl = REPL()
    repl.start()

if __name__ == "__main__":
    main()
