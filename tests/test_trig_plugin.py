"""
test_trig_plugin.py
Tests for the trigonometry plugin.
"""

import math
from calculator.plugins.trig_plugin import PluginCommand

def run_trig_test(monkeypatch, capsys, user_input):
    monkeypatch.setattr('builtins.input', lambda prompt='': user_input)
    plugin = PluginCommand()
    plugin.execute()
    return capsys.readouterr().out.strip()

def extract_result(output):
    # Expected output format: "operation(angle°) = result"
    try:
        result_str = output.split('=')[-1].strip()
        return float(result_str)
    except (IndexError, ValueError):
        return None

def test_trig_sin(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "sin 30")
    assert "sin(30°)" in output
    result = extract_result(output)
    expected = math.sin(math.radians(30))
    assert result is not None and abs(result - expected) < 1e-6

def test_trig_cos(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "cos 60")
    assert "cos(60°)" in output
    result = extract_result(output)
    expected = math.cos(math.radians(60))
    assert result is not None and abs(result - expected) < 1e-6

def test_trig_tan(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "tan 45")
    assert "tan(45°)" in output
    result = extract_result(output)
    expected = math.tan(math.radians(45))
    assert result is not None and abs(result - expected) < 1e-6

def test_trig_cot(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "cot 45")
    assert "cot(45°)" in output or "cot" in output
    result = extract_result(output)
    expected = 1 / math.tan(math.radians(45))
    assert result is not None and abs(result - expected) < 1e-6

def test_trig_sec(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "sec 60")
    assert "sec(60°)" in output or "sec" in output
    result = extract_result(output)
    expected = 1 / math.cos(math.radians(60))
    assert result is not None and abs(result - expected) < 1e-6

def test_trig_sec_zero(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "sec 90")
    assert "undefined" in output.lower()

def test_trig_csc(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "csc 30")
    assert "csc(30°)" in output or "csc" in output
    result = extract_result(output)
    expected = 1 / math.sin(math.radians(30))
    assert result is not None and abs(result - expected) < 1e-6

def test_invalid_operation(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "foo 30")
    assert "not supported" in output

def test_invalid_input_format(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "sin30")
    assert "Invalid input" in output or "enter an operation" in output

def test_invalid_angle(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "sin abc")
    assert "Invalid angle" in output or "numeric" in output

def test_empty_input(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "")
    assert "No input provided" in output

def test_cot_zero(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "cot 0")
    assert "undefined" in output.lower()

def test_sec_zero(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "sec 90")
    assert "undefined" in output.lower()

def test_csc_zero(monkeypatch, capsys):
    output = run_trig_test(monkeypatch, capsys, "csc 0")
    assert "undefined" in output.lower()
