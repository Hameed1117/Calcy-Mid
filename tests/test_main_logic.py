"""
test_main_logic.py
Additional tests for the main_logic module.
"""

from calculator.main_logic import CalculatorApp

def test_unsupported_operation():
    app = CalculatorApp()
    # When an unsupported operation is requested, perform_operation should return None.
    result = app.perform_operation("nonexistent", 1, 2)
    assert result is None
