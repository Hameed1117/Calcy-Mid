"""
main_logic.py
Core 'CalculatorApp' that creates and executes commands, 
and interacts with HistoryFacade for persistent storage.
"""

from commands import (
    AddCommand, SubCommand, MulCommand, DivCommand,
    SqrtCommand, SquareCommand, CubeCommand, LogCommand
)
from history_facade import HistoryFacade
from logger import LoggerSingleton

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
    - Manages the history via HistoryFacade
    - Uses CommandFactory to instantiate the correct operation
    """

    def __init__(self, history_file="history.csv"):
        self.history = HistoryFacade(filename=history_file)
        self.history.load_history()

    def perform_operation(self, operation, a, b):
        """
        Instantiate the command object for `operation`, execute,
        record the result, and return it.
        """
        logger.info(f"Performing operation: {operation} with arguments {a} and {b}")
        cmd = CommandFactory.get_command(operation)
        if not cmd:
            logger.error(f"Invalid operation: {operation}")
            return None
        result = cmd.execute(a, b)
        logger.info(f"Operation result: {result}")
        self.history.add_record(operation, a, b, result)
        return result
