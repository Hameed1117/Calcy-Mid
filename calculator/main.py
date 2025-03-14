#!/usr/bin/env python3
import os
import sys

# If this file is run directly (instead of as a module),
# add the repository root to sys.path and re‑execute it in module mode.
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.execvp(sys.executable, [sys.executable, "-m", "calculator.main"])

from calculator.repl import REPL

def main():
    repl = REPL()
    repl.start()

if __name__ == "__main__":
    main()
