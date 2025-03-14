"""
test_calculator.py
Tests for basic and advanced operations through the CalculatorApp.
"""

import pytest
from calculator.main_logic import CalculatorApp
from calculator.exceptions import DivisionByZeroError

def test_add_two_positive_numbers():
    calc = CalculatorApp()
    result = calc.perform_operation("add", 2, 3)
    assert result == 5

def test_subtract_smaller_from_larger():
    calc = CalculatorApp()
    result = calc.perform_operation("sub", 5, 2)
    assert result == 3

def test_multiply_two_positive_integers():
    calc = CalculatorApp()
    result = calc.perform_operation("mul", 3, 4)
    assert result == 12

def test_div():
    calc = CalculatorApp()
    result = calc.perform_operation("div", 10, 2)
    assert result == 5

def test_div_by_zero():
    calc = CalculatorApp()
    with pytest.raises(DivisionByZeroError):
        calc.perform_operation("div", 5, 0)

def test_sqrt():
    calc = CalculatorApp()
    result = calc.perform_operation("sqrt", 16, 0)
    assert result == 4

def test_sqrt_negative():
    calc = CalculatorApp()
    with pytest.raises(ValueError):
        calc.perform_operation("sqrt", -9, 0)

def test_square():
    calc = CalculatorApp()
    result = calc.perform_operation("square", 5, 0)
    assert result == 25

def test_cube():
    calc = CalculatorApp()
    result = calc.perform_operation("cube", 3, 0)
    assert result == 27

def test_log():
    calc = CalculatorApp()
    result = calc.perform_operation("log", 100, 0)
    assert pytest.approx(result, 0.0001) == 2

def test_log_non_positive():
    calc = CalculatorApp()
    with pytest.raises(ValueError):
        calc.perform_operation("log", 0, 0)
