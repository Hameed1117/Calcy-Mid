"""
commands.py
Command pattern for calculator operations: add, sub, mul, div, sqrt, square, cube, log.
"""

import math
from abc import ABC, abstractmethod
from calculator.exceptions import DivisionByZeroError

class Command(ABC):
    """Abstract base class for any calculator command."""
    @abstractmethod
    def execute(self, a, b):
        pass

class AddCommand(Command):
    """Add two numbers."""
    def execute(self, a, b):
        return a + b

class SubCommand(Command):
    """Subtract b from a."""
    def execute(self, a, b):
        return a - b

class MulCommand(Command):
    """Multiply a by b."""
    def execute(self, a, b):
        return a * b

class DivCommand(Command):
    """Divide a by b."""
    def execute(self, a, b):
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return a / b

class SqrtCommand(Command):
    """Square root of a."""
    def execute(self, a, _):
        if a < 0:
            raise ValueError("Cannot take sqrt of a negative number.")
        return math.sqrt(a)

class SquareCommand(Command):
    """Square of a."""
    def execute(self, a, _):
        return a * a

class CubeCommand(Command):
    """Cube of a."""
    def execute(self, a, _ignored):
        return a ** 3

class LogCommand(Command):
    """Log base 10 of a."""
    def execute(self, a, _ignored):
        if a <= 0:
            raise ValueError("Cannot take log of a non-positive number.")
        return math.log10(a)
