"""
exceptions.py
Custom exceptions used by the calculator.
"""

class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass

class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""
    pass
