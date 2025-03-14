"""
main_logic.py
Core CalculatorApp that creates and executes commands,
and interacts with HistoryFacade for persistent storage.

Design Patterns Used:
- Command Pattern: Each operation is encapsulated in its own Command class.
- Factory Pattern: CommandFactory returns the correct command.
- Facade Pattern: HistoryFacade hides Pandas operations.
- Singleton Pattern: LoggerSingleton provides a global logger.
"""

from calculator.commands import AddCommand, SubCommand, MulCommand, DivCommand, SqrtCommand, SquareCommand, CubeCommand, LogCommand
from calculator.history_facade import HistoryFacade
from calculator.logger import LoggerSingleton

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
    Uses CommandFactory to execute the proper command and manages history via HistoryFacade.
    """
    def __init__(self, history_file="history.csv"):
        self.history = HistoryFacade(filename=history_file)
        self.history.load_history()

    def perform_operation(self, operation, a, b):
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
