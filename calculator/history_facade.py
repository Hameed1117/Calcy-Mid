"""
history_facade.py
A Facade for Pandas-based history management.
"""

import os
import pandas as pd
from calculator.logger import LoggerSingleton

LOGGER = LoggerSingleton.get_logger()

class HistoryFacade:
    """
    Provides a simplified interface to read/write history
    from a CSV file using Pandas.
    The history file is stored in the "history" folder.
    """
    def __init__(self, filename="history/history.csv"):
        self.filename = filename
        # Ensure the directory exists.
        dir_name = os.path.dirname(self.filename)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        self._history_df = pd.DataFrame(
            columns=["operation", "operand1", "operand2", "result"]
        )

    def load_history(self):
        """Load history from CSV if file exists."""
        try:
            if os.path.exists(self.filename):
                self._history_df = pd.read_csv(self.filename)
                LOGGER.info("History loaded from %s", self.filename)
            else:
                LOGGER.warning("No history file found at %s. Using empty history.", self.filename)
        except (IOError, PermissionError) as e:
            LOGGER.error("Error loading history: %s", str(e))

    def save_history(self):
        """Save the in-memory history DataFrame to CSV."""
        try:
            self._history_df.to_csv(self.filename, index=False)
            LOGGER.info("History saved to %s", self.filename)
        except (IOError, PermissionError) as e:
            LOGGER.error("Error saving history: %s", str(e))

    def clear_history(self):
        """Clear in-memory history (does not remove file)."""
        self._history_df = pd.DataFrame(
            columns=["operation", "operand1", "operand2", "result"]
        )
        LOGGER.info("History cleared in memory.")

    def delete_history_file(self):
        """Delete the CSV file from disk."""
        if os.path.exists(self.filename):
            os.remove(self.filename)
            LOGGER.info("History file %s deleted.", self.filename)
        else:
            LOGGER.warning("No history file found to delete at %s", self.filename)

    def add_record(self, operation, operand1, operand2, result):
        """Append a record to the in-memory DataFrame."""
        new_record = {
            "operation": operation,
            "operand1": operand1,
            "operand2": operand2,
            "result": result
        }
        # Create a DataFrame with explicit columns to avoid FutureWarning.
        new_df = pd.DataFrame([new_record], columns=self._history_df.columns)
        self._history_df = pd.concat([self._history_df, new_df], ignore_index=True)
        LOGGER.info("Record added: %s", new_record)

    def get_history(self):
        """Return the current DataFrame of history."""
        return self._history_df
