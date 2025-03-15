"""
test_repl.py
Tests for the REPL functionality.

We disable 'redefined-outer-name' because Pytest fixtures
commonly share names with local test parameters.
"""

# pylint: disable=redefined-outer-name

import pytest
from calculator.repl import REPL

@pytest.fixture
def make_fresh_repl(tmp_path):
    """
    Creates a new REPL object and ensures a completely empty state
    by clearing and deleting any existing default CSV in 'history/history.csv'.
    We also set a new path so that we don't interfere with real data.
    """
    repl_instance = REPL()
    repl_instance.calculator.history.clear_history()
    repl_instance.calculator.history.delete_history_file()
    repl_instance.calculator.history.filename = str(tmp_path / "test_history.csv")
    return repl_instance

def test_cmd_exit():
    repl_inst = REPL()
    with pytest.raises(SystemExit) as e_info:
        repl_inst.cmd_exit([])
    assert e_info.value.code == 0

def test_cmd_menu(make_fresh_repl, capsys):
    make_fresh_repl.cmd_menu([])
    output = capsys.readouterr().out
    assert "MENU:" in output or "Available Calculator Commands" in output

def test_cmd_usage(make_fresh_repl, capsys):
    make_fresh_repl.cmd_usage([])
    output = capsys.readouterr().out
    assert "USAGE:" in output or "How to Use the Calculator" in output

def test_cmd_history_empty(make_fresh_repl, capsys):
    make_fresh_repl.cmd_history([])
    output = capsys.readouterr().out
    assert "Empty DataFrame" in output or "Columns:" in output or "[]" in output

def test_cmd_save_and_load_history(make_fresh_repl):
    make_fresh_repl.calculator.history.add_record("mul", 2, 3, 6)
    make_fresh_repl.cmd_save_history([])
    make_fresh_repl.cmd_clear_history([])
    assert make_fresh_repl.calculator.history.get_history().empty
    make_fresh_repl.cmd_load_history([])
    df = make_fresh_repl.calculator.history.get_history()
    assert not df.empty
    assert df.iloc[0]["operation"] == "mul"

def test_handle_special_command_valid(make_fresh_repl, capsys):
    result = make_fresh_repl.handle_special_command("menu", [])
    assert result is True
    out = capsys.readouterr().out
    assert "MENU:" in out or "Available Calculator Commands" in out

def test_handle_special_command_invalid(make_fresh_repl):
    result = make_fresh_repl.handle_special_command("unknown", [])
    assert result is False

def test_handle_plugin_command_valid(make_fresh_repl, capsys):
    class DummyPlugin:
        def __init__(self):
            self.command_name = "dummy"
        def execute(self):
            print("Dummy plugin executed.")

    make_fresh_repl.plugins["dummy"] = DummyPlugin()
    result = make_fresh_repl.handle_plugin_command("dummy")
    assert result is True
    out = capsys.readouterr().out
    assert "Dummy plugin executed." in out

def test_handle_plugin_command_invalid(make_fresh_repl):
    result = make_fresh_repl.handle_plugin_command("nonexistent")
    assert result is False

def test_handle_arithmetic_command_valid(make_fresh_repl, capsys):
    result = make_fresh_repl.handle_arithmetic_command("add", ["add", "2", "3"])
    assert result is True
    out = capsys.readouterr().out
    assert "Result:" in out and "5" in out

def test_handle_arithmetic_command_invalid_args(make_fresh_repl, capsys):
    result = make_fresh_repl.handle_arithmetic_command("add", ["add", "2"])
    assert result is True
    out = capsys.readouterr().out.lower()
    assert "requires 2 numeric argument" in out

def test_handle_arithmetic_command_invalid_input(make_fresh_repl, capsys):
    result = make_fresh_repl.handle_arithmetic_command("add", ["add", "two", "three"])
    assert result is True
    out = capsys.readouterr().out.lower()
    assert "error:" in out or "valid numeric" in out

def test_arithmetic_command_error(make_fresh_repl, capsys):
    """
    Force an exception by mocking calculator.perform_operation
    to raise an exception, ensuring we cover the broad-exception-caught path.
    """
    def mock_perform_op(_cmd, _a, _b):
        raise ValueError("Forced error.")
    make_fresh_repl.calculator.perform_operation = mock_perform_op
    make_fresh_repl.handle_arithmetic_command("add", ["add", "1", "2"])
    out = capsys.readouterr().out.lower()
    assert "error:" in out

def test_start_method_sequence(monkeypatch, capsys):
    inputs = iter(["menu", "usage", "add 2 3", "foobar", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    new_repl = REPL()
    with pytest.raises(SystemExit):
        new_repl.start()
    output = capsys.readouterr().out
    assert "MENU:" in output or "Available Calculator Commands" in output
    assert "USAGE:" in output or "How to Use the Calculator" in output
    assert "Result:" in output and "5" in output
    assert "Unknown command:" in output

def test_plugin_directory_not_found(monkeypatch, tmp_path):
    """
    Force the 'plugins' directory to not exist by mocking os.path.isdir
    so we cover lines that log a warning for missing plugin dir.
    """
    def mock_isdir(_path):
        return False

    monkeypatch.setattr("os.path.isdir", mock_isdir)
    monkeypatch.setattr("os.path.dirname", lambda _: str(tmp_path))

    repl_missing = REPL()
    # Confirm no crash and no plugins
    assert len(repl_missing.plugins) == 0

def test_plugin_load_error(monkeypatch):
    """
    Force an import error while loading plugins to cover the
    'Failed to load plugin' path.
    """
    def mock_import(_name):
        raise ImportError("Forced plugin import error")

    monkeypatch.setattr("importlib.import_module", mock_import)
    new_repl = REPL()
    # Confirm no crash
    assert len(new_repl.plugins) == 0
