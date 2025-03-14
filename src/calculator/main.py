"""
main.py - Entrypoint to launch the Advanced Calculator.
Run: python -m src.calculator.main
"""

from repl import REPL

def main():
    repl = REPL()
    repl.start()

if __name__ == "__main__":
    main()
