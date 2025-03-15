"""
test_repl.py
Tests basic REPL functionality using mock input.
"""

from unittest.mock import patch
import pytest
from calculator.repl import REPL

def test_repl_exit():
    repl = REPL()
    with patch("builtins.input", side_effect=["exit"]):
        with pytest.raises(SystemExit):
            repl.start()
