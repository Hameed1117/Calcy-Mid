"""
main_logic.py
Core CalculatorApp that creates and executes commands,
and interacts with HistoryFacade for persistent storage.

Design Patterns Used:
- Command Pattern: Each arithmetic operation is encapsulated in a Command class.
- Factory Pattern: CommandFactory instantiates command objects based on the operation.
- Facade Pattern: HistoryFacade simplifies interactions with the Pandas DataFrame.
- Singleton Pattern: LoggerSingleton ensures one logger instance.
"""

from .commands import (
    AddCommand, SubCommand, MulCommand, DivCommand,
    SqrtCommand, SquareCommand, CubeCommand, LogCommand
)
from .history_facade import HistoryFacade
from .logger import LoggerSingleton

logger = LoggerSingleton.get_logger()

class CommandFactory:
    """Factory to create operation command objects."""
    operation_map = {
        "add": AddCommand(),
        "sub": SubCommand(),
        "mul": MulCommand(),
        "div": DivCommand(),
        "sqrt": SqrtCommand(),
        "square": SquareCommand(),
        "cube": CubeCommand(),
        "log": LogCommand()
    }

    @staticmethod
    def get_command(operation: str):
        cmd_obj = CommandFactory.operation_map.get(operation)
        if not cmd_obj:
            logger.error("Unknown operation requested: %s", operation)
        return cmd_obj

class CalculatorApp:
    """
    Main Calculator application class.
    - Uses the CommandFactory to get the appropriate command (Command Pattern)
    - Manages history through HistoryFacade (Facade Pattern)
    """
    def __init__(self, history_file="history.csv"):
        self.history = HistoryFacade(filename=history_file)
        self.history.load_history()

    def perform_operation(self, operation, a, b):
        """
        Instantiate the command object for `operation`, execute it,
        record the result, and return it.
        Demonstrates EAFP (try/except for conversion/execution)
        """
        logger.info("Performing operation: %s with arguments %s and %s", operation, a, b)
        cmd = CommandFactory.get_command(operation)
        if not cmd:
            logger.error("Invalid operation: %s", operation)
            return None
        try:
            result = cmd.execute(a, b)
        except Exception as exc:
            logger.error("Error during execution of %s: %s", operation, exc)
            raise exc
        logger.info("Operation result: %s", result)
        self.history.add_record(operation, a, b, result)
        return result
