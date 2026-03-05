from app.parsing.detect_runtime import detect_runtime
from app.parsing.parsers import python_parser, node_parser

def test_detect_runtime_python():
    log = """Traceback (most recent call last):
  File "test.py", line 1, in <module>
    1/0
ZeroDivisionError: division by zero"""
    assert detect_runtime(log) == "python"

def test_python_parser():
    log = """Traceback (most recent call last):
  File "test.py", line 5, in my_func
    result = 1 / 0
ZeroDivisionError: division by zero"""
    
    frames = python_parser.parse(log)
    assert len(frames) == 1
    assert frames[0]["file"] == "test.py"
    assert frames[0]["line"] == 5
    assert frames[0]["function"] == "my_func"
    assert "result = 1 / 0" in frames[0]["code_line"]

def test_node_parser():
    log = """TypeError: Cannot read properties of undefined
    at fetchUser (app.js:10:15)
    at main (index.js:20:5)"""
    
    frames = node_parser.parse(log)
    assert len(frames) == 2
    assert frames[0]["function"] == "fetchUser"
    assert frames[0]["file"] == "app.js"
    assert frames[0]["line"] == 10
