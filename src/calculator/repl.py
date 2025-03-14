"""
repl.py
An updated Read-Eval-Print Loop (REPL) with minimal if/else usage.
Uses dictionary-based dispatch for special commands and arithmetic commands.
"""

import sys
import os
import importlib

from main_logic import CalculatorApp
from logger import LoggerSingleton

logger = LoggerSingleton.get_logger()

class REPL:
    """
    The REPL (Read-Eval-Print Loop) class for interacting with the CalculatorApp.
    Minimizes if/elif usage by using dictionaries to dispatch commands.
    """

    def __init__(self):
        # The main calculator logic, which uses the CommandFactory & history facade
        self.calculator = CalculatorApp()
        
        # Dynamically loaded plugins
        self.plugins = {}
        
        # Define "special commands" that do not require numeric operands
        self.special_commands = {
            "exit": self.cmd_exit,
            "menu": self.cmd_menu,
            "usage": self.cmd_usage,
            "history": self.cmd_history,
            "clear_history": self.cmd_clear_history,
            "delete_history_file": self.cmd_delete_history_file,
            "save_history": self.cmd_save_history,
            "load_history": self.cmd_load_history
        }

        # Load plugins automatically
        self.load_plugins()

        # Define how many operands each arithmetic command requires
        # We'll use a single function to handle execution, but this dictionary
        # helps us parse the correct number of arguments from user input.
        self.arithmetic_cmds = {
            "add": 2,
            "sub": 2,
            "mul": 2,
            "div": 2,
            "sqrt": 1,
            "square": 1,
            "cube": 1,
            "log": 1
        }

    def load_plugins(self):
        """
        Dynamically load plugin modules from the 'plugins' directory.
        Each plugin is expected to have a class named 'PluginCommand'.
        """
        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
        if not os.path.isdir(plugins_dir):
            logger.warning("Plugins directory not found.")
            return

        for file in os.listdir(plugins_dir):
            if file.endswith(".py") and file != "__init__.py":
                plugin_name = file[:-3]
                try:
                    module = importlib.import_module(f"calculator.plugins.{plugin_name}")
                    plugin_class = getattr(module, "PluginCommand", None)
                    if plugin_class:
                        instance = plugin_class()
                        self.plugins[instance.command_name] = instance
                        logger.info("Plugin loaded: %s", instance.command_name)
                except Exception as exc:
                    logger.error("Failed to load plugin %s: %s", plugin_name, exc, exc_info=True)

    # -------------------------------------------------------------------------
    #  SPECIAL COMMAND HANDLERS (No arithmetic, just controlling the REPL)
    # -------------------------------------------------------------------------
    def cmd_exit(self, parts):
        """Exit the calculator."""
        print("Exiting the calculator. Goodbye!")
        sys.exit(0)

    def cmd_menu(self, parts):
        """Show available commands."""
        self.show_menu()

    def cmd_usage(self, parts):
        """Show usage instructions."""
        self.show_usage()

    def cmd_history(self, parts):
        """Show the calculation history."""
        print(self.calculator.history.get_history())

    def cmd_clear_history(self, parts):
        """Clear in-memory history."""
        self.calculator.history.clear_history()
        print("History cleared in memory.")

    def cmd_delete_history_file(self, parts):
        """Delete the CSV history file from disk."""
        self.calculator.history.delete_history_file()
        print("History file deleted.")

    def cmd_save_history(self, parts):
        """Save the history DataFrame to CSV."""
        self.calculator.history.save_history()
        print("History saved to file.")

    def cmd_load_history(self, parts):
        """Load history from CSV if available."""
        self.calculator.history.load_history()
        print("History loaded from file.")

    # -------------------------------------------------------------------------
    #  DISPLAY METHODS
    # -------------------------------------------------------------------------
    def show_menu(self):
        """
        Display a list of commands (basic, advanced, plugin, special).
        """
        print("\n--- MENU: Available Calculator Commands ---")
        print("Basic Commands (2 numbers):")
        print("  add, sub, mul, div")

        print("\nAdvanced Commands (1 number):")
        print("  sqrt, square, cube, log")

        plugin_commands = list(self.plugins.keys())
        if plugin_commands:
            print("\nPlugin Commands:")
            for cmd_name in plugin_commands:
                print(f"  {cmd_name}")

        print("\nSpecial Commands:")
        print("  history, clear_history, delete_history_file, save_history, load_history")
        print("  menu, usage, exit\n")

    def show_usage(self):
        """
        Display usage instructions for all commands.
        """
        print("\n--- USAGE: How to Use the Calculator ---")
        print("1) For two-operand commands (add, sub, mul, div):")
        print("      Example: 'add 2 3'")
        print("2) For single-operand commands (sqrt, square, cube, log):")
        print("      Example: 'sqrt 16'")
        print("3) For special commands: 'menu' (shows menu), 'usage' (this text), 'exit' (quit).")
        print("4) For plugin commands, just type the plugin command. Example: 'sample_plugin'.\n")

    # -------------------------------------------------------------------------
    #  MAIN REPL LOOP
    # -------------------------------------------------------------------------
    def start(self):
        """
        Start the REPL loop.
        """
        print("Welcome to the Advanced Calculator REPL!")
        print("Type 'menu' to see available commands, 'usage' for instructions, or 'exit' to quit.\n")

        while True:
            user_input = input(">> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            cmd = parts[0].lower()

            if self.handle_special_command(cmd, parts):
                continue
            if self.handle_plugin_command(cmd):
                continue
            if self.handle_arithmetic_command(cmd, parts):
                continue

            print(f"Unknown command: {cmd}. Type 'menu' to see available commands.")

    def handle_special_command(self, cmd, parts):
        if cmd in self.special_commands:
            self.special_commands[cmd](parts)
            return True
        return False

    def handle_plugin_command(self, cmd):
        if cmd in self.plugins:
            self.plugins[cmd].execute()
            return True
        return False

    def handle_arithmetic_command(self, cmd, parts):
        if cmd in self.arithmetic_cmds:
            required_args = self.arithmetic_cmds[cmd]
            if len(parts) - 1 < required_args:
                print(f"Error: '{cmd}' requires {required_args} numeric argument(s).")
                return True
            
            try:
                if required_args == 2:
                    a, b = float(parts[1]), float(parts[2])
                else:
                    a, b = float(parts[1]), 0

                result = self.calculator.perform_operation(cmd, a, b)
                if result is not None:
                    print(f"Result: {result}")
                else:
                    print(f"Unknown operation or error occurred.")
            except ValueError:
                print("Error: Please provide valid numeric input(s).")
            except Exception as exc:
                print(f"Error: {exc}")
            return True
        return False
