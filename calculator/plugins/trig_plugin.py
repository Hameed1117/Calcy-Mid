"""
trig_plugin.py
A plugin that implements trigonometric functions.
Users can enter a command such as "trig" in the REPL, then
input an operation (e.g., sin, cos, tan, cot, sec, csc) and an angle in degrees.
"""

import math
from calculator.logger import LoggerSingleton

LOGGER = LoggerSingleton.get_logger()

# Disable too-many-branches since it's a single function with multiple ops.
# pylint: disable=too-many-branches

class PluginCommand:
    """
    The trig plugin's main class, implementing trigonometric operations:
    sin, cos, tan, cot, sec, csc.
    The REPL loads plugins by looking for a class named 'PluginCommand'.
    """
    TOLERANCE = 1e-10

    def __init__(self):
        self.command_name = "trig"

    def execute(self):
        """
        Prompt the user for an operation (sin, cos, tan, cot, sec, csc)
        and an angle in degrees, then compute and print the result.
        """
        try:
            user_input = input("Enter trig operation and angle (e.g., sin 30): ").strip()
            if not user_input:
                print("No input provided.")
                return
            parts = user_input.split()
            if len(parts) != 2:
                print("Invalid input. Please enter an operation and an angle (e.g., sin 30).")
                return
            operation, angle_str = parts[0].lower(), parts[1]
            angle_deg = float(angle_str)
            angle_rad = math.radians(angle_deg)
            result = None

            if operation == "sin":
                result = math.sin(angle_rad)
            elif operation == "cos":
                result = math.cos(angle_rad)
            elif operation == "tan":
                result = math.tan(angle_rad)
            elif operation == "cot":
                tan_val = math.tan(angle_rad)
                if abs(tan_val) < self.TOLERANCE:
                    print("Cotangent is undefined for this angle.")
                    return
                result = 1 / tan_val
            elif operation == "sec":
                cos_val = math.cos(angle_rad)
                if abs(cos_val) < self.TOLERANCE:
                    print("Secant is undefined for this angle.")
                    return
                result = 1 / cos_val
            elif operation == "csc":
                sin_val = math.sin(angle_rad)
                if abs(sin_val) < self.TOLERANCE:
                    print("Cosecant is undefined for this angle.")
                    return
                result = 1 / sin_val
            else:
                print(f"Operation '{operation}' is not supported.")
                return

            LOGGER.info("Trig operation: %s, angle: %s degrees, result: %s",
                        operation, angle_deg, result)
            # Format the angle: if it is an integer, print without decimals.
            if angle_deg.is_integer():
                angle_formatted = str(int(angle_deg))
            else:
                angle_formatted = f"{angle_deg:.1f}"
            print(f"{operation}({angle_formatted}°) = {result}")

        except ValueError:
            print("Invalid angle. Please enter a numeric value for the angle.")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            LOGGER.error("Error in trig_plugin: %s", exc, exc_info=True)
            print(f"An error occurred: {exc}")
