#!/usr/bin/env python3
import os
import sys

# If running this file directly (e.g. "python calculator/main.py")
# and not via a package, re-invoke it using the "-m" flag.
if __name__ == "__main__" and __package__ is None:
    # Insert the parent directory (repository root) at the start of sys.path.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Restart the interpreter using the module flag.
    os.execvp(sys.executable, [sys.executable, "-m", "calculator.main"])

from calculator.repl import REPL

def main():
    repl = REPL()
    repl.start()

if __name__ == "__main__":
    main()
