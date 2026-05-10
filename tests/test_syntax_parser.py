import pytest

from src.syntax_parser import Code, TuringSyntaxError


def test_basic():
    code = Code.from_str("")
    assert code.go("a", "a") is None


def test_inverter():
    inverter = open("examples/inverter").read()
    Code.from_str(inverter)


def test_double():
    double = open("examples/double").read()
    Code.from_str(double)


def test_pattern_inv():
    pattern_inverter = open("examples/pattern_inverter").read()
    Code.from_str(pattern_inverter)


def test_pattern_loop():
    pattern_loop = open("examples/pattern_while_true").read()
    Code.from_str(pattern_loop)


def test_match():
    code = Code.from_str("_start,h*pa -> state,t*st,N")
    assert code.go("_start", "hopa") == ("state", "tost", "N")


def test_wrong_syntax():
    with pytest.raises(TuringSyntaxError):
        Code.from_str("test")


def test_wrong_glob():
    with pytest.raises(TuringSyntaxError):
        Code.from_str("_start,# -> test,*,N")


def test_priority():
    code = Code.from_str(
        "_start,* -> state,*,N\nstate,* -> state,*,N\n_start,1 -> _finish,1,N"
    )
    assert code.go("_start", "0") == ("state", "0", "N")
    assert code.go("_start", "1") == ("_finish", "1", "N")
