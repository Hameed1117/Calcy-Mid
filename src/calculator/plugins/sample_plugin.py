"""
sample_plugin.py
An example plugin demonstrating a dynamically loaded command.
"""

from ..logger import LoggerSingleton

logger = LoggerSingleton.get_logger()

class PluginCommand:
    """
    Example plugin command for demonstration.
    """

    def __init__(self):
        self.command_name = "sample_plugin"

    def execute(self):
        logger.info("Executing sample_plugin command!")
        logger.info("You just ran the Sample Plugin Command!")
