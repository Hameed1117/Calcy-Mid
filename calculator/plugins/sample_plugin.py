"""
sample_plugin.py
An example plugin demonstrating a dynamically loaded command.
"""

from calculator.logger import LoggerSingleton

LOGGER = LoggerSingleton.get_logger()

class PluginCommand:
    """
    Example plugin command for demonstration.
    """
    def __init__(self):
        self.command_name = "sample_plugin"

    def execute(self):
        LOGGER.info("Executing sample_plugin command!")
        print("You just ran the Sample Plugin Command!")
