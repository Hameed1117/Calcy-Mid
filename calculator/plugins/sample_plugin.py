"""
sample_plugin.py
An example plugin demonstrating a dynamically loaded command.
"""

from calculator.logger import LoggerSingleton

logger = LoggerSingleton.get_logger()

class PluginCommand:
    """
    Example plugin command.
    """
    def __init__(self):
        self.command_name = "sample_plugin"

    def execute(self):
        logger.info("Executing sample_plugin command!")
        print("You just ran the Sample Plugin Command!")
