"""
repl.py
A Read-Eval-Print Loop (REPL) for the calculator.
Supports basic arithmetic, special commands, and dynamic plugin commands.
Design Patterns: Command and Plugin.
"""

import sys
import os
import importlib
from calculator.main_logic import CalculatorApp
from calculator.logger import LoggerSingleton

logger = LoggerSingleton.get_logger()

class REPL:
    def __init__(self):
        self.calculator = CalculatorApp()
        self.plugins = {}
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
        self.load_plugins()
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

    # Special command handlers
    def cmd_exit(self, parts):
        print("Exiting the calculator. Goodbye!")
        sys.exit(0)

    def cmd_menu(self, parts):
        self.show_menu()

    def cmd_usage(self, parts):
        self.show_usage()

    def cmd_history(self, parts):
        print(self.calculator.history.get_history())

    def cmd_clear_history(self, parts):
        self.calculator.history.clear_history()
        print("History cleared in memory.")

    def cmd_delete_history_file(self, parts):
        self.calculator.history.delete_history_file()
        print("History file deleted.")

    def cmd_save_history(self, parts):
        self.calculator.history.save_history()
        print("History saved to file.")

    def cmd_load_history(self, parts):
        self.calculator.history.load_history()
        print("History loaded from file.")

    # Display methods
    def show_menu(self):
        print("\n--- MENU: Available Calculator Commands ---")
        print("Basic Commands (2 numbers):")
        print("  add, sub, mul, div")
        print("\nAdvanced Commands (1 number):")
        print("  sqrt, square, cube, log")
        if self.plugins:
            print("\nPlugin Commands:")
            for cmd_name in self.plugins.keys():
                print(f"  {cmd_name}")
        print("\nSpecial Commands:")
        print("  history, clear_history, delete_history_file, save_history, load_history")
        print("  menu, usage, exit\n")

    def show_usage(self):
        print("\n--- USAGE: How to Use the Calculator ---")
        print("1) For two-operand commands (add, sub, mul, div):")
        print("      Example: 'add 2 3'")
        print("2) For single-operand commands (sqrt, square, cube, log):")
        print("      Example: 'sqrt 16'")
        print("3) For special commands: 'menu', 'usage', 'exit'.")
        print("4) For plugin commands, type the command name (e.g. 'sample_plugin').\n")

    def start(self):
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
                    print("Unknown operation or error occurred.")
            except ValueError:
                print("Error: Please provide valid numeric input(s).")
            except Exception as exc:
                print(f"Error: {exc}")
            return True
        return False
