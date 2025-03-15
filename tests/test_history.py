"""
test_history.py
Tests the HistoryFacade's ability to save, load, clear, and delete CSV files.
"""

import pandas as pd
from calculator.history_facade import HistoryFacade

def test_load_history(tmp_path):
    fake_csv = tmp_path / "history.csv"
    data = "operation,operand1,operand2,result\nadd,2,3,5"
    fake_csv.write_text(data, encoding="utf-8")
    hist = HistoryFacade(filename=str(fake_csv))
    hist.load_history()
    df = hist.get_history()
    assert len(df) == 1
    assert df.loc[0, "operation"] == "add"
    assert df.loc[0, "result"] == 5

def test_save_history(tmp_path):
    fake_csv = tmp_path / "history.csv"
    hist = HistoryFacade(filename=str(fake_csv))
    hist.add_record("sub", 5, 3, 2)
    hist.save_history()
    assert fake_csv.exists()
    loaded_df = pd.read_csv(fake_csv)
    assert len(loaded_df) == 1
    assert loaded_df.loc[0, "operation"] == "sub"

def test_clear_history():
    hist = HistoryFacade(filename="test_clear.csv")
    hist.add_record("mul", 3, 4, 12)
    hist.clear_history()
    df = hist.get_history()
    assert len(df) == 0

def test_delete_history_file(tmp_path):
    fake_csv = tmp_path / "history.csv"
    hist = HistoryFacade(filename=str(fake_csv))
    hist.add_record("div", 10, 5, 2)
    hist.save_history()
    assert fake_csv.exists()
    hist.delete_history_file()
    assert not fake_csv.exists()
