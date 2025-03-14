"""
history_facade.py
A Facade for Pandas-based history management.
"""

import os
import pandas as pd
from .logger import LoggerSingleton

logger = LoggerSingleton.get_logger()

class HistoryFacade:
    """
    Provides a simplified interface to read/write history
    from a CSV file using Pandas.
    """

    def __init__(self, filename="history.csv"):
        self.filename = filename
        self._history_df = pd.DataFrame(columns=["operation", "operand1", "operand2", "result"])

    def load_history(self):
        """Load history from CSV if file exists."""
        try:
            if os.path.exists(self.filename):
                self._history_df = pd.read_csv(self.filename)
                logger.info("History loaded from %s", self.filename)
            else:
                logger.warning("No history file found at %s. Using empty history.", self.filename)
        except (IOError, PermissionError) as e:
            logger.error("Error loading history: %s", str(e))

    def save_history(self):
        """Save the in-memory history DataFrame to CSV."""
        try:
            self._history_df.to_csv(self.filename, index=False)
            logger.info("History saved to %s", self.filename)
        except (IOError, PermissionError) as e:
            logger.error("Error saving history: %s", str(e))

    def clear_history(self):
        """Clear in-memory history (does not remove file)."""
        self._history_df = pd.DataFrame(columns=["operation", "operand1", "operand2", "result"])
        logger.info("History cleared in memory.")

    def delete_history_file(self):
        """Delete the CSV file from disk."""
        if os.path.exists(self.filename):
            os.remove(self.filename)
            logger.info("History file %s deleted.", self.filename)
        else:
            logger.warning("No history file found to delete at %s", self.filename)

    def add_record(self, operation, operand1, operand2, result):
        """Append a record to the in-memory DataFrame."""
        new_record = {
            "operation": operation,
            "operand1": operand1,
            "operand2": operand2,
            "result": result
        }
        self._history_df = pd.concat([self._history_df, pd.DataFrame([new_record])], ignore_index=True)
        logger.info("Record added: %s", new_record)

    def get_history(self):
        """Return the current DataFrame of history."""
        return self._history_df
