import pytest

from src.machine import Machine, TuringLogicError, TuringDumpFormatError
from src.syntax_parser import Code


def test_inverter():
    inverter = open("examples/inverter").read()
    machine = Machine.from_code(Code.from_str(inverter))
    machine.place_input(["1", "0", "1"])
    machine.execute()
    assert machine.read_result() == ["0", "1", "0"]


def test_double():
    double = open("examples/double").read()
    machine = Machine.from_code(Code.from_str(double))
    machine.place_input(["1", "0", "1"])
    machine.execute()
    assert machine.read_result() == ["1", "0", "1", "1", "0", "1"]


def test_loop():
    loop = open("examples/while_true").read()
    machine = Machine.from_code(Code.from_str(loop))
    machine.execute()
    assert machine.state != "_finish"
    with pytest.raises(TuringLogicError):
        machine.read_result()


def test_tape_extension_l():
    code = Code.from_str("_start,* -> left,*,L\nleft,* -> left,*,L")
    machine = Machine.from_code(code)
    machine.execute(100)


def test_tape_extension_r():
    code = Code.from_str("_start,* -> rg,*,R\nrg,* -> rg,*,R")
    machine = Machine.from_code(code)
    machine.execute(100)


def test_dump_error():
    with pytest.raises(TuringDumpFormatError):
        machine = Machine.from_code(Code.from_str(""))
        machine.apply_dump("wrong dump")


def test_dump():
    double = open("examples/double").read()
    machine = Machine.from_code(Code.from_str(double))
    machine.place_input(["1", "0", "1"])
    machine.execute(3)
    dump = machine.dump()

    machine.clean()
    machine.apply_dump(dump)
    machine.execute()
    assert machine.read_result() == ["1", "0", "1", "1", "0", "1"]


def test_get_symbol():
    machine = Machine.from_code(Code.from_str(""))
    machine.place_input(["1", "0", "1"])
    assert machine.get_symbol(0) == "1"
    assert machine.get_symbol(1) == "0"
    assert machine.get_symbol(2) == "1"
    assert machine.get_symbol(3) == "#"
    assert machine.get_symbol(-1) == "#"
