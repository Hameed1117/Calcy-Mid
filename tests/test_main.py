"""
test_main.py
Tests for the main entry point of the calculator.
"""

import pytest
from calculator.main import main

def test_main_exit(monkeypatch, capsys):
    """
    Test the main entry point by simulating user input of 'exit'.
    This ensures coverage of lines in main.py.
    """
    # Provide a single 'exit' input so the REPL will quit immediately.
    monkeypatch.setattr("builtins.input", lambda prompt="": "exit")
    with pytest.raises(SystemExit) as excinfo:
        main()
    output = capsys.readouterr().out
    # Check for the REPL welcome message
    assert "Welcome to the Advanced Calculator REPL!" in output
    assert excinfo.value.code == 0
